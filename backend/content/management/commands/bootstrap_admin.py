import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the initial Django admin from environment variables, if configured."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        if not any((username, email, password)):
            self.stdout.write("Initial admin bootstrap skipped; no credentials configured.")
            return
        if not all((username, email, password)):
            raise CommandError(
                "Set DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, "
                "and DJANGO_SUPERUSER_PASSWORD together."
            )

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write("Initial admin already exists; credentials were left unchanged.")
            return

        user = User(username=username, email=email, is_staff=True, is_superuser=True)
        try:
            validate_password(password, user=user)
        except Exception as exc:
            raise CommandError(f"Initial admin password failed validation: {exc}") from exc

        user.set_password(password)
        user.save()
        self.stdout.write("Initial Django admin created.")
