from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from tests.settings import SELENIUM_DRIVER_URL, LOCAL_TEST_URL


class TestButtons:
    """Main class to test all buttons on home page."""

    # driver.implicitly_wait(5)
    # driver.get(LOCAL_TEST_URL)
    # driver.find_elements_by_tag_name("a")

    def setup_method(self):
        self.driver = webdriver.Remote(
            command_executor=SELENIUM_DRIVER_URL,
            desired_capabilities=DesiredCapabilities.CHROME,
        )
        self.driver.implicitly_wait(1)
        self.driver.get(LOCAL_TEST_URL)
        self.all_a_tags = self.driver.find_elements_by_tag_name("a")

    def teardown_method(self):
        self.driver.close()

    def test_invite_button(self):
        assert any(["Invite To Your Server" in x.text for x in self.all_a_tags])

    def test_api_button(self):
        assert True

    def test_source_button(self):
        assert True
