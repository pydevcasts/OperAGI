from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        # اگر از create_user برای سوپر یوزر استفاده می شود، اینها باید تنظیم شوند
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        
        if not email:
            raise ValueError(_("The Email must be set"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db) # استفاده از self._db برای حفظ ثبات در دیتابیس‌های مختلف
        return user

    def create_user(self, email, password=None, **extra_fields):
        # در اینجا مطمئن می شویم که is_staff و is_superuser به درستی تنظیم می شوند
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # فراخوانی create_user که اکنون _create_user را فراخوانی می کند
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)  # ✅ افزودن این خط
    google_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name="Google ID"
    )

    profile_picture = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="تصویر پروفایل"
    )

    is_email_verified = models.BooleanField(
        default=False,
        verbose_name="ایمیل تأیید شده"
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class SubscriptionPlan(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)
    monthly_post_limit = models.PositiveIntegerField(null=True, blank=True)
    social_account_limit = models.PositiveIntegerField(default=2)
    features = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ('sort_order', 'price')

    def __str__(self):
        return self.name


class UserSubscription(models.Model):
    class Status(models.TextChoices):
        TRIAL = 'trial', 'Trial'
        ACTIVE = 'active', 'Active'
        PAST_DUE = 'past_due', 'Past due'
        CANCELLED = 'cancelled', 'Cancelled'
        EXPIRED = 'expired', 'Expired'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.TRIAL)
    current_period_start = models.DateTimeField(default=timezone.now)
    current_period_end = models.DateTimeField(null=True, blank=True)
    external_customer_id = models.CharField(max_length=255, blank=True, default='')
    external_subscription_id = models.CharField(max_length=255, blank=True, default='')
    cancel_at_period_end = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} — {self.plan.name}'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)

    def activate_subscription(self):
        now = timezone.now()
        UserSubscription.objects.update_or_create(
            user=self.user,
            defaults={
                'plan': self.plan,
                'status': UserSubscription.Status.ACTIVE,
                'current_period_start': now,
                'current_period_end': now + timedelta(days=self.plan.duration_days),
            },
        )
