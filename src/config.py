"""
Модуль для работы с конфигурацией
"""
import os
from typing import Any, Dict
from pathlib import Path


class Config:
    """Класс для управления конфигурацией приложения"""

    def __init__(self, env_file: str = ".env"):

        self.env_file = Path(env_file)
        self._load_env_file()
        self._settings = self._load_settings()

    def _load_env_file(self):
        """Загружает переменные из .env файла"""
        if not self.env_file.exists():
            return

        with open(self.env_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

    def _load_settings(self) -> Dict[str, Any]:
        """Загружает настройки из переменных окружения"""
        def to_float(value: str) -> float:
            """Преобразует строку в число с плавающей точкой"""
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0

        def to_int(value: str) -> int:
            """Преобразует строку в целое число"""
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0

        def to_bool(value: str) -> bool:
            """Преобразует строку в булево значение"""
            return value.lower() in ('true', '1', 'yes', 'on')

        return {
            'default_report_type': os.getenv('DEFAULT_REPORT_TYPE'),
            'demo_data_file': os.getenv('DEMO_DATA_FILE'),
            'test_data_file': os.getenv('TEST_DATA_FILE'),
            'table_format': os.getenv('TABLE_FORMAT'),
            'max_output_width': to_int(os.getenv('MAX_OUTPUT_WIDTH')),
            'min_performance': to_float(os.getenv('MIN_PERFORMANCE')),
            'max_performance': to_float(os.getenv('MAX_PERFORMANCE')),
            'min_experience_years': to_int(os.getenv('MIN_EXPERIENCE_YEARS')),
            'sort_by_performance': to_bool(os.getenv('SORT_BY_PERFORMANCE')),
            'sort_order': os.getenv('SORT_ORDER'),
            'test_coverage_threshold': to_int(os.getenv('TEST_COVERAGE_THRESHOLD'))
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        Получает значение настройки

        Args:
            key: Ключ настройки
            default: Значение по умолчанию

        Returns:
            Значение настройки
        """
        return self._settings.get(key, default)

    def get_all(self) -> Dict[str, Any]:
        """
        Получает все настройки

        Returns:
            Словарь со всеми настройками
        """
        return self._settings.copy()


# Глобальный экземпляр конфигурации
config = Config()
