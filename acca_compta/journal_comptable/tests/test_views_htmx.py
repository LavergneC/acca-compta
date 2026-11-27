import datetime as dt
from http import HTTPStatus

import pytest
from django.contrib import messages
from django.urls import reverse

from acca_compta.journal_comptable.forms import NouvelleLigneForm
from acca_compta.journal_comptable.models import Ligne
from acca_compta.journal_comptable.tests.factories import create_compte
from acca_compta.journal_comptable.tests.factories import create_ligne
from acca_compta.journal_comptable.tests.factories import create_sous_categorie
from acca_compta.test_utils import HtmxClient

pytestmark = pytest.mark.django_db


class TestEditNouvelleLigneView:
    @pytest.fixture
    def client(self) -> HtmxClient:
        return HtmxClient()

    @pytest.fixture
    def url(self):
        return reverse("journal_comptable:edit_nouvelle_ligne")

    def test_access_view_with_htmx_get(self, client: HtmxClient, url: str):
        response = client.htmx_get(url)
        assert response.status_code == HTTPStatus.OK

    def test_cant_access_view_with_normal_get(self, client: HtmxClient, url: str):
        response = client.get(url)
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_cant_post_with_htmx(self, client: HtmxClient, url: str):
        response = client.htmx_post(url)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_use_right_template(self, client: HtmxClient, url: str):
        response = client.htmx_get(url)
        assert "journal_comptable/components/edit_nouvelle_ligne.html" in [
            t.name for t in response.templates
        ]

    def test_contains_nouvelle_ligne_form_in_context(
        self,
        client: HtmxClient,
        url: str,
    ):
        response = client.htmx_get(url)
        assert isinstance(response.context["form"], NouvelleLigneForm)

    def test_save_button_post_to_the_correct_url(
        self,
        url: str,
        client: HtmxClient,
    ):
        response = client.htmx_get(url)
        assert (
            f'hx-post="{reverse("journal_comptable:submit_nouvelle_ligne")}"'
            in response.content.decode()
        )

    def test_cancel_button_return_blank_template(
        self,
        client: HtmxClient,
        url: str,
    ):
        expected_url = reverse("journal_comptable:cancel_edit_nouvelle_ligne")
        response = client.htmx_get(url)
        assert f'hx-get="{expected_url}"' in response.content.decode()

    def test_meta_categorie_fait_un_post_htmx_sur_submit_half_nouvelle_ligne(
        self,
        url: str,
        client: HtmxClient,
    ):
        response = client.htmx_get(url)

        expected_url = reverse("journal_comptable:submit_half_nouvelle_ligne")
        assert f'hx-post="{expected_url}"' in response.content.decode(), (
            f"Expected '{expected_url}' in response"
        )


class TestCancelEditNouvelleLigne:
    @pytest.fixture
    def client(self):
        return HtmxClient()

    @pytest.fixture
    def url(self) -> str:
        return reverse("journal_comptable:cancel_edit_nouvelle_ligne")

    def test_access_view_with_htmx_get(self, client: HtmxClient, url: str):
        response = client.htmx_get(url)
        assert response.status_code == HTTPStatus.OK

    def test_cant_access_view_with_normal_get(self, client: HtmxClient, url: str):
        response = client.get(url)
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_cant_post_with_htmx(self, client: HtmxClient, url: str):
        response = client.htmx_post(url)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_returned_html_content_is_blank(self, client: HtmxClient, url: str):
        response = client.htmx_get(url)
        assert response.content.decode("utf-8") == ""


class TestHalfSubmitNouvelleLigne:
    @pytest.fixture
    def client(self):
        return HtmxClient()

    @pytest.fixture
    def url(self) -> str:
        return reverse("journal_comptable:submit_half_nouvelle_ligne")

    @pytest.fixture
    def half_data(self) -> dict:
        self.categorie = create_sous_categorie("Achat", "Cartouche d'encre")
        self.compte = create_compte("Courant")

        return {
            "date": "2026-11-17",
            "compte": self.compte.pk,
            "categorie": self.categorie.categorie.pk,
            "montant": -123.45,
        }

    def test_access_view_with_htmx_post(
        self,
        client: HtmxClient,
        url: str,
        half_data: dict,
    ):
        response = client.htmx_post(url, data=half_data)
        assert response.status_code == HTTPStatus.OK

    def test_cant_access_view_with_normal_post(self, client: HtmxClient, url: str):
        response = client.post(url, data={})
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_cant_get_with_htmx(self, client: HtmxClient, url: str):
        response = client.htmx_get(url)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_post_return_filled_edit_nouvelle_ligne_htmx_view(
        self,
        client: HtmxClient,
        url: str,
        half_data: dict,
    ):
        response = client.htmx_post(url, data=half_data)
        assert response.status_code == HTTPStatus.OK
        assert "journal_comptable/components/edit_nouvelle_ligne.html" in [
            t.name for t in response.templates
        ]
        assert response.context["form"]["compte"].value() == str(self.compte.pk)
        assert response.context["form"]["date"].value() == "2026-11-17"
        assert response.context["form"]["categorie"].value() == str(
            self.categorie.categorie.pk,
        )

        assert response.context["form"]["montant"].value() == "-123.45"


class TestSubmitNouvelleLigne:
    @pytest.fixture
    def client(self):
        return HtmxClient()

    @pytest.fixture
    def url(self) -> str:
        return reverse("journal_comptable:submit_nouvelle_ligne")

    @pytest.fixture
    def data(self) -> dict:
        sous_categorie = create_sous_categorie("Achat", "Cartouche d'encre")
        self.compte = create_compte("Courant")

        return {
            "date": "2026-11-17",
            "compte": self.compte.pk,
            "categorie": sous_categorie.categorie.pk,
            "sous_categorie": sous_categorie.pk,
            "montant": "123.11",
        }

    def test_access_view_with_htmx_post(
        self,
        client: HtmxClient,
        url: str,
        data: dict,
    ):
        response = client.htmx_post(url, data=data)
        assert response.status_code == HTTPStatus.FOUND

    def test_cant_access_view_with_normal_post(self, client: HtmxClient, url: str):
        response = client.post(url, data={})
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_cant_get_with_htmx(self, client: HtmxClient, url: str):
        response = client.htmx_get(url)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_post_create_new_new_line_in_db(
        self,
        client: HtmxClient,
        url: str,
        data: dict,
    ):
        assert Ligne.objects.count() == 0

        client.htmx_post(url, data=data)

        new_ligne = Ligne.objects.first()
        assert new_ligne is not None
        assert new_ligne.date == dt.date(year=2026, month=11, day=17)
        assert new_ligne.compte.pk == data["compte"]
        assert new_ligne.sous_categorie.pk == data["sous_categorie"]
        assert new_ligne.montant == float(data["montant"])

    def test_post_redirect_to_text_htmx_view_on_success_with_message(
        self,
        client: HtmxClient,
        url: str,
        data: dict,
    ):
        assert Ligne.objects.count() == 0

        response = client.htmx_post(url, data=data)
        assert response.status_code == HTTPStatus.FOUND

        expected_url = reverse(
            "journal_comptable:text_ligne",
            kwargs={"pk": Ligne.objects.first().pk},
        )
        assert response.url == expected_url

        messages_sent = [
            m.message for m in messages.get_messages(response.wsgi_request)
        ]
        assert messages_sent == ["Ligne comptable ajoutée"]

    def test_post_return_edit_nouvelle_ligne_htmx_view_on_error(
        self,
        client: HtmxClient,
        url: str,
        data: dict,
    ):
        data.pop("montant")

        response = client.htmx_post(url, data=data)
        assert response.status_code == HTTPStatus.OK
        assert "journal_comptable/components/edit_nouvelle_ligne.html" in [
            t.name for t in response.templates
        ]
        assert response.context["form"]["compte"].value() == str(self.compte.pk)


class TestTextLigne:
    @pytest.fixture
    def client(self) -> HtmxClient:
        return HtmxClient()

    @pytest.fixture
    def url(self):
        self.ligne = create_ligne(
            date=dt.date(year=2024, month=7, day=4),
            compte=create_compte(nom="Super Banque"),
            sous_categorie=create_sous_categorie("Gibier", "Escargot"),
            montant=-1,
        )
        return reverse("journal_comptable:text_ligne", kwargs={"pk": self.ligne.pk})

    def test_access_view_with_htmx_get(self, client: HtmxClient, url: str):
        response = client.htmx_get(url)
        assert response.status_code == HTTPStatus.OK

    def test_cant_access_view_with_normal_get(self, client: HtmxClient, url: str):
        response = client.get(url)
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_cant_post_with_htmx(self, client: HtmxClient, url: str):
        response = client.htmx_post(url)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_use_right_template(self, client: HtmxClient, url: str):
        response = client.htmx_get(url)
        assert "journal_comptable/components/text_ligne.html" in [
            t.name for t in response.templates
        ]

    def test_passe_la_ligne_dans_le_context(self, client: HtmxClient, url: str):
        response = client.htmx_get(url)

        assert "ligne" in response.context
        assert response.context["ligne"].pk == self.ligne.pk

    def test_affiche_la_ligne_passee_en_argument(self, client: HtmxClient, url: str):
        response = client.htmx_get(url)
        assert "Gibier" in response.content.decode("utf-8")
        assert "Escargot" in response.content.decode("utf-8")
        assert "Super Banque" in response.content.decode("utf-8")
        assert "04/07/2024" in response.content.decode("utf-8")
        assert "-1" in response.content.decode("utf-8")
