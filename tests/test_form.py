"""
Тесты формы обратной связи на https://practice-automation.com/form-fields/

Содержит:
- Smoke-тест: проверка открытия страницы
- Позитивный тест: успешная отправка формы с корректными данными
- Негативный тест: отправка формы без обязательного поля Name
"""

import allure
import pytest

from pages.form_page import FormPage


@pytest.mark.smoke
@allure.title("Smoke: страница формы открывается и загружается")
def test_form_page_opens(driver, base_url: str) -> None:
    """Проверяем, что страница формы доступна и ключевые элементы отображаются."""
    page = FormPage(driver=driver, base_url=base_url).open()

    assert "practice-automation.com/form-fields/" in driver.current_url, (
        "URL не содержит ожидаемый путь"
    )
    assert page.is_loaded(), "Форма не загрузилась - ключевые элементы не найдены"


@pytest.mark.regression
@allure.title("Позитивный: успешная отправка формы со всеми полями")
def test_submit_form_positive(driver, base_url: str) -> None:
    """
    Позитивный сценарий: заполняем все поля формы корректными данными,
    отправляем и проверяем, что появляется alert 'Message received!'.
    """
    with allure.step("Открыть страницу формы"):
        page = FormPage(driver=driver, base_url=base_url).open()

    with allure.step("Проверить, что форма загружена"):
        assert page.is_loaded(), "Форма не загрузилась"

    with allure.step("Заполнить все поля формы и отправить"):
        (
            page.fill_name("Test User")
            .fill_password("StrongPass123!")
            .select_drinks_milk_and_coffee()
            .select_color_yellow()
            .select_automation_option("yes")
            .fill_email("name@example.com")
            .fill_message_from_automation_tools()
            .submit()
        )

    with allure.step("Проверить текст alert"):
        assert page.get_alert_text() == FormPage.ALERT_EXPECTED_TEXT, (
            "Alert с текстом 'Message received!' не появился"
        )
        page.accept_alert()


@pytest.mark.regression
@allure.title("Негативный: отправка формы с пустым полем Name")
def test_submit_form_negative_empty_name(driver, base_url: str) -> None:
    """
    Негативный сценарий: не заполняем обязательное поле Name.
    Ожидаем, что форма не отправится и браузер покажет валидационное сообщение.
    """
    with allure.step("Открыть страницу формы"):
        page = FormPage(driver=driver, base_url=base_url).open()

    with allure.step("Проверить, что форма загружена"):
        assert page.is_loaded(), "Форма не загрузилась"

    with allure.step("Заполнить форму БЕЗ поля Name и нажать Submit"):
        (
            page.fill_password("StrongPass123!")
            .select_drinks_milk_and_coffee()
            .select_color_yellow()
            .select_automation_option("yes")
            .fill_email("name@example.com")
            .fill_message_from_automation_tools()
            .submit()
        )

    with allure.step("Проверить, что alert НЕ появился"):
        assert not page.is_alert_present(timeout=2), (
            "Alert не должен появляться при пустом Name"
        )

    with allure.step("Проверить валидационное сообщение браузера"):
        validation_msg = page.get_name_validation_message()
        assert validation_msg != "", (
            "Браузер должен показать сообщение валидации для пустого поля Name"
        )
