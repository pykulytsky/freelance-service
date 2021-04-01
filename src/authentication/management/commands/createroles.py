from typing import Any, Optional

from authentication.models import Role
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        for role_id in len(Role.ROLE_CHOISES):
            self.stdout(f"Creating role {Role.ROLE_CHOISES[role_id][1]}... ",)
            Role.objects.create_or_update(id=role_id)
            self.stdout("Done!")
