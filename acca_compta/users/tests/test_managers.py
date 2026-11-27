from io import StringIO

import pytest
from django.core.management import call_command

from acca_compta.users.models import User


@pytest.mark.django_db
class TestUserManager:
    def test_create_user(self):
        user = User.objects.create_user(
            username="john",
            password="something-r@nd0m!",  # noqa: S106
        )
        assert user.username == "john"
        assert not user.is_staff
        assert not user.is_superuser
        assert user.check_password("something-r@nd0m!")
        assert user.email is None

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username="admin",
            password="something-r@nd0m!",  # noqa: S106
        )
        assert user.username == "admin"
        assert user.is_staff
        assert user.is_superuser
        assert user.email is None


@pytest.mark.django_db
def test_createsuperuser_command():
    """Ensure createsuperuser command works with our custom manager."""
    out = StringIO()
    command_result = call_command(
        "createsuperuser",
        "--username",
        "henry",
        interactive=False,
        stdout=out,
    )

    assert command_result is None
    assert out.getvalue() == "Superuser created successfully.\n"
    user = User.objects.get(username="henry")
    assert not user.has_usable_password()
