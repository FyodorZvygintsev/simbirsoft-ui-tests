import pytest
import allure

from pages.form_page import FormPage


@pytest.mark.ui
@allure.title("Smoke: страница формы открывается")
def test_form_page_is_opened(driver, base_url: str) -> None:
    page = FormPage(driver=driver, base_url=base_url).open()
    assert "practice-automation.com/form-fields/" in driver.current_url
    assert page.is_loaded()
