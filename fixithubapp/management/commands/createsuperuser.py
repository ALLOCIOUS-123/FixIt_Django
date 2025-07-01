from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser account with email verification'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Superuser email address', required=True)
        parser.add_argument('--password', type=str, help='Superuser password', required=True)
        parser.add_argument('--full-name', type=str, help='Superuser full name', default='Admin User')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        full_name = options['full_name']

        try:
            # Check if user already exists
            if User.objects.filter(email=email).exists():
                self.stdout.write(self.style.WARNING(f'User with email {email} already exists.'))
                return

            # Create superuser
            user = User.objects.create_superuser(
                email=email,
                password=password,
                full_name=full_name
            )

            # Set user as active and verified
            user.is_active = True
            user.is_verified = True
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {email}'))

        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {str(e)}'))
