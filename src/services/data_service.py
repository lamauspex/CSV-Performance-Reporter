"""
Сервис для работы с данными
"""
from typing import List, Dict, Any
from pathlib import Path

from src.interfaces.data_loader import DataLoaderInterface


class DataService:
    """Сервис для загрузки и валидации данных"""

    def __init__(self, data_loader: DataLoaderInterface):
        """
        Инициализация сервиса

        Args:
            data_loader: Загрузчик данных (инверсия зависимостей)
        """
        self._data_loader = data_loader

    def load_data(self,
                  file_paths: List[str] = None,
                  folder_path: str = None) -> List[Dict[str, Any]]:
        """
        Загружает данные из файлов или папки

        Args:
            file_paths: Список путей к файлам
            folder_path: Путь к папке

        Returns:
            Список словарей с данными

        Raises:
            ValueError: Если не указаны файлы или папка
        """
        if folder_path:
            return self._data_loader.load_from_folder(folder_path)
        elif file_paths:
            self._validate_files(file_paths)
            return self._data_loader.load_from_files(file_paths)
        else:
            raise ValueError(
                "Необходимо указать файлы или папку для загрузки данных")

    def _validate_files(self, file_paths: List[str]) -> None:
        """
        Валидирует существование файлов

        Args:
            file_paths: Список путей к файлам

        Raises:
            FileNotFoundError: Если файл не найден
            ValueError: Если путь не является файлом
        """
        for file_path in file_paths:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            if not path.is_file():
                raise ValueError(f"Путь не является файлом: {file_path}")
            if not file_path.lower().endswith('.csv'):
                raise ValueError(
                    f"Файл должен иметь расширение .csv: {file_path}")
