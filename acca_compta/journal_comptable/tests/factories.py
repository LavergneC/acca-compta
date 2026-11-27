import datetime as dt

from acca_compta.journal_comptable.models import Categorie
from acca_compta.journal_comptable.models import Compte
from acca_compta.journal_comptable.models import Ligne
from acca_compta.journal_comptable.models import SousCategorie


def create_categorie(nom: str) -> Categorie:
    return Categorie.objects.get_or_create(nom=nom)[0]


def create_sous_categorie(categorie: Categorie | str, nom: str) -> SousCategorie:
    if isinstance(categorie, str):
        categorie, _ = Categorie.objects.get_or_create(nom=categorie)

    return SousCategorie.objects.create(categorie=categorie, nom=nom)


def create_compte(nom: str) -> Compte:
    return Compte.objects.create(nom=nom)


def create_ligne(
    date: dt.date | None = None,
    compte: Compte | None = None,
    sous_categorie: SousCategorie | None = None,
    montant: float | None = None,
) -> Ligne:
    if sous_categorie is None:
        categorie, _ = Categorie.objects.get_or_create(nom="Deck")
        sous_categorie, _ = SousCategorie.objects.get_or_create(
            categorie=categorie,
            nom="Carte",
        )

    return Ligne.objects.create(
        date=date if date is not None else dt.date(2026, 9, 29),
        compte=compte if compte is not None else create_compte(nom="Credit"),
        sous_categorie=sous_categorie,
        montant=montant if montant is not None else 123.45,
    )
