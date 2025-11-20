"""
Unit-тесты для DataService
"""
import pytest
from unittest.mock import patch
from typing import List, Dict, Any

from src.services.data_service import DataService
from src.interfaces.data_loader import DataLoaderInterface


class MockDataLoader(DataLoaderInterface):
    """Mock-реализация DataLoaderInterface для тестирования"""

    def __init__(self, data_to_return: List[Dict[str, Any]]):
        self.data_to_return = data_to_return
        self.load_from_files_calls = []
        self.load_from_folder_calls = []

    def load_from_files(self, file_paths: List[str]) -> List[Dict[str, Any]]:
        self.load_from_files_calls.append(file_paths)
        return self.data_to_return

    def load_from_folder(self, folder_path: str) -> List[Dict[str, Any]]:
        self.load_from_folder_calls.append(folder_path)
        return self.data_to_return


class TestDataService:
    """Тесты для класса DataService"""

    def test_init_with_data_loader(self):
        """Тест инициализации с загрузчиком данных"""
        mock_loader = MockDataLoader([])
        service = DataService(mock_loader)

        assert service._data_loader is mock_loader

    def test_load_data_from_files_success(self):
        """Тест успешной загрузки данных из файлов"""
        # Подготавливаем тестовые данные
        test_data = [
            {
                'name': 'John Doe',
                'position': 'Developer',
                'completed_tasks': 25,
                'performance': 4.5,
                'skills': 'Python, Django',
                'team': 'Backend Team',
                'experience_years': 3
            },
            {
                'name': 'Jane Smith',
                'position': 'Designer',
                'completed_tasks': 30,
                'performance': 4.2,
                'skills': 'Figma, Sketch',
                'team': 'Design Team',
                'experience_years': 2
            }
        ]

        mock_loader = MockDataLoader(test_data)
        service = DataService(mock_loader)

        # Загружаем данные из файлов
        file_paths = ['data/employees1.csv', 'data/employees2.csv']
        result = service.load_data(file_paths=file_paths)

        # Проверяем результат
        assert result == test_data
        assert len(result) == 2

        # Проверяем, что метод был вызван с правильными параметрами
        assert mock_loader.load_from_files_calls == [file_paths]
        assert len(mock_loader.load_from_folder_calls) == 0

    def test_load_data_from_folder_success(self):
        """Тест успешной загрузки данных из папки"""
        # Подготавливаем тестовые данные
        test_data = [
            {
                'name': 'Bob Johnson',
                'position': 'QA Engineer',
                'completed_tasks': 20,
                'performance': 3.8,
                'skills': 'Selenium, Python',
                'team': 'QA Team',
                'experience_years': 4
            }
        ]

        mock_loader = MockDataLoader(test_data)
        service = DataService(mock_loader)

        # Загружаем данные из папки
        folder_path = '/path/to/csv/folder'
        result = service.load_data(folder_path=folder_path)

        # Проверяем результат
        assert result == test_data
        assert len(result) == 1

        # Проверяем, что метод был вызван с правильными параметрами
        assert mock_loader.load_from_folder_calls == [folder_path]
        assert len(mock_loader.load_from_files_calls) == 0

    def test_load_data_no_files_or_folder_raises_error(self):
        """Тест ошибки при отсутствии файлов и папки"""
        mock_loader = MockDataLoader([])
        service = DataService(mock_loader)

        with pytest.raises(
            ValueError,
            match="Необходимо указать файлы или папку"
        ):
            service.load_data()

    def test_file_validation_success(self):
        """Тест успешной валидации файлов"""
        mock_loader = MockDataLoader([])
        service = DataService(mock_loader)

        # Создаем временные файлы для тестирования
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file:

            mock_exists.return_value = True
            mock_is_file.return_value = True

            # Валидация должна пройти без ошибок
            service._validate_files(['existing_file.csv', 'another_file.csv'])

            # Проверяем, что методы были вызваны правильное количество раз
            assert mock_exists.call_count == 2
            assert mock_is_file.call_count == 2

    def test_file_validation_nonexistent_file_raises_error(self):
        """Тест ошибки валидации для несуществующего файла"""
        mock_loader = MockDataLoader([])
        service = DataService(mock_loader)

        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False

            with pytest.raises(FileNotFoundError, match="Файл не найден"):
                service._validate_files(['nonexistent_file.csv'])

    def test_file_validation_directory_raises_error(self):
        """Тест ошибки валидации для директории вместо файла"""
        mock_loader = MockDataLoader([])
        service = DataService(mock_loader)

        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file:

            mock_exists.return_value = True
            mock_is_file.return_value = False

            with pytest.raises(ValueError, match="Путь не является файлом"):
                service._validate_files(['some_directory'])

    def test_file_validation_non_csv_extension_raises_error(self):
        """Тест ошибки валидации для файла не с расширением .csv"""
        mock_loader = MockDataLoader([])
        service = DataService(mock_loader)

        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file:

            mock_exists.return_value = True
            mock_is_file.return_value = True

            with pytest.raises(ValueError, match="Файл должен иметь расширение .csv"):
                service._validate_files(['document.txt'])

    def test_file_validation_case_insensitive_csv_extension(self):
        """Тест валидации CSV расширения с разным регистром"""
        mock_loader = MockDataLoader([])
        service = DataService(mock_loader)

        with patch('pathlib.Path.exists') as mock_exists, \
                patch('pathlib.Path.is_file') as mock_is_file:

            mock_exists.return_value = True
            mock_is_file.return_value = True

            # Валидация должна пройти для .CSV, .csv, .Csv
            service._validate_files(['file1.CSV', 'file2.csv', 'file3.Csv'])

            # Проверяем, что все файлы прошли валидацию
            assert mock_exists.call_count == 3
            assert mock_is_file.call_count == 3

    def test_dependency_injection(self):
        """Тест инверсии зависимостей"""
        # Создаем mock-загрузчик
        mock_loader = MockDataLoader([{'test': 'data'}])

        # Создаем сервис
        service = DataService(mock_loader)

        # Проверяем, что зависимость правильно внедрена
        assert service._data_loader is mock_loader

        # Проверяем, что сервис может использовать загрузчик
        result = service.load_data(file_paths=['data\\employees1.csv'])
        assert result == [{'test': 'data'}]

    def test_service_isolation(self):
        """Тест изоляции сервиса"""
        # Создаем два разных загрузчика
        loader1_data = [{'id': 1, 'name': 'First'}]
        loader2_data = [{'id': 2, 'name': 'Second'}]

        loader1 = MockDataLoader(loader1_data)
        loader2 = MockDataLoader(loader2_data)

        service1 = DataService(loader1)
        service2 = DataService(loader2)

        # Проверяем, что сервисы изолированы
        result1 = service1.load_data(file_paths=['data/employees1.csv'])
        result2 = service2.load_data(file_paths=['data\\employees2.csv'])

        assert result1 == loader1_data
        assert result2 == loader2_data
        assert result1 != result2
