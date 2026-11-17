import datetime as dt

from functional_tests.base import FunctionalTest
from selenium.webdriver.common.by import By

from acca_compta.journal_comptable.tests.factories import create_categorie
from acca_compta.journal_comptable.tests.factories import create_compte
from acca_compta.journal_comptable.tests.factories import create_ligne


class LignesDuJournal(FunctionalTest):
    def setUp(self) -> None:
        super().setUp()

        create_ligne(
            date=dt.date(year=2025, month=7, day=4),
            compte=create_compte(nom="Banque"),
            categorie=create_categorie(meta_categorie="Grand gibier", nom="chevreuil"),
            montant=-258.54,
        )
        create_ligne(
            date=dt.date(year=2025, month=7, day=1),
            compte=create_compte(nom="Livret A"),
            categorie=create_categorie(meta_categorie="Intérêts", nom="Livret A"),
            montant=260.00,
        )

    def test_consulter_journal(self):
        # Depuis la page de garde
        self.browser.get(self.live_server_url)
        self.wait_for_page("ACCA Compta")

        # L'utilisateur utilise le menu pour accéder à la lecture du
        self.browser.find_element(By.ID, "journal_dropdown_id").click()
        self.browser.find_element(By.LINK_TEXT, "Consulter le journal").click()
        self.wait_for_page("Consulter le journal")

        # Les informations de la BDD sont correctement affichées
        ligne1 = self.browser.find_element(By.ID, "id_ligne_1")
        assert ligne1.find_element(By.ID, "id_date_1").text == "04/07/2025"
        assert ligne1.find_element(By.ID, "id_compte_1").text == "Banque"
        assert (
            ligne1.find_element(By.ID, "id_categorie_1").text
            == "Grand gibier - chevreuil"
        )
        assert ligne1.find_element(By.ID, "id_montant_1").text == "-258.54 €"

        ligne2 = self.browser.find_element(By.ID, "id_ligne_2")
        assert ligne2.find_element(By.ID, "id_date_2").text == "01/07/2025"
        assert ligne2.find_element(By.ID, "id_compte_2").text == "Livret A"
        assert (
            ligne2.find_element(By.ID, "id_categorie_2").text == "Intérêts - Livret A"
        )
        assert ligne2.find_element(By.ID, "id_montant_2").text == "+260.00 €"

    def test_ajouter_une_recette(self):
        # Depuis la page de garde
        self.browser.get(self.live_server_url)
        self.wait_for_page("ACCA Compta")

        # L'utilisateur utilise le menu pour accéder à l'ajout de recette
        self.browser.find_element(By.ID, "journal_dropdown_id").click()
        self.browser.find_element(By.LINK_TEXT, "Ajouter une recette").click()

        self.wait_for_page("Ajouter une recette")

        form = self.browser.find_element(By.ID, "id_ajouter_recette")

        # L'utilisateur sélectionne le compte "caisse"
        form.find_element(By.ID, "id_compte").click()
        form.find_element(By.XPATH, f"//option[. = '{'Caisse'}']").click()

        # Sélectionne la meta-catégorie "Frais généraux"
        form.find_element(By.ID, "id_meta_categorie").click()
        form.find_element(By.XPATH, f"//option[. = '{'Frais généraux'}']").click()

        # Sélectionne la catégorie "Papeterie"
        form.find_element(By.ID, "id_categorie").click()
        form.find_element(By.XPATH, f"//option[. = '{'Papeterie'}']").click()

        # Sélectionne la date
        date_element = self.browser.find_element(By.ID, "id_date")
        date_element.send_keys("2026-07-15")

        # Ajoute le montant de 10€50
        montant_element = self.browser.find_element(By.ID, "id_montant")
        montant_element.send_keys("10.50")

        # Valide l'ajout
        self.browser.find_element(By.ID, "id_valider").click()

        # Un message de succès s'affiche
        self.wait_for_message("Ligne comptable ajoutée")

        # L'utilisateur va voir son ajout dans le journal comptable
        # depuis l'url
        self.browser.get(self.live_server_url + "/journal/consulter")
        self.wait_for_page("Journal comptable")

        # Il repère la ligne qu'il vient d'ajouter
        ligne1 = self.browser.find_element(By.ID, "id_ligne_1")

        # Les informations correspondent
        assert ligne1.find_element(By.ID, "id_date_1").text == "15/07/2026"
        assert ligne1.find_element(By.ID, "id_compte_1").text == "Caisse"
        assert (
            ligne1.find_element(By.ID, "id_categorie_1").text
            == "Frais généraux - Papeterie"
        )
        assert ligne1.find_element(By.ID, "id_montant_1").text == "-10.50 €"
