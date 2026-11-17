from typing import TYPE_CHECKING

from django.shortcuts import render

from acca_compta.journal_comptable.models import Ligne

if TYPE_CHECKING:
    from django.http import HttpResponse


def consulter_journal(request) -> HttpResponse:
    lignes = Ligne.objects.all().order_by("date").reverse()

    return render(
        request=request,
        template_name="journal_comptable/consulter.html",
        context={"lignes": lignes},
    )
