from django import forms

from acca_compta.journal_comptable.models import Categorie
from acca_compta.journal_comptable.models import Ligne
from acca_compta.journal_comptable.models import SousCategorie


class NouvelleLigneForm(forms.models.ModelForm):
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all())

    class Meta:
        model = Ligne
        fields = ("date", "compte", "sous_categorie", "montant")
        widgets = {
            "date": forms.DateInput(
                format="%d/%m/%Y",
                attrs={"type": "date"},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # S'il y a des datas, c'est le post final, pas besoin de filtrer les categories
        if kwargs.get("data") is not None:
            return

        kwargs_initial: dict | None = kwargs.get("initial")
        if kwargs_initial is None:
            self.fields["sous_categorie"].disabled = True
            return

        if "categorie" not in kwargs_initial:
            return

        if (
            isinstance(kwargs_initial["categorie"], str) is False
            or kwargs_initial["categorie"].isdigit() is False
        ):
            return

        self.fields["sous_categorie"].queryset = SousCategorie.objects.filter(
            categorie=kwargs_initial["categorie"],
        )
