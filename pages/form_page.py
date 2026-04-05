"""
Page Object для страницы формы https://practice-automation.com/form-fields/

Реализует паттерны:
- Page Object Model - инкапсуляция логики взаимодействия со страницей
- Fluent Interface - методы возвращают self для цепочки вызовов
"""

from typing import Optional

from selenium.common.exceptions import (
    NoAlertPresentException,
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.page_factory import PageFactory


class FormPage:
    """Page Object для формы обратной связи на practice-automation.com."""

    # --- Локаторы элементов ---
    # Используем разные типы селекторов: ID, CSS, XPath (по требованию задания)

    # Поиск по ID - самый быстрый и надёжный способ
    FORM = (By.ID, "feedbackForm")
    NAME_INPUT = (By.ID, "name-input")
    DRINK_MILK_CHECKBOX = (By.ID, "drink2")
    DRINK_COFFEE_CHECKBOX = (By.ID, "drink3")
    COLOR_YELLOW_RADIO = (By.ID, "color3")
    AUTOMATION_SELECT = (By.ID, "automation")
    EMAIL_INPUT = (By.ID, "email")
    MESSAGE_TEXTAREA = (By.ID, "message")

    # Поиск по CSS-селектору - когда нужен более гибкий поиск
    PASSWORD_INPUT = (By.CSS_SELECTOR, "#feedbackForm input[type='password']")
    AUTOMATION_TOOLS_ITEMS = (By.CSS_SELECTOR, "#feedbackForm ul li")

    # Поиск по XPath - для сложных условий (здесь: кнопка по тексту внутри формы)
    SUBMIT_BUTTON = (
        By.XPATH,
        "//form[@id='feedbackForm']//button[normalize-space()='Submit']",
    )

    # Ожидаемый текст алерта после успешной отправки формы
    ALERT_EXPECTED_TEXT = "Message received!"

    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10) -> None:
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout
        # PageFactory обеспечивает автоматическое ожидание элементов
        self.page = PageFactory(driver=driver, timeout=timeout)

    # --- Методы навигации ---

    def open(self) -> "FormPage":
        """Открыть страницу формы в браузере."""
        self.driver.get(self.base_url)
        return self

    def is_loaded(self) -> bool:
        """Проверить, что ключевые элементы формы отображаются."""
        try:
            return (
                self.page.element(self.NAME_INPUT).is_displayed()
                and self.page.element(self.PASSWORD_INPUT).is_displayed()
                and self.page.element(self.SUBMIT_BUTTON).is_displayed()
            )
        except (NoSuchElementException, TimeoutException):
            return False

    # --- Методы заполнения полей (Fluent Interface - возвращают self) ---

    def fill_name(self, value: str) -> "FormPage":
        """Заполнить поле Name."""
        self.page.type(self.NAME_INPUT, value)
        return self

    def fill_password(self, value: str) -> "FormPage":
        """Заполнить поле Password."""
        self.page.type(self.PASSWORD_INPUT, value)
        return self

    def select_drink_milk(self) -> "FormPage":
        """Выбрать чекбокс Milk (если ещё не выбран)."""
        checkbox = self.page.element(self.DRINK_MILK_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
        return self

    def select_drink_coffee(self) -> "FormPage":
        """Выбрать чекбокс Coffee (если ещё не выбран)."""
        checkbox = self.page.element(self.DRINK_COFFEE_CHECKBOX)
        if not checkbox.is_selected():
            checkbox.click()
        return self

    def select_drinks_milk_and_coffee(self) -> "FormPage":
        """Выбрать оба напитка: Milk и Coffee."""
        return self.select_drink_milk().select_drink_coffee()

    def select_color_yellow(self) -> "FormPage":
        """Выбрать радиокнопку Yellow."""
        self.page.click(self.COLOR_YELLOW_RADIO)
        return self

    def select_automation_option(self, value: str = "yes") -> "FormPage":
        """Выбрать вариант в выпадающем списке 'Do you like automation?'."""
        self.page.select_by_value(self.AUTOMATION_SELECT, value)
        return self

    def fill_email(self, value: str) -> "FormPage":
        """Заполнить поле Email."""
        self.page.type(self.EMAIL_INPUT, value)
        return self

    # --- Работа с блоком Automation Tools ---

    def get_automation_tools(self) -> list[str]:
        """Получить список инструментов из блока Automation Tools на странице."""
        return [
            element.text.strip()
            for element in self.page.elements(self.AUTOMATION_TOOLS_ITEMS)
            if element.text.strip()
        ]

    def build_message_from_automation_tools(self) -> str:
        """
        Сформировать сообщение для поля Message:
        - количество инструментов в списке Automation Tools
        - инструмент с самым длинным названием
        """
        tools = self.get_automation_tools()
        count = len(tools)
        longest = max(tools, key=len) if tools else ""
        return f"Tools count: {count}. Longest tool: {longest}."

    def fill_message(self, value: str) -> "FormPage":
        """Заполнить поле Message произвольным текстом."""
        self.page.type(self.MESSAGE_TEXTAREA, value)
        return self

    def fill_message_from_automation_tools(self) -> "FormPage":
        """Заполнить поле Message данными из блока Automation Tools."""
        return self.fill_message(self.build_message_from_automation_tools())

    # --- Отправка формы ---

    def submit(self) -> "FormPage":
        """Нажать кнопку Submit."""
        self.page.click(self.SUBMIT_BUTTON)
        return self

    # --- Работа с alert ---

    def is_alert_present(self, timeout: Optional[int] = None) -> bool:
        """Проверить, появился ли alert в течение заданного таймаута."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            WebDriverWait(self.driver, wait_timeout).until(EC.alert_is_present())
            return True
        except TimeoutException:
            return False

    def get_alert_text(self, timeout: Optional[int] = None) -> str:
        """Получить текст alert (пустая строка, если alert не появился)."""
        wait_timeout = timeout if timeout is not None else self.timeout
        try:
            alert = WebDriverWait(self.driver, wait_timeout).until(EC.alert_is_present())
            return alert.text
        except TimeoutException:
            return ""

    def accept_alert(self) -> "FormPage":
        """Закрыть alert нажатием OK."""
        try:
            self.driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass
        return self

    # --- Валидация ---

    def get_name_validation_message(self) -> str:
        """Получить сообщение валидации браузера для поля Name."""
        return self.page.element(self.NAME_INPUT).get_attribute("validationMessage")
