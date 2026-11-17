import datetime as dt

import pytest

from acca_compta.journal_comptable.models import Categorie
from acca_compta.journal_comptable.models import Compte
from acca_compta.journal_comptable.models import MetaCategorie
from acca_compta.journal_comptable.tests.factories import create_categorie
from acca_compta.journal_comptable.tests.factories import create_compte
from acca_compta.journal_comptable.tests.factories import create_ligne
from acca_compta.journal_comptable.tests.factories import create_meta_categorie

pytestmark = pytest.mark.django_db


class TestMetaCategorieModel:
    def test_saving_and_retrieving_items(self):
        meta_cat = create_meta_categorie("Meta cat")

        assert meta_cat.nom == "Meta cat"


class TestCategorieModel:
    def test_saving_and_retrieving_items(self):
        cat = create_categorie(
            meta_categorie=create_meta_categorie("Meta cat"),
            nom="Cat",
        )

        assert cat.nom == "Cat"
        assert isinstance(cat.meta_categorie, MetaCategorie)
        assert cat.meta_categorie.nom == "Meta cat"


class TestLigneModel:
    def test_saving_and_retrieving_items(self):
        ligne = create_ligne(
            date=dt.date(year=2025, month=7, day=4),
            compte=create_compte(nom="Banque"),
            categorie=create_categorie(meta_categorie="Grand gibier", nom="Chevreuil"),
            montant=1451786.21,
        )

        assert str(ligne.date) == "2025-07-04"

        assert isinstance(ligne.compte, Compte)
        assert str(ligne.compte) == "Banque"

        assert isinstance(ligne.categorie, Categorie)
        assert str(ligne.categorie) == "Grand gibier - Chevreuil"

        assert ligne.montant == 1451786.21  # noqa: PLR2004


class TestCompteModel:
    def test_saving_and_retrieving_items(self):
        compte = create_compte("Banque")

        assert compte.nom == "Banque"
