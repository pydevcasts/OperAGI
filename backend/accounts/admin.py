from django.contrib import admin

from accounts.models import Payment, SubscriptionPlan, User, UserSubscription

admin.site.register(User)
admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
admin.site.register(Payment)
