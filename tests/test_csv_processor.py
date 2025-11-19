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

    def test_discover_and_validate_files_success(self):
        """Тест успешного обнаружения и валидации CSV файлов"""
        processor = CSVProcessor()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем валидный CSV файл
            valid_csv = os.path.join(temp_dir, "valid_data.csv")
            csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Test User,Developer,10,4.5,"Python, Django",Test Team,2
"""

            with open(valid_csv, 'w') as f:
                f.write(csv_content)

            # Создаем не-CSV файл (должен быть проигнорирован)
            txt_file = os.path.join(temp_dir, "readme.txt")
            with open(txt_file, 'w') as f:
                f.write("This is not a CSV file")

            # Тестируем обнаружение и валидацию
            result = processor.discover_and_validate_files(temp_dir)

            assert len(result) == 1
            assert valid_csv in result
            assert txt_file not in result

    def test_discover_and_validate_files_empty_folder(self):
        """Тест с пустой папкой"""
        processor = CSVProcessor()

        with tempfile.TemporaryDirectory() as temp_dir:
            with pytest.raises(
                ValueError,
                match="В папке .* не найдено CSV файлов"
            ):
                processor.discover_and_validate_files(temp_dir)

    def test_discover_and_validate_files_folder_not_found(self):
        """Тест с несуществующей папкой"""
        processor = CSVProcessor()

        with pytest.raises(FileNotFoundError, match="Папка не найдена"):
            processor.discover_and_validate_files("/nonexistent/folder")

    def test_discover_and_validate_files_path_not_directory(self):
        """Тест когда путь не является папкой"""
        processor = CSVProcessor()

        with tempfile.NamedTemporaryFile() as tmp_file:
            with pytest.raises(
                NotADirectoryError,
                match="Путь не является папкой"
            ):
                processor.discover_and_validate_files(tmp_file.name)

    def test_discover_and_validate_files_with_subdirectories(self):
        """Тест обнаружения файлов в подпапках"""
        processor = CSVProcessor()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем подпапку
            subfolder = os.path.join(temp_dir, "subfolder")
            os.makedirs(subfolder)

            # Создаем файлы в разных местах
            root_file = os.path.join(temp_dir, "root.csv")
            sub_file = os.path.join(subfolder, "sub.csv")

            csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Test User,Developer,10,4.5,"Python",Test Team,2
"""

            for file_path in [root_file, sub_file]:
                with open(file_path, 'w') as f:
                    f.write(csv_content)

            # Тестируем обнаружение
            result = processor.discover_and_validate_files(temp_dir)

            assert len(result) == 2
            assert root_file in result
            assert sub_file in result

    def test_discover_and_validate_files_invalid_csv(self):
        """Тест с невалидным CSV файлом"""
        processor = CSVProcessor()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем невалидный CSV файл
            invalid_csv = os.path.join(temp_dir, "invalid.csv")
            csv_content = """name,position,invalid_column
Test User,Developer,10
"""

            with open(invalid_csv, 'w') as f:
                f.write(csv_content)

            # discover_and_validate_files не должен
            # валидировать содержимое файлов,
            # только обнаруживать их. Валидация происходит при load_data.
            result = processor.discover_and_validate_files(temp_dir)

            assert len(result) == 1
            assert invalid_csv in result

    def test_discover_and_validate_files_mixed_files(self):
        """Тест с смешанными типами файлов"""
        processor = CSVProcessor()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем различные файлы
            csv_file = os.path.join(temp_dir, "data.csv")
            txt_file = os.path.join(temp_dir, "readme.txt")
            pdf_file = os.path.join(temp_dir, "document.pdf")
            xlsx_file = os.path.join(temp_dir, "data.xlsx")

            # Создаем только CSV файл с содержимым
            csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Test User,Developer,10,4.5,"Python",Test Team,2
"""

            with open(csv_file, 'w') as f:
                f.write(csv_content)

            # Создаем остальные файлы как пустые
            for file_path in [txt_file, pdf_file, xlsx_file]:
                with open(file_path, 'w') as f:
                    f.write("not a csv")

            result = processor.discover_and_validate_files(temp_dir)

            # Только CSV файл должен быть найден
            assert len(result) == 1
            assert csv_file in result
            assert txt_file not in result
            assert pdf_file not in result
            assert xlsx_file not in result
