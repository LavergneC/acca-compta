import pytest
from functional_tests.base import FunctionalTest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from acca_compta.users.models import User


class LoginTest(FunctionalTest):
    def setUp(self):
        self.username = "acca_bordeaux"
        self.user = User.objects.create_user(
            username=self.username,
            password="azerty",  # noqa: S106
        )
        return super().setUp()

    def test_login(self) -> None:
        # User goes to the home page
        self.browser.get(self.live_server_url)

        # Pas de bouton "Journal Comptable"
        with pytest.raises(NoSuchElementException):
            self.browser.find_element(By.LINK_TEXT, "Journal Comptable")

        self.browser.find_element(By.LINK_TEXT, "Connexion").click()
        self.wait_for_page("S'identifier")

        # User enters their username and password
        self.browser.find_element(By.ID, "id_login").send_keys(self.username)
        self.browser.find_element(By.ID, "id_password").send_keys("azerty")

        # User clicks the login button
        self.browser.find_element(By.CLASS_NAME, "btn-primary").click()

        # User is redirected to the home page
        self.wait_for_page("ACCA Compta")

        # User sees login success message
        self.wait_for_message(f"Connexion avec {self.username} réussie.")

        self.browser.find_element(By.LINK_TEXT, "Journal Comptable").click()
        self.wait_for_page("Journal comptable")
