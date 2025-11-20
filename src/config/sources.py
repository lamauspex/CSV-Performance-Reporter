"""
Источники конфигурации
"""

import os
from pathlib import Path
from typing import Dict

from .interfaces import ConfigurationSource


class EnvFileSource(ConfigurationSource):
    """Загрузка конфигурации из .env файла"""

    def __init__(self, env_file: str = ".env"):
        self.env_file = Path(env_file)

    def load(self) -> Dict[str, str]:
        """Загружает переменные из .env файла"""
        if not self.env_file.exists():
            return {}

        config = {}
        with open(self.env_file, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
        return config


class EnvironmentSource(ConfigurationSource):
    """Загрузка конфигурации из переменных окружения"""

    def load(self) -> Dict[str, str]:
        return dict(os.environ)
