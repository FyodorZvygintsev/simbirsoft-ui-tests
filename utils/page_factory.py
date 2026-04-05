"""
Реализация паттерна Page Factory для Python/Selenium.

В Java Selenium есть встроенный PageFactory с аннотациями @FindBy.
В Python аналога нет, поэтому реализуем через обёртку над WebDriverWait,
которая обеспечивает автоматическое ожидание элементов перед взаимодействием.
"""

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class PageFactory:
    """
    Фабрика для работы с элементами страницы.
    Все методы используют явные ожидания (Explicit Waits),
    что делает тесты стабильнее по сравнению с обычным find_element.
    """

    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def element(self, locator: tuple[str, str]) -> WebElement:
        """Найти элемент, дождавшись его видимости на странице."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def elements(self, locator: tuple[str, str]) -> list[WebElement]:
        """Найти все элементы по локатору (ждём появления хотя бы одного)."""
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def clickable(self, locator: tuple[str, str]) -> WebElement:
        """Найти элемент, дождавшись его кликабельности."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def type(self, locator: tuple[str, str], value: str) -> None:
        """Очистить поле и ввести текст."""
        element = self.element(locator)
        element.clear()
        element.send_keys(value)

    def click(self, locator: tuple[str, str]) -> None:
        """
        Клик по элементу с обработкой типичных проблем:
        1. Скролл к элементу (он может быть за пределами видимой области)
        2. Повторная попытка при перехвате клика другим элементом
        3. JS-клик как запасной вариант
        """
        element = self.clickable(locator)
        # Скроллим к элементу, чтобы он был в зоне видимости
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
            element,
        )

        # Пробуем кликнуть дважды - иногда элемент перекрыт анимацией или overlay
        for _ in range(2):
            try:
                self.clickable(locator).click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException):
                element = self.clickable(locator)
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                    element,
                )

        # Если обычный клик не сработал - используем JavaScript
        self.driver.execute_script("arguments[0].click();", self.clickable(locator))

    def select_by_value(self, locator: tuple[str, str], value: str) -> None:
        """Выбрать значение в выпадающем списке <select> по атрибуту value."""
        select = Select(self.element(locator))
        select.select_by_value(value)
