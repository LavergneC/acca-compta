import pytest

from acca_compta.journal_comptable.forms import NouvelleLigneForm
from acca_compta.journal_comptable.models import Categorie
from acca_compta.journal_comptable.tests.factories import create_categorie
from acca_compta.journal_comptable.tests.factories import create_compte
from acca_compta.journal_comptable.tests.factories import create_sous_categorie

pytestmark = pytest.mark.django_db


class TestNouvelleLigneForm:
    def test_form_renders_fields_input(self):
        form = NouvelleLigneForm()
        assert 'id="id_date"' in form.as_p()
        assert 'id="id_compte"' in form.as_p()
        assert 'id="id_categorie"' in form.as_p()
        assert 'id="id_sous_categorie"' in form.as_p()
        assert 'id="id_montant"' in form.as_p()

    def test_meta_categorie_field_values(self):
        meta_categories = [
            create_categorie("Ventes"),
            create_categorie("Loto"),
            create_categorie("Repas"),
        ]

        form = NouvelleLigneForm()

        assert len(form.fields["categorie"].queryset) == len(meta_categories)
        for categorie in meta_categories:
            assert categorie in form.fields["categorie"].queryset

    def test_basic_form_validation(self):
        sous_categorie = create_sous_categorie("Achat", "Cartouche d'encre")
        compte = create_compte("Courant")
        data = {
            "date": "2026-11-17",
            "compte": compte.pk,
            "categorie": sous_categorie.categorie.pk,
            "sous_categorie": sous_categorie.pk,
            "montant": "123.11",
        }

        form = NouvelleLigneForm(data=data)
        assert form.is_valid(), form.errors

    def test_sous_categorie_verrouille_si_le_formulaire_est_initialise_sans_categorie(
        self,
    ):
        form = NouvelleLigneForm()
        assert form.fields["sous_categorie"].disabled is True

        # A l'inverse, si la categorie est passée à l'initialisation
        # le champs est actif
        form = NouvelleLigneForm(
            initial={"categorie": str(create_categorie(nom="tempMeta").pk)},
        )
        assert form.fields["sous_categorie"].disabled is False

    def test_formulaire_avec_categorie_filtre_les_sous_categories(self):
        # Lorsque l'on sélectionne une meta-categorie, alors le champs catégorie
        # n'affiche que les catégorie liés
        plante1 = create_sous_categorie("Plantes", "Pilea")
        plante2 = create_sous_categorie("Plantes", "Arbre")
        caillou = create_sous_categorie("Caillou", "Granite")

        form = NouvelleLigneForm(
            initial={
                "categorie": str(Categorie.objects.get(nom="Plantes").pk),
            },
        )

        sous_categories = form.fields["sous_categorie"].queryset
        assert plante1 in sous_categories
        assert plante2 in sous_categories
        assert caillou not in sous_categories

    def test_formulaire_sans_categorie(self):
        form = NouvelleLigneForm(
            initial={
                "date": "2026-11-17",
                "compte": create_compte("azerty"),
            },
        )
        assert form.is_valid() is False

    def test_formulaire_categorie_vide(self):
        form = NouvelleLigneForm(
            initial={
                "date": "2026-11-17",
                "compte": create_compte("azerty"),
                "categorie": "",
            },
        )
        assert form.is_valid() is False
