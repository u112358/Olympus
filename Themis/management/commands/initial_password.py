from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from Themis.models import Employee


class Command(BaseCommand):
    help = 'Sets initial passwords for all users who do not have one.'

    def handle(self, *args, **options):
        users = Employee.objects.all()  # 或使用更合适的筛选条件，如password__isnull=True
        for user in users:
            user.password = make_password('dihuge123')
            user.is_staff = True
            if user.name == "hubingzhang":
                user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully set password for {user.username}'))
