from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from tests.settings import (
    SELENIUM_DRIVER_URL,
    LOCAL_TEST_URL,
    TEST_USER_NAME,
    TEST_USER_PASSWORD,
)

ADMIN_TEST_URL = f"{LOCAL_TEST_URL}/admin"


class TestForms:
    """Main class to test any form. Specifically the admin for currently."""

    def setup_method(self):
        self.driver = webdriver.Remote(
            command_executor=SELENIUM_DRIVER_URL,
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        self.driver.implicitly_wait(1)
        self.driver.get(ADMIN_TEST_URL)

    def teardown_method(self):
        self.driver.close()
        self.driver.quit()

    def test_admin_form_empty(self) -> None:
        """Empty login form should reject login."""
        login_button = self.driver.find_element_by_css_selector("input[type='submit']")
        login_button.click()
        self.driver.get(ADMIN_TEST_URL)

        login_button = self.driver.find_element_by_css_selector("input[type='submit']")
        assert login_button.get_attribute("value") == "Log in"

    def test_admin_form_staff_success(self) -> None:
        username_field = self.driver.find_element_by_id("id_username")
        username_field.send_keys(TEST_USER_NAME)

        password_field = self.driver.find_element_by_id("id_password")
        password_field.send_keys(TEST_USER_PASSWORD)

        login_button = self.driver.find_element_by_css_selector("input[type='submit']")
        login_button.click()
        self.driver.implicitly_wait(0.3)
        admin_message = (
            self.driver.find_element_by_id("content-main")
            .find_element_by_tag_name("p")
            .text
        )
        assert admin_message == "You don’t have permission to view or edit anything."
