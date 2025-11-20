"""
Модуль для работы с конфигурацией
Структура разработана с соблюдением принципов SOLID
"""

# Импорты интерфейсов
from .interfaces import ConfigurationSource, ConfigurationParser

# Импорты источников
from .sources import EnvFileSource, EnvironmentSource

# Импорты парсеров
from .parsers import SimpleParser, TypeConverter

# Импорты основного класса
from .config import Config, create_config

# Импорт глобального экземпляра (с обработкой ошибок)
try:
    from .config_instance import config
except ImportError:
    # Fallback если глобальная конфигурация не может быть создана
    config = None

__all__ = [
    'config',
    'Config',
    'ConfigurationSource',
    'ConfigurationParser',
    'EnvFileSource',
    'EnvironmentSource',
    'SimpleParser',
    'TypeConverter',
    'create_config'
]
