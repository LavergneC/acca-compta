from django import forms

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
