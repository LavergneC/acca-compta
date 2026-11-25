import pytest

from acca_compta.journal_comptable.forms import NouvelleLigneForm
from acca_compta.journal_comptable.models import MetaCategorie
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

    def test_categorie_verrouille_si_le_formulaire_est_initialise_sans_meta_categorie(
        self,
    ):
        form = NouvelleLigneForm()
        assert form.fields["categorie"].disabled is True

        # A l'inverse, si la meta_categorie est passée à l'initialisation
        # le champs est actif
        form = NouvelleLigneForm(
            initial={"meta_categorie": str(create_meta_categorie(nom="tempMeta").pk)},
        )
        assert form.fields["categorie"].disabled is False

    def test_formulaire_avec_meta_categorie_filtre_les_categories(self):
        # Lorsque l'on sélectionne une meta-categorie, alors le champs catégorie
        # n'affiche que les catégorie liés
        plante1 = create_categorie(meta_categorie="Plantes", nom="Pilea")
        plante2 = create_categorie(meta_categorie="Plantes", nom="Arbre")
        caillou = create_categorie(meta_categorie="Caillou", nom="Granite")

        form = NouvelleLigneForm(
            initial={
                "meta_categorie": str(MetaCategorie.objects.get(nom="Plantes").pk),
            },
        )

        categories = form.fields["categorie"].queryset
        assert plante1 in categories
        assert plante2 in categories
        assert caillou not in categories

    def test_formulaire_sans_meta_categorie(self):
        form = NouvelleLigneForm(
            initial={
                "date": "2026-11-17",
                "compte": create_compte("azerty"),
            },
        )
        assert form.is_valid() is False

    def test_formulaire_meta_categorie_vide(self):
        form = NouvelleLigneForm(
            initial={
                "date": "2026-11-17",
                "compte": create_compte("azerty"),
                "meta_categorie": "",
            },
        )
        assert form.is_valid() is False
