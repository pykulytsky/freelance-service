from typing import Any, Optional

from authentication.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        for user in User.objects.all():
            self.stdout.write(f'Delete {user}...')
            user.delete()
            self.stdout.write('Done.')
        self.stdout.write('All users has been deleted.')
