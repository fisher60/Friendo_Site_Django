from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from tests.settings import SELENIUM_DRIVER_URL, LOCAL_TEST_URL


class TestButtons:
    """Main class to test all buttons on home page."""

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
        self.driver.quit()

    def text_in_a_tag(self, text: str) -> bool:
        return any([text in x.text for x in self.all_a_tags])

    def test_invite_button(self) -> None:
        test_text = "Invite To Your Server"
        assert self.text_in_a_tag(test_text)

    def test_api_button(self) -> None:
        test_text = "API"
        assert self.text_in_a_tag(test_text)

    def test_source_button(self) -> None:
        test_text = "Source"
        assert self.text_in_a_tag(test_text)
