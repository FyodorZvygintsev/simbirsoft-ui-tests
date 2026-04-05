import pytest


@pytest.mark.ui
def test_form_page_is_opened(driver, base_url: str) -> None:
    driver.get(base_url)
    assert "practice-automation.com/form-fields/" in driver.current_url
