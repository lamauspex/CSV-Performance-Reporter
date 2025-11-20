"""
Модуль для обработки CSV файлов
"""
import csv
from typing import List, Dict, Any
import os

from src.config import config
from src.utils.discover import discover_csv_files


class CSVProcessor:
    """Обработчик CSV файлов с данными о сотрудниках"""

    REQUIRED_COLUMNS = [
        'name', 'position', 'completed_tasks',
        'performance', 'skills', 'team', 'experience_years'
    ]

    def __init__(self):
        self.data: List[Dict[str, Any]] = []

    def load_data(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Загружает и объединяет данные из нескольких CSV файлов

        Args:
            file_paths: Список путей к CSV файлам

        Returns:
            Список словарей с данными сотрудников

        Raises:
            FileNotFoundError: Если файл не найден
            ValueError: Если файл имеет некорректную структуру
        """
        all_data: List[Dict[str, Any]] = []

        for file_path in file_paths:
            self._validate_file_exists(file_path)
            file_data = self._load_single_file(file_path)
            all_data.extend(file_data)

        self.data = all_data
        return all_data

    def _validate_file_exists(self, file_path: str) -> None:
        """Проверяет существование файла"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

    def _load_single_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Загружает данные из одного CSV файла

        Args:
            file_path: Путь к CSV файлу

        Returns:
            Список словарей с данными

        Raises:
            ValueError: Если файл имеет некорректную структуру
        """
        data: List[Dict[str, Any]] = []

        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Приводим тип fieldnames к List[str]
            fieldnames = list(reader.fieldnames) if reader.fieldnames else []
            self._validate_columns(fieldnames, file_path)

            for row_num, row in enumerate(reader, start=2):
                processed_row = self._process_row(row, row_num, file_path)
                data.append(processed_row)

        return data

    def _validate_columns(self, columns: List[str], file_path: str) -> None:
        """Проверяет наличие всех обязательных колонок"""
        if not columns:
            raise ValueError(f"Файл {file_path} не содержит заголовков")

        missing_columns = set(self.REQUIRED_COLUMNS) - set(columns)
        if missing_columns:
            raise ValueError(
                f"Файл {file_path} содержит некорректные колонки. "
                f"Отсутствуют: {', '.join(missing_columns)}"
            )

    def discover_and_validate_files(self, folder_path: str) -> List[str]:
        """
        Определяет и валидирует все CSV файлы в указанной папке

        Args:
            folder_path: Путь к папке для поиска CSV файлов

        Returns:
            Список путей к найденным CSV файлам

        Raises:
            FileNotFoundError: Если папка не найдена
            NotADirectoryError: Если путь не является папкой
            PermissionError: Если нет доступа к папке
        """
        # Находим все CSV файлы в папке с учетом конфигурации
        csv_files = discover_csv_files(folder_path)

        # TODO: Здесь можно добавить валидацию структуры CSV файлов:
        # - проверка наличия нужных колонок
        # - валидация формата данных
        # - фильтрация невалидных файлов

        if not csv_files:
            raise ValueError(f"В папке {folder_path} не найдено CSV файлов")

        return csv_files

    def discover_default_folder(self) -> str:
        """
        Автоматически обнаруживает папку с CSV файлами на основе конфигурации

        Returns:
            Путь к папке с CSV файлами

        Raises:
            ValueError: Если папка не найдена или не существует
        """
        from src.utils.discover import discover_default_csv_folder
        return discover_default_csv_folder()

    def _process_row(
            self,
            row: Dict[str, str],
            row_num: int,
            file_path: str) -> Dict[str, Any]:
        """
        Обрабатывает и валидирует одну строку данных

        Args:
            row: Словарь с данными строки
            row_num: Номер строки в файле
            file_path: Путь к файлу

        Returns:
            Обработанный словарь с правильными типами данных

        Raises:
            ValueError: Если данные некорректны
        """
        try:
            return {
                **self._process_string_fields(row),
                **self._process_numeric_fields(row)
            }
        except ValueError as e:
            raise ValueError(
                f"Ошибка в строке {row_num} файла {file_path}: {e}"
            )

    def _process_string_fields(self, row: Dict[str, str]) -> Dict[str, str]:
        """Обрабатывает строковые поля"""
        string_fields = ['name', 'position', 'skills', 'team']
        processed: Dict[str, str] = {}

        for field in string_fields:
            value = row.get(field, '').strip()
            if not value:
                raise ValueError(f"Пустое значение в поле '{field}'")
            processed[field] = value

        return processed

    def _process_numeric_fields(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Обрабатывает числовые поля"""
        processed: Dict[str, Any] = {}

        # completed_tasks
        try:
            completed_tasks = int(row['completed_tasks'])
            if completed_tasks < 0:
                raise ValueError("completed_tasks должно быть неотрицательным")
            processed['completed_tasks'] = completed_tasks
        except (ValueError, KeyError) as e:
            raise ValueError(f"Некорректное значение completed_tasks: {e}")

        # performance
        try:
            performance = float(row['performance'])
            min_perf = float(config.get('MIN_PERFORMANCE'))
            max_perf = float(config.get('MAX_PERFORMANCE'))
            if not (min_perf <= performance <= max_perf):
                raise ValueError(
                    f"performance должно быть в диапазоне от "
                    f"{min_perf} до {max_perf}"
                )
            processed['performance'] = performance
        except (ValueError, KeyError) as e:
            raise ValueError(f"Некорректное значение performance: {e}")

        # experience_years
        try:
            experience_years = int(row['experience_years'])
            min_exp = int(config.get('MIN_EXPERIENCE_YEARS'))
            if experience_years < min_exp:
                raise ValueError(
                    f"experience_years должно быть не меньше {min_exp}"
                )
            processed['experience_years'] = experience_years
        except (ValueError, KeyError) as e:
            raise ValueError(f"Некорректное значение experience_years: {e}")

        return processed
