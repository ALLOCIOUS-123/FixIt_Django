from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Clear all users and their associated data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force deletion without confirmation'
        )

    def handle(self, *args, **options):
        if not options['force']:
            confirm = input("\nAre you sure you want to delete ALL users and their data? This action cannot be undone. (yes/no): ")
            if confirm.lower() != 'yes':
                self.stdout.write(self.style.WARNING('Operation cancelled.'))
                return

        try:
            with transaction.atomic():
                # Delete all users
                User.objects.all().delete()
                
                # Delete all email verification tokens
                from fixithubapp.models import EmailVerificationToken
                EmailVerificationToken.objects.all().delete()
                
                # Delete all problems and solutions
                from fixithubapp.models import Problem, Solution, Vote
                Problem.objects.all().delete()
                Solution.objects.all().delete()
                Vote.objects.all().delete()
                
                self.stdout.write(self.style.SUCCESS('Successfully cleared all users and their data.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {str(e)}'))
