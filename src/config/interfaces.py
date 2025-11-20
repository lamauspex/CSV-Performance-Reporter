"""
Интерфейсы для системы конфигурации
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class ConfigurationSource(ABC):
    """Интерфейс для источников конфигурации"""

    @abstractmethod
    def load(self) -> Dict[str, str]:
        """Загружает конфигурацию из источника"""
        pass


class ConfigurationParser(ABC):
    """Интерфейс для парсинга конфигурации"""

    @abstractmethod
    def parse(self, raw_config: Dict[str, str]) -> Dict[str, Any]:
        """Парсит сырую конфигурацию в типизированную"""
        pass
