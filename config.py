"""
Модуль конфигурации проекта.
Загружает настройки из .env файла и предоставляет их остальным модулям.
"""

import os

from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Базовый URL тестируемого приложения
BASE_URL: str = os.getenv("BASE_URL", "https://practice-automation.com/form-fields/")

# Запуск браузера без GUI (для CI/CD)
HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"

# Таймаут ожидания элементов (секунды)
TIMEOUT: int = int(os.getenv("TIMEOUT", "10"))
