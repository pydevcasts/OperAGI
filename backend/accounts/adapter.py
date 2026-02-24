from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        return f"{settings.FRONTEND_URL}/verify-email/{emailconfirmation.key}"
    
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        
        ctx = {
            'user': emailconfirmation.email_address.user,
            'activate_url': activate_url,
            'key': emailconfirmation.key,
        }
        
        subject = 'تأیید ایمیل OperAGI'
        body_txt = f"برای تأیید ایمیل روی این لینک کلیک کنید:\n{activate_url}"
        body_html = render_to_string('account/email/email_confirmation_message.html', ctx)
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=body_txt,
            from_email=self.get_from_email(),
            to=[emailconfirmation.email_address.email]
        )
        msg.attach_alternative(body_html, "text/html")
        msg.send()
    
    def send_password_reset_mail(self, user, email, extra_email_context):
        extra_email_context = extra_email_context or {}
        extra_email_context['frontend_url'] = settings.FRONTEND_URL
        super().send_password_reset_mail(user, email, extra_email_context)