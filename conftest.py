"""
Главный conftest.py - точка входа для всех фикстур и хуков pytest.
Здесь настраиваем браузер, ожидания и интеграцию с Allure.
"""

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from config import BASE_URL, HEADLESS, TIMEOUT


# --- Хуки pytest ---

def pytest_addoption(parser: pytest.Parser) -> None:
    """Добавляем CLI-опцию для headless-режима (удобно переключать в CI)."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=HEADLESS,
        help="Запуск браузера в headless-режиме (без окна).",
    )


# --- Фикстуры ---

@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> webdriver.Chrome:
    """
    Фикстура инициализации Chrome WebDriver.
    Создаёт новый экземпляр браузера для каждого теста,
    после завершения теста - закрывает браузер.
    """
    options = Options()
    # Разворачиваем окно на весь экран
    options.add_argument("--start-maximized")
    # Отключаем всплывающие уведомления браузера
    options.add_argument("--disable-notifications")

    # Headless-режим: браузер работает без GUI (нужен для CI/CD)
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


@pytest.fixture(scope="function")
def wait(driver: webdriver.Chrome) -> WebDriverWait:
    """Фикстура явного ожидания - используется для проверки элементов."""
    return WebDriverWait(driver, TIMEOUT)


@pytest.fixture()
def base_url() -> str:
    """Базовый URL приложения, загруженный из .env."""
    return BASE_URL


# --- Хуки Allure ---

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    """
    Хук для автоматического скриншота при падении теста.
    Скриншот прикрепляется к Allure-отчёту для удобства анализа.
    """
    outcome = yield
    report = outcome.get_result()

    # Скриншот делаем только при падении на этапе выполнения теста
    if report.when == "call" and report.failed:
        driver_instance = item.funcargs.get("driver")
        if driver_instance:
            allure.attach(
                driver_instance.get_screenshot_as_png(),
                name=f"screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )
