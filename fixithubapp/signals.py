from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import User, EmailVerificationToken
from django.utils.crypto import get_random_string

@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created and not instance.is_verified:
        try:
            # Create or get the verification token
            token, created = EmailVerificationToken.objects.get_or_create(user=instance)
            
            # Generate verification link
            verification_link = f"{settings.FRONTEND_URL}/verify/{token.token}/"
            
            # Load email template
            subject = "Welcome to FixItHub - Please Verify Your Email"
            html_message = render_to_string("emails/welcome_email.html", {
                "user": instance,
                "verification_link": verification_link
            })
            plain_message = strip_tags(html_message)
            
            # Send email
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                html_message=html_message,
                fail_silently=False
            )
        except Exception as e:
            # Log the error but don't fail the user creation
            print(f"Error sending verification email: {str(e)}")
