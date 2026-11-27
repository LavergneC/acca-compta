import datetime as dt

from functional_tests.base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from acca_compta.journal_comptable.models import Ligne
from acca_compta.journal_comptable.tests.factories import create_categorie
from acca_compta.journal_comptable.tests.factories import create_compte
from acca_compta.journal_comptable.tests.factories import create_ligne


class LignesDuJournal(FunctionalTest):
    def setUp(self) -> None:
        super().setUp()
        self.login()

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
        create_categorie(meta_categorie="Frais généraux", nom="Papeterie")
        create_compte("Caisse")

    def test_consulter_journal(self):
        # Depuis la page de garde
        self.browser.get(self.live_server_url)
        self.wait_for_page("ACCA Compta")

        # L'utilisateur utilise le menu pour accéder à la lecture du Journal Comptable
        self.browser.find_element(By.LINK_TEXT, "Journal Comptable").click()
        self.wait_for_page("Journal comptable")

        # Les informations de la BDD sont correctement affichées
        ligne1 = self.browser.find_element(By.ID, "id_ligne_1")
        assert ligne1.find_element(By.ID, "id_date_1").text == "04/07/2025"
        assert ligne1.find_element(By.ID, "id_compte_1").text == "Banque"
        assert (
            ligne1.find_element(By.ID, "id_categorie_1").text
            == "Grand gibier - chevreuil"
        )
        assert ligne1.find_element(By.ID, "id_montant_1").text == "-258,54 €"

        ligne2 = self.browser.find_element(By.ID, "id_ligne_2")
        assert ligne2.find_element(By.ID, "id_date_2").text == "01/07/2025"
        assert ligne2.find_element(By.ID, "id_compte_2").text == "Livret A"
        assert (
            ligne2.find_element(By.ID, "id_categorie_2").text == "Intérêts - Livret A"
        )
        assert ligne2.find_element(By.ID, "id_montant_2").text == "+260,00 €"

    def test_ajouter_une_recette(self):
        # Depuis la page de garde
        self.browser.get(self.live_server_url)
        self.wait_for_page("ACCA Compta")

        # L'utilisateur utilise le menu pour accéder au journal
        self.browser.find_element(By.LINK_TEXT, "Journal Comptable").click()
        self.wait_for_page("Journal comptable")

        # Il clique sur le bouton d'ajout de ligne
        self.browser.find_element(By.ID, "id_ajouter-ligne-button").click()
        form = self.wait_for_element("id_form-nouvelle-ligne")

        # L'utilisateur sélectionne le compte
        compte_selection = Select(form.find_element(By.ID, "id_compte"))
        compte_selection.select_by_visible_text("Caisse")

        # La catégorie est verrouillée tant que la meta-catégorie n'est pas sélectionnée
        categorie = form.find_element(By.ID, "id_categorie")
        assert not categorie.is_enabled()

        # Sélectionne la meta-catégorie
        meta_categorie = Select(form.find_element(By.ID, "id_meta_categorie"))
        meta_categorie.select_by_visible_text("Frais généraux")

        # Sélectionne la catégorie
        form = self.wait_for_element("id_form-nouvelle-ligne")
        categorie = Select(form.find_element(By.ID, "id_categorie"))
        categorie.select_by_visible_text("Frais généraux - Papeterie")

        # Sélectionne la date
        date_element = self.browser.find_element(By.ID, "id_date")
        date_element.send_keys("2026-07-15")

        # Ajoute le montant de -10€50
        montant_element = self.browser.find_element(By.ID, "id_montant")
        montant_element.send_keys("-10.50")

        # Valide l'ajout
        self.browser.find_element(By.ID, "id_form-submit-button").click()

        # Un message de succès s'affiche
        self.wait_for_message("Ligne comptable ajoutée")

        # L'utilisateur va voir son ajout dans le journal comptable
        # depuis l'url
        self.browser.get(self.live_server_url + "/journal_comptable/consulter")
        self.wait_for_page("Journal comptable")

        # Il repère la ligne qu'il vient d'ajouter
        new_id = Ligne.objects.last().pk
        ligne1 = self.browser.find_element(By.ID, f"id_ligne_{new_id}")

        # Les informations correspondent
        assert ligne1.find_element(By.ID, f"id_date_{new_id}").text == "15/07/2026"
        assert ligne1.find_element(By.ID, f"id_compte_{new_id}").text == "Caisse"
        assert (
            ligne1.find_element(By.ID, f"id_categorie_{new_id}").text
            == "Frais généraux - Papeterie"
        )
        assert ligne1.find_element(By.ID, f"id_montant_{new_id}").text == "-10,50 €"
