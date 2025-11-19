"""
Тесты для CSVProcessor
"""
import pytest
import tempfile
import os

from src.csv_processor import CSVProcessor
from src.config import config


class TestCSVProcessor:
    """Тесты для класса CSVProcessor"""

    def test_load_single_file_success(self):
        """Тест успешной загрузки одного файла"""
        processor = CSVProcessor()

        # Используем реальный тестовый файл
        test_file = config.get('test_data_file')
        data = processor.load_data([test_file])

        assert len(data) > 0
        assert data[0]['name'] == 'Reznik Kirill'
        assert data[0]['position'] == 'Backend Developer'
        assert data[0]['performance'] == 4.8
        assert data[0]['completed_tasks'] == 31
        assert data[0]['experience_years'] == 5

    def test_load_multiple_files(self):
        """Тест загрузки нескольких файлов"""
        processor = CSVProcessor()

        # Используем оба файла данных
        demo_file = config.get('demo_data_file')
        test_file = config.get('test_data_file')

        data = processor.load_data([demo_file, test_file])

        # Проверяем, что загружены данные из обоих файлов
        assert len(data) > 0

        # Проверяем наличие данных из первого файла
        david_found = any(employee['name'] ==
                          'David Chen' for employee in data)
        assert david_found

        # Проверяем наличие данных из второго файла
        alex_found = any(employee['name'] ==
                         'Alex Ivanov' for employee in data)
        assert alex_found

    def test_file_not_found(self):
        """Тест обработки отсутствующего файла"""
        processor = CSVProcessor()

        with pytest.raises(FileNotFoundError):
            processor.load_data(['nonexistent_file.csv'])

    def test_invalid_columns(self):
        """Тест обработки файла с неправильными колонками"""
        processor = CSVProcessor()

        csv_content = """name,position,invalid_column
David Chen,Mobile Developer,36"""

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False
        ) as f:
            f.write(csv_content)
            temp_file = f.name

        try:
            with pytest.raises(ValueError, match="некорректные колонки"):
                processor.load_data([temp_file])
        finally:
            os.unlink(temp_file)

    def test_invalid_performance_value(self):
        """Тест обработки некорректного значения performance"""
        processor = CSVProcessor()

        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
David Chen,Mobile Developer,36,invalid,"Swift, Kotlin",Mobile Team,3
"""

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False
        ) as f:
            f.write(csv_content)
            temp_file = f.name

        try:
            with pytest.raises(
                ValueError,
                match="Некорректное значение performance"
            ):
                processor.load_data([temp_file])
        finally:
            os.unlink(temp_file)

    def test_performance_out_of_range(self):
        """Тест обработки значения performance вне диапазона"""
        processor = CSVProcessor()

        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
David Chen,Mobile Developer,36,10.0,"Swift, Kotlin",Mobile Team,3
"""

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False
        ) as f:
            f.write(csv_content)
            temp_file = f.name

        try:
            with pytest.raises(
                ValueError,
                match="performance должно быть в диапазоне"
            ):
                processor.load_data([temp_file])
        finally:
            os.unlink(temp_file)

    def test_empty_required_field(self):
        """Тест обработки пустого обязательного поля"""
        processor = CSVProcessor()

        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
,Mobile Developer,36,4.6,"Swift, Kotlin",Mobile Team,3
"""

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False
        ) as f:
            f.write(csv_content)
            temp_file = f.name

        try:
            with pytest.raises(
                ValueError,
                match="Пустое значение в поле"
            ):
                processor.load_data([temp_file])
        finally:
            os.unlink(temp_file)

    def test_config_validation_ranges(self):
        """Тест использования конфигурационных значений для валидации"""
        processor = CSVProcessor()

        # Тест с значением в допустимом диапазоне из конфигурации
        csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Test User,Developer,10,2.5,"Python",Team,1
"""

        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.csv',
            delete=False
        ) as f:
            f.write(csv_content)
            temp_file = f.name

        try:
            data = processor.load_data([temp_file])
            assert len(data) == 1
            assert data[0]['performance'] == 2.5
        finally:
            os.unlink(temp_file)
