"""
Основной класс конфигурации
"""

from typing import Any, Dict
from .interfaces import ConfigurationSource, ConfigurationParser
from .sources import EnvFileSource
from .parsers import SimpleParser


class Config:
    """Упрощенный класс управления конфигурацией"""

    def __init__(self,
                 source: ConfigurationSource = None,
                 parser: ConfigurationParser = None):
        self.source = source or EnvFileSource()
        self.parser = parser or SimpleParser()
        self._settings = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Загружает и парсит конфигурацию"""
        raw_config = self.source.load()
        return self.parser.parse(raw_config)

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

    def reload(self):
        """Перезагружает конфигурацию"""
        self._settings = self._load_config()


def create_config(env_file: str = ".env") -> Config:
    """
    Создает конфигурацию с настройками по умолчанию

    Args:
        env_file: Путь к файлу .env

    Returns:
        Экземпляр Config
    """
    source = EnvFileSource(env_file)
    parser = SimpleParser()
    return Config(source, parser)
