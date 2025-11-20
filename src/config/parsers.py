"""
Парсеры конфигурации
"""

from typing import Any, Dict
from .interfaces import ConfigurationParser


class TypeConverter:
    """Статические методы преобразования типов"""

    @staticmethod
    def to_float(value: str) -> float:
        """Преобразует строку в число с плавающей точкой"""
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def to_int(value: str) -> int:
        """Преобразует строку в целое число"""
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def to_bool(value: str) -> bool:
        """Преобразует строку в булево значение"""
        return value.lower() in ('true', '1', 'yes', 'on')


class SimpleParser(ConfigurationParser):
    """Простой парсер конфигурации"""

    def __init__(self):

        self.type_converters = {
            'DEFAULT_REPORT_TYPE': str,
            'DEMO_DATA_FILE': str,
            'TEST_DATA_FILE': str,
            'TABLE_FORMAT': str,
            'MAX_OUTPUT_WIDTH': TypeConverter.to_int,
            'MIN_PERFORMANCE': TypeConverter.to_float,
            'MAX_PERFORMANCE': TypeConverter.to_float,
            'MIN_EXPERIENCE_YEARS': TypeConverter.to_int,
            'SORT_BY_PERFORMANCE': TypeConverter.to_bool,
            'SORT_ORDER': str,
            'TEST_COVERAGE_THRESHOLD': TypeConverter.to_int,
            # Дополнительные ключи для совместимости
            'SKILLS_REPORT_MIN_OCCURRENCE': TypeConverter.to_int,
            # Ключи для SkillsReport
            'SKILLS_REPORT_SHOW_RARE': TypeConverter.to_bool,
            'SKILLS_REPORT_CALCULATE_RARITY': TypeConverter.to_bool,
            # Ключи для автообнаружения
            'AUTO_DISCOVER_CSV_FOLDER': TypeConverter.to_bool,
            'CSV_FOLDER_PATH': str,
            'INCLUDE_SUBFOLDERS': TypeConverter.to_bool,
            'AUTO_DISCOVER_FOLDER': TypeConverter.to_bool,
        }

    def parse(self, raw_config: Dict[str, str]) -> Dict[str, Any]:
        """Парсит сырую конфигурацию"""
        parsed = {}
        for key, converter in self.type_converters.items():
            value = raw_config.get(key)
            if value is not None:
                parsed[key] = converter(value) if callable(
                    converter) else converter
        return parsed
