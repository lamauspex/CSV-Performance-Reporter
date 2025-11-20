
"""Отладочный скрипт для проверки загрузки конфигурации"""

import os
from pathlib import Path

# Проверяем текущую директорию
print(f"Текущая рабочая директория: {os.getcwd()}")

# Проверяем наличие .env файла
env_path = Path(".env")
print(f"Путь к .env файлу: {env_path.absolute()}")
print(f"Файл .env существует: {env_path.exists()}")

# Пробуем прочитать .env файл напрямую
print("\n=== Прямое чтение .env файла ===")
try:
    with open(".env", "r", encoding="utf-8") as f:
        lines = f.readlines()
    print(f"Прочитано строк: {len(lines)}")
    for i, line in enumerate(lines, 1):
        print(f"Строка {i}: {repr(line)}")
except Exception as e:
    print(f"Ошибка при чтении .env файла: {e}")

# Пробуем использовать EnvFileSource напрямую
print("\n=== Тестирование EnvFileSource ===")
try:
    from src.config.sources import EnvFileSource
    source = EnvFileSource()
    print(f"EnvFileSource создан с файлом: {source.env_file}")
    print(f"Файл существует: {source.env_file.exists()}")

    raw_config = source.load()
    print(f"Загруженная сырая конфигурация: {raw_config}")

except Exception as e:
    print(f"Ошибка при тестировании EnvFileSource: {e}")
    import traceback
    traceback.print_exc()

# Пробуем импортировать конфигурацию
print("\n=== Импорт конфигурации ===")
try:
    from src.config import config
    print(f"Конфигурация успешно импортирована: {config}")

    # Проверяем все загруженные настройки
    all_settings = config.get_all()
    print(f"Все загруженные настройки: {all_settings}")

except Exception as e:
    print(f"Ошибка при импорте конфигурации: {e}")
    import traceback
    traceback.print_exc()
