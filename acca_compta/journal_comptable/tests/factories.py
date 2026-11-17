import datetime as dt

from acca_compta.journal_comptable.models import Categorie
from acca_compta.journal_comptable.models import Compte
from acca_compta.journal_comptable.models import Ligne
from acca_compta.journal_comptable.models import MetaCategorie


def create_meta_categorie(nom: str) -> MetaCategorie:
    return MetaCategorie.objects.create(nom=nom)


def create_categorie(meta_categorie: MetaCategorie | str, nom: str) -> Categorie:
    if isinstance(meta_categorie, str):
        meta_categorie = create_meta_categorie(nom=meta_categorie)

    return Categorie.objects.create(meta_categorie=meta_categorie, nom=nom)


def create_compte(nom: str) -> Compte:
    return Compte.objects.create(nom=nom)


def create_ligne(
    date: dt.date | None = None,
    compte: Compte | None = None,
    categorie: Categorie | None = None,
    montant: float | None = None,
) -> Ligne:
    return Ligne.objects.create(
        date=date if date is not None else dt.date(2026, 9, 29),
        compte=compte if compte is not None else create_compte(nom="Credit"),
        categorie=categorie
        if categorie is not None
        else create_categorie(meta_categorie="Deck", nom="Carte"),
        montant=montant if montant is not None else 123.45,
    )
