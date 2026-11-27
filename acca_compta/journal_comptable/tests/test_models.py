import datetime as dt

import pytest

from acca_compta.journal_comptable.models import Categorie
from acca_compta.journal_comptable.models import Compte
from acca_compta.journal_comptable.models import SousCategorie
from acca_compta.journal_comptable.tests.factories import create_categorie
from acca_compta.journal_comptable.tests.factories import create_compte
from acca_compta.journal_comptable.tests.factories import create_ligne
from acca_compta.journal_comptable.tests.factories import create_sous_categorie

pytestmark = pytest.mark.django_db


class TestCategorieModel:
    def test_saving_and_retrieving_items(self):
        cat = create_categorie("Meta cat")

        assert cat.nom == "Meta cat"


class TestSousCategorieModel:
    def test_saving_and_retrieving_items(self):
        sous_categorie = create_sous_categorie(
            categorie=create_categorie("Meta cat"),
            nom="Cat",
        )

        assert sous_categorie.nom == "Cat"
        assert isinstance(sous_categorie.categorie, Categorie)
        assert sous_categorie.categorie.nom == "Meta cat"


class TestLigneModel:
    def test_saving_and_retrieving_items(self):
        ligne = create_ligne(
            date=dt.date(year=2025, month=7, day=4),
            compte=create_compte(nom="Banque"),
            sous_categorie=create_sous_categorie(
                categorie="Grand gibier",
                nom="Chevreuil",
            ),
            montant=1451786.21,
        )

        assert str(ligne.date) == "2025-07-04"

        assert isinstance(ligne.compte, Compte)
        assert str(ligne.compte) == "Banque"

        assert isinstance(ligne.sous_categorie, SousCategorie)
        assert str(ligne.sous_categorie) == "Grand gibier - Chevreuil"

        assert ligne.montant == 1451786.21  # noqa: PLR2004


class TestCompteModel:
    def test_saving_and_retrieving_items(self):
        compte = create_compte("Banque")

        assert compte.nom == "Banque"
