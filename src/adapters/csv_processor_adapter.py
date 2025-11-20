"""
Адаптер для CSVProcessor
"""
from typing import List, Dict, Any
from src.interfaces.data_loader import DataLoaderInterface
from src.csv_processor import CSVProcessor


class CSVProcessorAdapter(DataLoaderInterface):
    """Адаптер для CSVProcessor, реализующий DataLoaderInterface"""

    def __init__(self):
        self._processor = CSVProcessor()

    def load_from_files(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """Реализация загрузки из файлов"""
        return self._processor.load_data(file_paths)

    def load_from_folder(self, folder_path: str) -> List[Dict[str, Any]]:
        """Реализация загрузки из папки"""
        csv_files = self._processor.discover_and_validate_files(folder_path)
        return self._processor.load_data(csv_files)
