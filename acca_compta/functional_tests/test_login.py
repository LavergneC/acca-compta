from functional_tests.base import FunctionalTest
from functional_tests.constants import MESSAGES
from selenium.webdriver.common.by import By
from unycapp.users.tests.factories import create_user


class LoginTest(FunctionalTest):
    def setUp(self):
        self.user = create_user(password="testpass")  # noqa: S106
        return super().setUp()

    def test_login(self) -> None:
        # User goes to the login page
        self.browser.get(self.live_server_url + "/accounts/login")

        # User enters their username and password
        self.browser.find_element(By.NAME, "login").send_keys(self.user.email)
        self.browser.find_element(By.NAME, "password").send_keys("testpass")

        # User clicks the login button
        self.browser.find_element(By.XPATH, "//button[contains(.,'Connexion')]").click()

        # User is redirected to the user detail page
        self.wait_for_page(str(self.user.name))

        # User sees login success message
        self.wait_for_message(MESSAGES.LOGIN_SUCCESS.format(user=str(self.user)))

        # User is logged in
        self._check_if_user_is_logged_in()
