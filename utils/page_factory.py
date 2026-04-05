from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class PageFactory:
    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def element(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def elements(self, locator: tuple[str, str]) -> list[WebElement]:
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def type(self, locator: tuple[str, str], value: str) -> None:
        element = self.element(locator)
        element.clear()
        element.send_keys(value)

    def click(self, locator: tuple[str, str]) -> None:
        self.clickable(locator).click()

    def select_by_value(self, locator: tuple[str, str], value: str) -> None:
        select = Select(self.element(locator))
        select.select_by_value(value)
