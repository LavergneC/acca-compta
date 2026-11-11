from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from rest_framework.test import APIRequestFactory

from acca_compta.users.api.views import UserViewSet

if TYPE_CHECKING:
    from acca_compta.users.models import User


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request  # type: ignore[assignment]

        assert user in view.get_queryset()

    def test_me(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet()
        request = api_rf.get("/fake-url/")
        request.user = user

        view.request = request  # type: ignore[assignment]

        response = view.me(request)

        assert response.data == {
            "url": f"http://testserver/api/users/{user.pk}/",
            "name": user.name,
        }
