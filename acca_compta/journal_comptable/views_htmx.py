from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from acca_compta.journal_comptable.forms import NouvelleLigneForm
from acca_compta.journal_comptable.models import Ligne
from acca_compta.utils import require_htmx


@require_GET
@require_htmx
def edit_nouvelle_ligne(request) -> HttpResponse:
    return render(
        request,
        template_name="journal_comptable/components/edit_nouvelle_ligne.html",
        context={"form": NouvelleLigneForm()},
    )


@require_GET
@require_htmx
def cancel_edit_nouvelle_ligne(request) -> HttpResponse:
    return HttpResponse()


@require_POST
@require_htmx
def submit_half_nouvelle_ligne(request) -> HttpResponse:
    form = NouvelleLigneForm(initial=request.POST.dict())
    return render(
        request,
        template_name="journal_comptable/components/edit_nouvelle_ligne.html",
        context={"form": form},
    )


@require_POST
@require_htmx
def submit_nouvelle_ligne(request) -> HttpResponse:
    form = NouvelleLigneForm(data=request.POST)
    if form.is_valid() is False:
        return render(
            request,
            template_name="journal_comptable/components/edit_nouvelle_ligne.html",
            context={"form": form},
        )

    messages.success(request, "Ligne comptable ajoutée")

    ligne = form.save()
    return redirect(reverse("journal_comptable:text_ligne", kwargs={"pk": ligne.pk}))


@require_GET
@require_htmx
def text_ligne(request, pk: int) -> HttpResponse:
    return render(
        request,
        template_name="journal_comptable/components/text_ligne.html",
        context={"ligne": Ligne.objects.get(pk=pk)},
    )
