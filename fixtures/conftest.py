import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchDriverException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запускать браузер в headless-режиме.",
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


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> webdriver.Chrome:
    is_headless = bool(request.config.getoption("--headless"))
    chrome_driver_path = str(request.config.getoption("--chrome-driver-path")).strip()
    chrome_binary_path = str(request.config.getoption("--chrome-binary-path")).strip()
    strict_driver = bool(request.config.getoption("--strict-driver"))

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
