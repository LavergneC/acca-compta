import pytest

from acca_compta.journal_comptable.forms import NouvelleLigneForm
from acca_compta.journal_comptable.tests.factories import create_categorie
from acca_compta.journal_comptable.tests.factories import create_compte
from acca_compta.journal_comptable.tests.factories import create_meta_categorie

pytestmark = pytest.mark.django_db


class TestNouvelleLigneForm:
    def test_form_renders_fields_input(self):
        form = NouvelleLigneForm()
        assert 'id="id_date"' in form.as_p()
        assert 'id="id_compte"' in form.as_p()
        assert 'id="id_categorie"' in form.as_p()
        assert 'id="id_meta_categorie"' in form.as_p()
        assert 'id="id_montant"' in form.as_p()

    def test_meta_categorie_field_values(self):
        meta_categories = [
            create_meta_categorie("Ventes"),
            create_meta_categorie("Loto"),
            create_meta_categorie("Repas"),
        ]

        form = NouvelleLigneForm()

        assert len(form.fields["meta_categorie"].queryset) == len(meta_categories)
        for meta_categorie in meta_categories:
            assert meta_categorie in form.fields["meta_categorie"].queryset

    def test_basic_form_validation(self):
        categorie = create_categorie("Achat", "Cartouche d'encre")
        compte = create_compte("Courant")
        data = {
            "date": "2026-11-17",
            "compte": compte.pk,
            "meta_categorie": categorie.meta_categorie.pk,
            "categorie": categorie.pk,
            "montant": "123.11",
        }

        form = NouvelleLigneForm(data=data)
        assert form.is_valid(), form.errors
