from django.db import models


class MetaCategorie(models.Model):
    nom = models.CharField(unique=True)

    def __str__(self) -> str:
        return self.nom


class Categorie(models.Model):
    nom = models.CharField(unique=True)
    meta_categorie = models.ForeignKey(
        "journal_comptable.MetaCategorie",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return str(self.meta_categorie) + " - " + self.nom


class Ligne(models.Model):
    date = models.DateField()
    compte = models.ForeignKey("journal_comptable.Compte", on_delete=models.CASCADE)
    categorie = models.ForeignKey(
        "journal_comptable.Categorie",
        on_delete=models.CASCADE,
    )
    montant = models.FloatField()

    def __str__(self) -> str:
        return (
            f"{self.date!s} - {self.compte!s} - {self.categorie!s} - {self.montant} €"
        )


class Compte(models.Model):
    nom = models.CharField()

    def __str__(self) -> str:
        return self.nom
