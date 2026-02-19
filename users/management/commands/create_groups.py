from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Создает группу Менеджеры и назначает права"

    def handle(self, *args, **options):
        managers_group, created = Group.objects.get_or_create(name="Менеджеры")

        # Получаем права
        permissions = Permission.objects.filter(
            codename__in=[
                "can_view_all_clients",
                "can_view_all_messages",
                "can_view_all_mailings",
                "can_disable_mailing",
            ]
        )

        managers_group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS("Группа Менеджеры создана или обновлена"))
