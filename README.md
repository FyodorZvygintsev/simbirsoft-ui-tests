# UI-автотесты формы Practice Automation

Проект UI-автоматизации для формы: https://practice-automation.com/form-fields/

## Технологии
- Python 3.10
- pytest
- Selenium WebDriver (Chrome)
- Allure

## Установка
```bash
py -3.10 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Запуск тестов
```bash
python -m pytest
```

## Запуск UI-тестов (Chrome)
```bash
python -m pytest --run-ui
```

## Запуск UI-тестов в headless-режиме
```bash
python -m pytest --run-ui --headless
```

## Запуск UI-тестов с локальным chromedriver
```bash
python -m pytest --run-ui --chrome-driver-path "C:\tools\chromedriver.exe"
```

## Запуск UI-тестов с локальными путями к chromedriver и Chrome
```bash
python -m pytest --run-ui --chrome-driver-path "C:\tools\chromedriver.exe" --chrome-binary-path "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

## Запуск Allure
```bash
python -m pytest --alluredir=allure-results
allure serve allure-results
```

## Структура проекта
```text
project/
+-- tests/
+-- pages/
+-- locators/
+-- fixtures/
+-- utils/
+-- requirements.txt
+-- pytest.ini
+-- .gitignore
L-- README.md
```

## Тест-кейсы
### Позитивный тест-кейс
- Будет добавлен в следующих шагах.

### Негативный тест-кейс
- Будет добавлен в следующих шагах.
