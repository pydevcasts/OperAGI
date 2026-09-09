import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models

PLANS = [
    ('starter', 'Starter', '19.00', 30, 2, ['30 posts/month', '2 social platforms', 'Caption generation'], 1),
    ('pro', 'Pro', '49.00', 150, 3, ['150 posts/month', '3 social platforms', 'Scheduling', 'Analytics'], 2),
    ('agency', 'Agency', '99.00', None, 5, ['Unlimited posts', '5 social accounts', 'API access', 'White-label reports'], 3),
]


def seed_plans(apps, schema_editor):
    Plan = apps.get_model('accounts', 'SubscriptionPlan')
    for slug, name, price, limit, accounts, features, order in PLANS:
        Plan.objects.update_or_create(slug=slug, defaults={'name': name, 'price': price, 'monthly_post_limit': limit, 'social_account_limit': accounts, 'features': features, 'sort_order': order, 'is_active': True})


class Migration(migrations.Migration):
    dependencies = [('accounts', '0001_initial')]
    operations = [
        migrations.AddField(model_name='subscriptionplan', name='features', field=models.JSONField(blank=True, default=list)),
        migrations.AddField(model_name='subscriptionplan', name='is_active', field=models.BooleanField(default=True)),
        migrations.AddField(model_name='subscriptionplan', name='monthly_post_limit', field=models.PositiveIntegerField(blank=True, null=True)),
        migrations.AddField(model_name='subscriptionplan', name='slug', field=models.SlugField(null=True)),
        migrations.AddField(model_name='subscriptionplan', name='social_account_limit', field=models.PositiveIntegerField(default=2)),
        migrations.AddField(model_name='subscriptionplan', name='sort_order', field=models.PositiveSmallIntegerField(default=0)),
        migrations.AlterModelOptions(name='subscriptionplan', options={'ordering': ('sort_order', 'price')}),
        migrations.RunPython(seed_plans, migrations.RunPython.noop),
        migrations.AlterField(model_name='subscriptionplan', name='slug', field=models.SlugField(unique=True)),
        migrations.CreateModel(name='UserSubscription', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('status', models.CharField(choices=[('trial', 'Trial'), ('active', 'Active'), ('past_due', 'Past due'), ('cancelled', 'Cancelled'), ('expired', 'Expired')], default='trial', max_length=16)),
            ('current_period_start', models.DateTimeField(default=django.utils.timezone.now)), ('current_period_end', models.DateTimeField(blank=True, null=True)),
            ('external_customer_id', models.CharField(blank=True, default='', max_length=255)), ('external_subscription_id', models.CharField(blank=True, default='', max_length=255)),
            ('cancel_at_period_end', models.BooleanField(default=False)), ('created_at', models.DateTimeField(auto_now_add=True)), ('updated_at', models.DateTimeField(auto_now=True)),
            ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='accounts.subscriptionplan')),
            ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to=settings.AUTH_USER_MODEL)),
        ]),
    ]
