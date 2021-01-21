from typing import Any, Optional
from django.core.management.base import BaseCommand
from authentication.models import User


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        for user in User.objects.all():
            self.stdout.write(f'Delete {user}...')
            user.delete()
            self.stdout.write('Done')
        self.stdout.write('All users has been deleted.')
