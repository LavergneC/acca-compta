from django.urls import path

from acca_compta.journal_comptable.views_htmx import cancel_edit_nouvelle_ligne
from acca_compta.journal_comptable.views_htmx import edit_nouvelle_ligne
from acca_compta.journal_comptable.views_htmx import submit_half_nouvelle_ligne
from acca_compta.journal_comptable.views_htmx import submit_nouvelle_ligne
from acca_compta.journal_comptable.views_htmx import text_ligne

urlpatterns = [
    path(
        "edit_nouvelle_ligne",
        view=edit_nouvelle_ligne,
        name="edit_nouvelle_ligne",
    ),
    path(
        "cancel_edit_nouvelle_ligne",
        view=cancel_edit_nouvelle_ligne,
        name="cancel_edit_nouvelle_ligne",
    ),
    path(
        "submit_half_nouvelle_ligne",
        view=submit_half_nouvelle_ligne,
        name="submit_half_nouvelle_ligne",
    ),
    path(
        "submit_nouvelle_ligne",
        view=submit_nouvelle_ligne,
        name="submit_nouvelle_ligne",
    ),
    path(
        "text_ligne/<int:pk>",
        view=text_ligne,
        name="text_ligne",
    ),
]
