from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    is_subscribed = models.BooleanField(default=False)
    subscription_expiry = models.DateTimeField(null=True, blank=True)

    def has_active_subscription(self):
        return self.is_subscribed and self.subscription_expiry and self.subscription_expiry > timezone.now()

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(default=30)  # طول اشتراک بر حسب روز

    def __str__(self):
        return self.name

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)

    def activate_subscription(self):
        self.user.is_subscribed = True
        self.user.subscription_expiry = timezone.now() + timedelta(days=self.plan.duration_days)
        self.user.save()
