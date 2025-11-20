"""
Глобальный экземпляр конфигурации
"""
from .sources import EnvFileSource
from .parsers import SimpleParser
from .config import Config


def create_global_config():
    """
    Создает и настраивает глобальный экземпляр конфигурации

    Returns:
        Config: Настроенный экземпляр конфигурации
    """
    try:
        source = EnvFileSource()
        parser = SimpleParser()
        return Config(source, parser)
    except Exception as e:
        # Логирование ошибки или fallback на значения по умолчанию
        raise RuntimeError(f"Не удалось создать конфигурацию: {e}")


# Глобальный экземпляр
config = create_global_config()
