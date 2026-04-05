import pytest
import allure

from pages.form_page import FormPage


@pytest.mark.ui
@allure.title("Позитивный: успешная отправка формы")
def test_submit_form_positive(driver) -> None:
    with allure.step("Открыть страницу формы"):
        page = FormPage(driver=driver).open()

    with allure.step("Проверить, что форма загружена"):
        assert page.is_loaded()

    with allure.step("Заполнить форму по основному сценарию"):
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
        assert page.get_alert_text() == FormPage.ALERT_EXPECTED_TEXT
        page.accept_alert()


@pytest.mark.ui
@allure.title("Негативный: отправка с пустым Name")
def test_submit_form_negative_empty_name(driver) -> None:
    with allure.step("Открыть страницу формы"):
        page = FormPage(driver=driver).open()

    with allure.step("Проверить, что форма загружена"):
        assert page.is_loaded()

    with allure.step("Заполнить форму без поля Name и нажать Submit"):
        (
            page.fill_password("StrongPass123!")
            .select_drinks_milk_and_coffee()
            .select_color_yellow()
            .select_automation_option("yes")
            .fill_email("name@example.com")
            .fill_message_from_automation_tools()
            .submit()
        )

    with allure.step("Проверить, что alert не появился и браузер вернул валидационное сообщение"):
        assert not page.is_alert_present(timeout=2)
        assert page.get_name_validation_message() != ""
