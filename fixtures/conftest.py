import pytest
import allure
from selenium import webdriver
from selenium.common.exceptions import NoSuchDriverException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-ui",
        action="store_true",
        default=False,
        help="Запускать UI-тесты с браузером.",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://practice-automation.com/form-fields/",
        help="Базовый URL для UI-тестов.",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запускать браузер в headless-режиме.",
    )
    parser.addoption(
        "--ui-timeout",
        action="store",
        type=int,
        default=10,
        help="Таймаут WebDriverWait в секундах.",
    )
    parser.addoption(
        "--chrome-driver-path",
        action="store",
        default="",
        help="Путь к chromedriver. Если пусто, используется Selenium Manager.",
    )
    parser.addoption(
        "--chrome-binary-path",
        action="store",
        default="",
        help="Путь к исполняемому файлу Chrome (необязательно).",
    )
    parser.addoption(
        "--strict-driver",
        action="store_true",
        default=False,
        help="Падать с ошибкой, если ChromeDriver недоступен.",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--run-ui"):
        return

    skip_ui = pytest.mark.skip(reason="UI-тесты пропущены по умолчанию. Используй --run-ui для запуска.")
    for item in items:
        if "ui" in item.keywords:
            item.add_marker(skip_ui)


@pytest.fixture(scope="session")
def base_url(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--base-url"))


@pytest.fixture(scope="session")
def ui_timeout(request: pytest.FixtureRequest) -> int:
    return int(request.config.getoption("--ui-timeout"))


@pytest.fixture(scope="session")
def is_headless(request: pytest.FixtureRequest) -> bool:
    return bool(request.config.getoption("--headless"))


@pytest.fixture(scope="function")
def chrome_driver_path(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--chrome-driver-path")).strip()


@pytest.fixture(scope="function")
def chrome_binary_path(request: pytest.FixtureRequest) -> str:
    return str(request.config.getoption("--chrome-binary-path")).strip()


@pytest.fixture(scope="function")
def strict_driver(request: pytest.FixtureRequest) -> bool:
    return bool(request.config.getoption("--strict-driver"))


@pytest.fixture(scope="function")
def driver(
    is_headless: bool,
    chrome_driver_path: str,
    chrome_binary_path: str,
    strict_driver: bool,
) -> webdriver.Chrome:
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--lang=en-US")

    if chrome_binary_path:
        options.binary_location = chrome_binary_path

    if is_headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    service = Service(executable_path=chrome_driver_path) if chrome_driver_path else Service()

    try:
        driver_instance = webdriver.Chrome(service=service, options=options)
    except (NoSuchDriverException, WebDriverException) as exc:
        if strict_driver:
            pytest.fail(
                "Chrome WebDriver недоступен в текущей среде. "
                "Проверь установку браузера/драйвера или передай корректные пути. "
                f"Детали: {exc}"
            )

        pytest.skip(
            "Chrome WebDriver недоступен в текущей среде. "
            "Передай --chrome-driver-path (и при необходимости --chrome-binary-path). "
            f"Детали: {exc}"
        )

    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="function")
def wait(driver: webdriver.Chrome, ui_timeout: int) -> WebDriverWait:
    return WebDriverWait(driver, ui_timeout)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    if "driver" not in item.fixturenames:
        return

    driver_instance = item.funcargs.get("driver")
    if driver_instance is None:
        return

    allure.attach(
        driver_instance.get_screenshot_as_png(),
        name=f"{item.name}_failure",
        attachment_type=allure.attachment_type.PNG,
    )
