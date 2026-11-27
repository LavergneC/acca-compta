import datetime as dt
from http import HTTPStatus

import pytest
from django.urls import reverse

from acca_compta.journal_comptable.models import Ligne
from acca_compta.journal_comptable.tests.factories import create_compte
from acca_compta.journal_comptable.tests.factories import create_ligne
from acca_compta.journal_comptable.tests.factories import create_sous_categorie

pytestmark = pytest.mark.django_db


class TestConsulterJournalView:
    @pytest.fixture
    def url(self) -> str:
        return reverse("journal_comptable:consulter")

    @pytest.fixture
    def lignes(self) -> list[Ligne]:
        return [
            create_ligne(
                date=dt.date(year=2025, month=7, day=4),
                compte=create_compte(nom="Banque"),
                sous_categorie=create_sous_categorie("Frais", "Assurance"),
                montant=-12.45,
            ),
            create_ligne(
                date=dt.date(year=2025, month=7, day=1),
                compte=create_compte(nom="Caisse"),
                sous_categorie=create_sous_categorie("Cartes", "Extérieur"),
                montant=23400.00,
            ),
        ]

    def test_access_consulter_journal(self, client, url: str):
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK

    def test_consulter_journal_render_correct_template(self, client, url: str):
        response = client.get(url)

        assert "journal_comptable/consulter.html" in [
            t.name for t in response.templates
        ]

    def test_consulter_journal_retourne_les_lignes_dans_le_context(
        self,
        client,
        url: str,
        lignes: list[Ligne],
    ):
        response = client.get(url)
        received_lignes = response.context["lignes"]

        assert len(received_lignes) == len(lignes)
        assert all(isinstance(ligne, Ligne) for ligne in received_lignes)

        assert [ligne.pk for ligne in lignes] == [ligne.pk for ligne in received_lignes]

    def test_le_context_est_en_ordre_chronologique(self, client, url: str):
        create_ligne(date=dt.date(2026, 9, 29))
        create_ligne(date=dt.date(2026, 9, 30))
        create_ligne(date=dt.date(2026, 9, 28))

        response = client.get(url)
        received_lignes = response.context["lignes"]

        assert [str(ligne.date) for ligne in received_lignes] == [
            "2026-09-30",
            "2026-09-29",
            "2026-09-28",
        ]

    def test_affichage_du_context_dans_le_template(
        self,
        client,
        url: str,
        lignes: list[Ligne],
    ):
        response = client.get(url)

        for ligne in lignes:
            assert ligne.date.strftime("%d/%m/%Y") in response.content.decode("utf-8")
            assert str(ligne.compte) in response.content.decode("utf-8")
            assert str(ligne.sous_categorie) in response.content.decode("utf-8")
            assert str(ligne.montant) in response.content.decode("utf-8")

    def test_affichage_d_un_signe_plus_devant_les_montants_positif(
        self,
        client,
        url: str,
    ):
        create_ligne(montant=123)
        create_ligne(montant=-456)

        response = client.get(url)

        assert ">+123.00 €" in response.content.decode("utf-8")
        assert ">-456.00 €" in response.content.decode("utf-8")
