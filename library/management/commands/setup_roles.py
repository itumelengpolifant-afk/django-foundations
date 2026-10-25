
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

ROLES = {
    'Member': [
        'view_book',
    ],
    'Librarian': [
        'view_book',
        'add_book',
        'change_book',
        'delete_book',
        'add_author',
        'change_author',
        'add_publisher',
        'change_publisher',
        'add_bookauthor',
        'change_bookauthor',
        'delete_bookauthor',
    ],
}


class Command(BaseCommand):
    help = 'Create Member and Librarian groups with permissions'

    def handle(self, *args, **options):
        for role, codenames in ROLES.items():
            group, _ = Group.objects.get_or_create(name=role)

            permissions = Permission.objects.filter(
                content_type__app_label='library',
                codename__in=codenames
            )

            group.permissions.set(permissions)

            self.stdout.write(
                self.style.SUCCESS(
                    f'{role}: {permissions.count()} permissions'
                )
            )
