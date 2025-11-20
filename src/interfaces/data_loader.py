"""
Интерфейс для загрузки и обработки данных
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class DataLoaderInterface(ABC):
    """Интерфейс для загрузчиков данных"""

    @abstractmethod
    def load_from_files(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Загружает данные из списка файлов

        Args:
            file_paths: Список путей к файлам

        Returns:
            Список словарей с данными
        """
        pass

    @abstractmethod
    def load_from_folder(self, folder_path: str) -> List[Dict[str, Any]]:
        """
        Загружает данные из всех файлов в папке

        Args:
            folder_path: Путь к папке

        Returns:
            Список словарей с данными
        """
        pass
