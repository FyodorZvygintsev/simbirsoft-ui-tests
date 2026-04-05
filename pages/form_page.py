from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from typing import Optional

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.page_factory import PageFactory


class FormPage:
    FORM = (By.ID, "feedbackForm")
    NAME_INPUT = (By.ID, "name-input")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#feedbackForm input[type='password']")
    DRINK_MILK_CHECKBOX = (By.ID, "drink2")
    DRINK_COFFEE_CHECKBOX = (By.ID, "drink3")
    COLOR_YELLOW_RADIO = (By.ID, "color3")
    AUTOMATION_SELECT = (By.ID, "automation")
    EMAIL_INPUT = (By.ID, "email")
    MESSAGE_TEXTAREA = (By.ID, "message")
    SUBMIT_BUTTON = (By.XPATH, "//form[@id='feedbackForm']//button[normalize-space()='Submit']")
    AUTOMATION_TOOLS_ITEMS = (By.CSS_SELECTOR, "#feedbackForm ul li")
    ALERT_EXPECTED_TEXT = "Message received!"

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10) -> None:
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout
        self.page = PageFactory(driver=driver, timeout=timeout)

    def open(self) -> "FormPage":
        self.driver.get(self.base_url)
        return self

    def is_loaded(self) -> bool:
        try:
            return (
                self.page.element(self.NAME_INPUT).is_displayed()
                and self.page.element(self.PASSWORD_INPUT).is_displayed()
                and self.page.element(self.SUBMIT_BUTTON).is_displayed()
            )
        except (NoSuchElementException, TimeoutException):
            return False

    def fill_name(self, value: str) -> "FormPage":
        self.page.type(self.NAME_INPUT, value)
        return self

    def fill_password(self, value: str) -> "FormPage":
        self.page.type(self.PASSWORD_INPUT, value)
        return self

    def select_drink_milk(self) -> "FormPage":
        checkbox = self.page.element(self.DRINK_MILK_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
        return self

    def select_drink_coffee(self) -> "FormPage":
        checkbox = self.page.element(self.DRINK_COFFEE_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
        return self

    def select_drinks_milk_and_coffee(self) -> "FormPage":
        return self.select_drink_milk().select_drink_coffee()

    def select_color_yellow(self) -> "FormPage":
        self.page.click(self.COLOR_YELLOW_RADIO)
        return self

    def select_automation_option(self, value: str = "yes") -> "FormPage":
        self.page.select_by_value(self.AUTOMATION_SELECT, value)
        return self

    def fill_email(self, value: str) -> "FormPage":
        self.page.type(self.EMAIL_INPUT, value)
        return self

    def get_automation_tools(self) -> list[str]:
        return [element.text.strip() for element in self.page.elements(self.AUTOMATION_TOOLS_ITEMS) if element.text.strip()]

    def build_message_from_automation_tools(self) -> str:
        tools = self.get_automation_tools()
        count = len(tools)
        longest = max(tools, key=len) if tools else ""
        return f"Tools count: {count}. Longest tool: {longest}."

    def fill_message(self, value: str) -> "FormPage":
        self.page.type(self.MESSAGE_TEXTAREA, value)
        return self

    def fill_message_from_automation_tools(self) -> "FormPage":
        return self.fill_message(self.build_message_from_automation_tools())

    def submit(self) -> "FormPage":
        self.page.click(self.SUBMIT_BUTTON)
        return self

    def is_alert_present(self, timeout: Optional[int] = None) -> bool:
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(EC.alert_is_present())
            return True
        except TimeoutException:
            return False

    def get_alert_text(self, timeout: Optional[int] = None) -> str:
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            alert = WebDriverWait(self.driver, wait_timeout).until(EC.alert_is_present())
            return alert.text
        except TimeoutException:
            return ""

    def get_name_validation_message(self) -> str:
        return self.page.element(self.NAME_INPUT).get_attribute("validationMessage")

    def accept_alert(self) -> "FormPage":
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass
        return self
