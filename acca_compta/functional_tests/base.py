from __future__ import annotations

import time
from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from faker import Faker
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

User = get_user_model()
fake = Faker()


if TYPE_CHECKING:
    from selenium.webdriver.remote.webelement import WebElement

MAX_WAIT = 10


class COOKIE:
    NAME_ATTRIBUTE = "name"
    NAME = "sessionid"
    VALUE_ATTRIBUTE = "value"
    PATH_ATTRIBUTE = "path"
    PATH = "/"


def wait(fn):
    def modified_fn(*args, **kwargs):
        start_time = time.time()
        while True:
            try:
                return fn(*args, **kwargs)
            except AssertionError, WebDriverException:
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    return modified_fn


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        driver_path = "/snap/bin/geckodriver"
        driver_service = webdriver.FirefoxService(executable_path=driver_path)

        options = webdriver.FirefoxOptions()
        options.set_preference("intl.accept_languages", "fr-FR,fr")

        cls.browser = webdriver.Firefox(service=driver_service, options=options)

    @classmethod
    def login(cls) -> None:
        cls.client = Client()
        cls.user = User.objects.create_user(  # pyright: ignore[reportAttributeAccessIssue]
            username="Jean",
            password="testpassword",  # noqa: S106
        )
        cls.client.login(username=cls.user.username, password="testpassword")  # noqa: S106
        cookie = cls.client.cookies[COOKIE.NAME]
        cls.browser.get(cls.live_server_url + "/fake-path")
        cls.browser.add_cookie(
            {
                COOKIE.NAME_ATTRIBUTE: COOKIE.NAME,
                COOKIE.VALUE_ATTRIBUTE: cookie.value,
                COOKIE.PATH_ATTRIBUTE: COOKIE.PATH,
            },
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.quit()
        super().tearDownClass()

    @wait
    def wait_for_page(self, page_title: str) -> None:
        assert page_title in self.browser.title, (
            f"{self.browser.title} is not {page_title}"
        )

    @wait
    def wait_for_message(self, message_content: str) -> None:
        assert (
            message_content
            in self.browser.find_element(By.CLASS_NAME, "toast-body").text
        )

    @wait
    def wait_for_form_next_step(self, step_number: int) -> None:
        assert f"Étape {step_number} sur 5" in self.browser.page_source

    @wait
    def wait_for_click_element(self, element_id: str) -> None:
        self.browser.find_element(By.ID, element_id).click()

    @wait
    def wait_for_element(self, element_id: str) -> WebElement:
        return self.browser.find_element(By.ID, element_id)

    @wait
    def wait_for_element_text(self, element_id: str, element_text: str) -> None:
        assert self.browser.find_element(By.ID, element_id).text == element_text

    @wait
    def wait_for_alert_and_accept(self) -> None:
        self.browser.switch_to.alert.accept()

    @wait
    def wait_for_htmx(self) -> None:
        """Wait until all HTMX requests have completed and the DOM has settled.

        It works by checking HTMX's own CSS classes:
        - .htmx-request - added to the triggering element while the XHR is in flight
        - .htmx-swapping - added to the target during content swap
        - .htmx-settling - added to the target during the settle phase (CSS transitions)

        When none of these classes are present, the HTMX request has fully completed and
        the DOM is stable.
        """
        assert not self.browser.execute_script(
            "return !!document.querySelector('.htmx-request, .htmx-settling, .htmx-swapping')",  # noqa: E501
        )

    def login_as(self, role: str) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            email=fake.email(),
            password="testpassword",  # noqa: S106
        )
        self.client.login(email=self.user.email, password=self.user.email.password)
        cookie = self.client.cookies[COOKIE.NAME]
        self.browser.get(self.live_server_url + "/fake-path")
        self.browser.add_cookie(
            {
                COOKIE.NAME_ATTRIBUTE: COOKIE.NAME,
                COOKIE.VALUE_ATTRIBUTE: cookie.value,
                COOKIE.PATH_ATTRIBUTE: COOKIE.PATH,
            },
        )

    def get_element_value(self, element_id: str):
        return self.browser.find_element(By.ID, element_id).get_attribute(
            "value",
        )

    def _check_if_user_is_logged_in(self) -> None:
        assert self.browser.find_element(By.ID, "logout_button_id")

    def select_element(self, select_id: str, visible_text: str) -> None:
        """Select an option from a dropdown and trigger the change event for HTMX.

        This is useful when the select element has hx-trigger="change" attribute.
        Selenium's Select doesn't automatically fire JavaScript events.
        """
        select_element = self.browser.find_element(By.ID, select_id)
        select = Select(select_element)
        select.select_by_visible_text(visible_text)
        self.browser.execute_script(
            "arguments[0].dispatchEvent(new Event('change'));",
            select_element,
        )
