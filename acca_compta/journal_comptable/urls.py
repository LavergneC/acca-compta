from django.urls import include
from django.urls import path

from acca_compta.journal_comptable.views import consulter_journal

app_name = "journal"

urlpatterns = [
    path("consulter", view=consulter_journal, name="consulter"),
]

urlpatterns += [path("htmx/", include("acca_compta.journal_comptable.urls_htmx"))]
