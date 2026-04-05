# UI-автотесты формы Practice Automation

Проект UI-автоматизации для формы:
https://practice-automation.com/form-fields/

## Стек
- Python 3.10
- pytest
- Selenium WebDriver (Chrome)
- Allure
- GitHub Actions

## Установка
```bash
py -3.10 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Запуск тестов
Быстрый запуск без UI (`ui`-тесты отфильтрованы через marker):
```bash
python -m pytest
```

Запуск только UI-тестов:
```bash
python -m pytest -m ui
```

Запуск UI-тестов в headless-режиме:
```bash
python -m pytest -m ui --headless
```

Строгий режим (ошибка при недоступном драйвере):
```bash
python -m pytest -m ui --headless --strict-driver
```

Запуск с локальным chromedriver:
```bash
python -m pytest -m ui --chrome-driver-path "C:\tools\chromedriver.exe"
```

Запуск с локальными путями к chromedriver и Chrome:
```bash
python -m pytest -m ui --chrome-driver-path "C:\tools\chromedriver.exe" --chrome-binary-path "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

## Allure
Локальная генерация:
```bash
python -m pytest -m ui --headless --alluredir=allure-results
allure serve allure-results
```

## CI
В репозитории добавлен workflow:
`.github/workflows/ui-tests.yml`

Что делает pipeline:
- запускает UI-тесты в headless режиме;
- включает строгий режим драйвера (`--strict-driver`);
- сохраняет `allure-results` как artifact;
- публикует Allure-отчет в отдельную ветку `gh-pages`.

## Структура проекта
```text
project/
+-- .github/
|   L-- workflows/
|       L-- ui-tests.yml
+-- fixtures/
+-- pages/
+-- tests/
+-- utils/
+-- requirements.txt
+-- pytest.ini
+-- README.md
L-- .gitignore
```

## Тест-кейсы
### Позитивный тест-кейс
Название: `test_submit_form_positive`

Шаги:
1. Открыть страницу формы.
2. Заполнить `Name`.
3. Заполнить `Password`.
4. Выбрать `Milk` и `Coffee`.
5. Выбрать цвет `Yellow`.
6. Выбрать любой вариант в `Do you like automation?`.
7. Ввести `name@example.com` в поле Email.
8. В Message записать:
количество инструментов в блоке `Automation tools` и инструмент с самым длинным названием.
9. Нажать `Submit`.

Ожидаемый результат:
появляется alert с текстом `Message received!`.

### Негативный тест-кейс
Название: `test_submit_form_negative_empty_name`

Шаги:
1. Открыть страницу формы.
2. Не заполнять обязательное поле `Name`.
3. Заполнить остальные поля.
4. Нажать `Submit`.

Ожидаемый результат:
- alert не появляется;
- браузер показывает встроенное сообщение валидации для поля `Name`.
