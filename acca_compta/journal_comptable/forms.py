from django import forms

from acca_compta.journal_comptable.models import Categorie
from acca_compta.journal_comptable.models import Ligne
from acca_compta.journal_comptable.models import MetaCategorie


class NouvelleLigneForm(forms.models.ModelForm):
    meta_categorie = forms.ModelChoiceField(queryset=MetaCategorie.objects.all())

    class Meta:
        model = Ligne
        fields = ("date", "compte", "categorie", "montant")
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
            self.fields["categorie"].disabled = True
            return

        if "meta_categorie" not in kwargs_initial:
            return

        if (
            isinstance(kwargs_initial["meta_categorie"], str) is False
            or kwargs_initial["meta_categorie"].isdigit() is False
        ):
            return

        self.fields["categorie"].queryset = Categorie.objects.filter(
            meta_categorie=kwargs_initial["meta_categorie"],
        )
