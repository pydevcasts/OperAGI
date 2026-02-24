from dj_rest_auth.forms import AllAuthPasswordResetForm
from django.contrib.sites.shortcuts import get_current_site

class CustomPasswordResetForm(AllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        
        # Override URL to point to Nuxt frontend
        kwargs['domain_override'] = 'localhost:3000'
        kwargs['use_https'] = False
        
        return super().save(request, **kwargs)