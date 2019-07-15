from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from feedzero.rules.jobs import process_rules_for_user

User = get_user_model()


class Command(BaseCommand):
    help = "Enqueue rule processing"

    def handle(self, *args, **options):
        for user in User.objects.filter(is_active=True):
            if settings.RQ_ENABLED:
                process_rules_for_user.delay(user)
            else:
                process_rules_for_user(user)
