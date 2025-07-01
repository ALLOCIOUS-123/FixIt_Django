from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from fixithubapp.models import EmailVerificationToken
import os

User = get_user_model()

class EmailVerificationTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            full_name='Test User'
        )
        self.user.is_active = False
        self.user.save()
        
        # Create a verification token
        self.token = EmailVerificationToken.objects.create(
            user=self.user,
            token='test-token-1234567890'
        )
        
    def test_email_verification(self):
        print("\nTesting Email Verification System")
        print("=================================")
        
        # Test 1: Verify email with valid token
        print("\nTest 1: Verify with valid token")
        response = self.client.get(reverse('verify_email', args=[self.token.token]))
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        print("✓ Test 1 passed: Email verified successfully")
        
        # Test 2: Verify with expired token
        print("\nTest 2: Verify with expired token")
        expired_token = EmailVerificationToken.objects.create(
            user=self.user,
            token='expired-token-123'
        )
        expired_token.created_at = timezone.now() - timezone.timedelta(hours=25)
        expired_token.save()
        
        response = self.client.get(reverse('verify_email', args=[expired_token.token]))
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('expired' in str(m) for m in messages))
        print("✓ Test 2 passed: Expired token handled correctly")
        
        # Test 3: Verify with invalid token
        print("\nTest 3: Verify with invalid token")
        response = self.client.get(reverse('verify_email', args=['invalid-token']))
        self.assertEqual(response.status_code, 302)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any('invalid' in str(m) for m in messages))
        print("✓ Test 3 passed: Invalid token handled correctly")
        
        # Test 4: Test email sending
        print("\nTest 4: Test email sending")
        user = User.objects.create_user(
            email='test2@example.com',
            password='testpassword123',
            full_name='Test User 2'
        )
        user.is_active = False
        user.save()
        
        # Create verification token
        token = EmailVerificationToken.objects.create(
            user=user,
            token='test-token-2345678901'
        )
        
        # Send verification email
        verification_url = f"{os.getenv('FRONTEND_URL', 'http://127.0.0.1:8000')}/verify/{token.token}/"
        subject = "Verify Your FixItHub Account"
        
        # Load HTML template
        from django.template.loader import render_to_string
        html_message = render_to_string('emails/verification_email.html', {
            'verification_url': verification_url,
            'full_name': user.full_name
        })
        
        # Send email
        from django.core.mail import send_mail
        send_mail(
            subject,
            'Please verify your email address by clicking the link in the email.',
            os.getenv('DEFAULT_FROM_EMAIL', 'noreply@fixithub.com'),
            [user.email],
            fail_silently=False,
            html_message=html_message
        )
        
        # Check if email was sent
        self.assertEqual(len(mail.outbox), 1)
        print("✓ Test 4 passed: Email sent successfully")
        
    def tearDown(self):
        # Clean up test data
        User.objects.all().delete()
        EmailVerificationToken.objects.all().delete()

if __name__ == '__main__':
    import unittest
    unittest.main()
