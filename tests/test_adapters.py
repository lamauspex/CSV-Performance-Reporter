"""
Unit-тесты для адаптеров
"""
import pytest
import tempfile
import os
from unittest.mock import patch

from src.adapters.csv_processor_adapter import CSVProcessorAdapter
from src.adapters.report_generator_adapter import ReportGeneratorAdapter
from src.csv_processor import CSVProcessor
from src.report_generator import ReportGenerator
from src.config import config


class TestCSVProcessorAdapter:
    """Тесты для класса CSVProcessorAdapter"""

    def test_init_creates_csv_processor(self):
        """Тест инициализации адаптера"""
        adapter = CSVProcessorAdapter()

        # Проверяем, что адаптер создал CSVProcessor
        assert hasattr(adapter, '_processor')
        assert isinstance(adapter._processor, CSVProcessor)

    def test_load_from_files_success(self):
        """Тест успешной загрузки данных из файлов"""
        adapter = CSVProcessorAdapter()

        # Используем реальный тестовый файл
        test_file = config.get('TEST_DATA_FILE')

        # Загружаем данные
        result = adapter.load_from_files([test_file])

        # Проверяем результат
        assert len(result) > 0
        assert result[0]['name'] == 'Reznik Kirill'
        assert result[0]['position'] == 'Backend Developer'
        assert result[0]['performance'] == 4.8
        assert result[0]['completed_tasks'] == 31
        assert result[0]['experience_years'] == 5

    def test_load_from_files_multiple_files(self):
        """Тест загрузки данных из нескольких файлов"""
        adapter = CSVProcessorAdapter()

        # Используем оба тестовых файла
        demo_file = config.get('DEMO_DATA_FILE')
        test_file = config.get('TEST_DATA_FILE')

        # Загружаем данные из обоих файлов
        result = adapter.load_from_files([demo_file, test_file])

        # Проверяем, что загружены данные из обоих файлов
        assert len(result) > 0

        # Проверяем наличие данных из первого файла
        david_found = any(employee['name'] ==
                          'David Chen' for employee in result)
        assert david_found

        # Проверяем наличие данных из второго файла
        alex_found = any(employee['name'] ==
                         'Alex Ivanov' for employee in result)
        assert alex_found

    def test_load_from_folder_success(self):
        """Тест успешной загрузки данных из папки"""
        adapter = CSVProcessorAdapter()

        # Создаем временную папку с CSV файлами
        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем валидный CSV файл
            csv_file = os.path.join(temp_dir, "test_data.csv")
            csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Test User,Developer,15,4.2,"Python, Django",Test Team,3
Another User,Designer,20,3.8,"Figma, Sketch",Design Team,2
"""

            with open(csv_file, 'w') as f:
                f.write(csv_content)

            # Загружаем данные из папки
            result = adapter.load_from_folder(temp_dir)

            # Проверяем результат
            assert len(result) == 2

            # Проверяем данные первого сотрудника
            test_user = next(
                (emp for emp in result if emp['name'] == 'Test User'), None)
            assert test_user is not None
            assert test_user['position'] == 'Developer'
            assert test_user['performance'] == 4.2

            # Проверяем данные второго сотрудника
            another_user = next(
                (emp for emp in result if emp['name'] == 'Another User'), None)
            assert another_user is not None
            assert another_user['position'] == 'Designer'
            assert another_user['performance'] == 3.8

    def test_load_from_folder_empty_folder_raises_error(self):
        """Тест ошибки при загрузке из пустой папки"""
        adapter = CSVProcessorAdapter()

        with tempfile.TemporaryDirectory() as temp_dir:
            # Папка существует, но CSV файлов нет
            with pytest.raises(ValueError, match="В папке .* не найдено CSV файлов"):
                adapter.load_from_folder(temp_dir)

    def test_load_from_folder_nonexistent_folder_raises_error(self):
        """Тест ошибки при загрузке из несуществующей папки"""
        adapter = CSVProcessorAdapter()

        with pytest.raises(FileNotFoundError, match="Папка не найдена"):
            adapter.load_from_folder('/nonexistent/folder')

    def test_load_from_files_file_not_found_raises_error(self):
        """Тест ошибки при загрузке несуществующего файла"""
        adapter = CSVProcessorAdapter()

        with pytest.raises(FileNotFoundError, match="Файл не найден"):
            adapter.load_from_files(['nonexistent_file.csv'])

    def test_load_from_files_invalid_csv_raises_error(self):
        """Тест ошибки при загрузке некорректного CSV файла"""
        adapter = CSVProcessorAdapter()

        # Создаем некорректный CSV файл
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,position,invalid_column\nTest User,Developer,invalid")
            temp_file = f.name

        try:
            with pytest.raises(ValueError, match="некорректные колонки"):
                adapter.load_from_files([temp_file])
        finally:
            os.unlink(temp_file)

    def test_adapter_delegates_to_csv_processor(self):
        """Тест делегирования вызовов к CSVProcessor"""
        # Создаем spy на CSVProcessor
        with patch('src.adapters.csv_processor_adapter.CSVProcessor') as mock_processor_class:
            mock_processor = mock_processor_class.return_value
            mock_processor.load_data.return_value = [{'test': 'data'}]
            mock_processor.discover_and_validate_files.return_value = [
                'file1.csv', 'file2.csv']

            adapter = CSVProcessorAdapter()

            # Тест load_from_files
            result = adapter.load_from_files(['file1.csv', 'file2.csv'])
            assert result == [{'test': 'data'}]
            mock_processor.load_data.assert_called_once_with(
                ['file1.csv', 'file2.csv'])

            # Сбрасываем mock
            mock_processor.reset_mock()

            # Тест load_from_folder
            result = adapter.load_from_folder('/test/folder')
            assert result == [{'test': 'data'}]
            mock_processor.discover_and_validate_files.assert_called_once_with(
                '/test/folder')
            mock_processor.load_data.assert_called_once_with(
                ['file1.csv', 'file2.csv'])

    def test_adapter_preserves_csv_processor_behavior(self):
        """Тест сохранения поведения CSVProcessor в адаптере"""
        adapter = CSVProcessorAdapter()

        # Создаем временный CSV файл с данными на границе допустимых значений
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            csv_content = """name,position,completed_tasks,performance,skills,team,experience_years
Boundary User,Developer,0,0.0,"Python",Team,0
"""
            f.write(csv_content)
            temp_file = f.name

        try:
            # Загружаем данные с граничными значениями
            result = adapter.load_from_files([temp_file])

            # Проверяем, что данные загружены корректно
            assert len(result) == 1
            assert result[0]['name'] == 'Boundary User'
            assert result[0]['completed_tasks'] == 0
            assert result[0]['performance'] == 0.0
            assert result[0]['experience_years'] == 0

        finally:
            os.unlink(temp_file)


class TestReportGeneratorAdapter:
    """Тесты для класса ReportGeneratorAdapter"""

    def test_init_creates_report_generator(self):
        """Тест инициализации адаптера"""
        adapter = ReportGeneratorAdapter()

        # Проверяем, что адаптер создал ReportGenerator
        assert hasattr(adapter, '_generator')
        assert isinstance(adapter._generator, ReportGenerator)

    def test_generate_report_success(self):
        """Тест успешной генерации отчета"""
        adapter = ReportGeneratorAdapter()

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
            }
        ]

        # Генерируем отчет по эффективности
        result = adapter.generate_report('performance', test_data)

        # Проверяем результат
        assert 'Позиция' in result
        assert 'Средняя эффективность' in result
        assert 'Developer' in result
        assert 'John Doe' in result

    def test_generate_skills_report_success(self):
        """Тест успешной генерации отчета по навыкам"""
        adapter = ReportGeneratorAdapter()

        # Подготавливаем тестовые данные
        test_data = [
            {
                'name': 'Jane Smith',
                'position': 'Designer',
                'completed_tasks': 30,
                'performance': 4.2,
                'skills': 'Figma, Sketch, Adobe XD',
                'team': 'Design Team',
                'experience_years': 2
            }
        ]

        # Генерируем отчет по навыкам
        result = adapter.generate_report('skills', test_data)

        # Проверяем результат
        assert 'ОТЧЕТ ПО НАВЫКАМ СОТРУДНИКОВ' in result
        assert 'Figma' in result
        assert 'Sketch' in result
        assert 'Jane Smith' in result

    def test_generate_report_unsupported_type_raises_error(self):
        """Тест ошибки при генерации неподдерживаемого типа отчета"""
        adapter = ReportGeneratorAdapter()

        test_data = [
            {
                'name': 'Test User',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.0,
                'skills': 'Python',
                'team': 'Team',
                'experience_years': 2
            }
        ]

        with pytest.raises(ValueError, match="Неподдерживаемый тип отчета"):
            adapter.generate_report('unsupported_report', test_data)

    def test_generate_report_with_empty_data(self):
        """Тест генерации отчета с пустыми данными"""
        adapter = ReportGeneratorAdapter()

        # Генерируем отчет по эффективности с пустыми данными
        result = adapter.generate_report('performance', [])

        # Должна быть создана пустая таблица
        assert 'Позиция' in result
        assert 'Средняя эффективность' in result

    def test_generate_skills_report_with_empty_data(self):
        """Тест генерации отчета по навыкам с пустыми данными"""
        adapter = ReportGeneratorAdapter()

        # Генерируем отчет по навыкам с пустыми данными
        result = adapter.generate_report('skills', [])

        # Должен быть создан отчет для пустых данных
        assert 'Нет данных для анализа навыков' in result

    def test_adapter_delegates_to_report_generator(self):
        """Тест делегирования вызовов к ReportGenerator"""
        # Создаем spy на ReportGenerator
        with patch('src.adapters.report_generator_adapter.ReportGenerator') as mock_generator_class:
            mock_generator = mock_generator_class.return_value
            mock_generator.generate_report.return_value = "Mock Report"

            adapter = ReportGeneratorAdapter()

            # Тест генерации отчета
            test_data = [{'name': 'Test', 'performance': 4.5}]
            result = adapter.generate_report('performance', test_data)

            assert result == "Mock Report"
            mock_generator.generate_report.assert_called_once_with(
                'performance', test_data)

    def test_adapter_preserves_report_generator_behavior(self):
        """Тест сохранения поведения ReportGenerator в адаптере"""
        adapter = ReportGeneratorAdapter()

        # Используем реальный тестовый файл для проверки поведения
        test_file = config.get('TEST_DATA_FILE')
        from src.csv_processor import CSVProcessor

        processor = CSVProcessor()
        data = processor.load_data([test_file])

        # Генерируем отчет
        result = adapter.generate_report('performance', data)

        # Проверяем, что отчет содержит ожидаемые данные из тестового файла
        assert 'Backend Developer' in result
        assert 'Frontend Developer' in result
        assert 'Reznik Kirill' in result

    def test_multiple_report_generation(self):
        """Тест множественной генерации отчетов"""
        adapter = ReportGeneratorAdapter()

        # Подготавливаем тестовые данные
        test_data = [
            {
                'name': 'User1',
                'position': 'Developer',
                'completed_tasks': 20,
                'performance': 4.5,
                'skills': 'Python',
                'team': 'Team',
                'experience_years': 3
            },
            {
                'name': 'User2',
                'position': 'Designer',
                'completed_tasks': 25,
                'performance': 4.0,
                'skills': 'Figma',
                'team': 'Team',
                'experience_years': 2
            }
        ]

        # Генерируем несколько отчетов
        performance_result = adapter.generate_report('performance', test_data)
        skills_result = adapter.generate_report('skills', test_data)

        # Проверяем результаты
        assert 'Developer' in performance_result
        assert 'Designer' in performance_result
        assert 'Python' in skills_result
        assert 'Figma' in skills_result
        assert 'User1' in performance_result
        assert 'User2' in skills_result

    def test_report_generation_with_large_dataset(self):
        """Тест генерации отчета с большим набором данных"""
        adapter = ReportGeneratorAdapter()

        # Создаем большой набор данных
        large_data = [
            {
                'name': f'Employee{i}',
                'position': 'Developer',
                'completed_tasks': 20 + i,
                'performance': 3.0 + (i % 20) * 0.1,
                'skills': f'Skill{i % 5}',
                'team': 'Team',
                'experience_years': 1 + (i % 10)
            }
            for i in range(100)
        ]

        # Генерируем отчет
        result = adapter.generate_report('performance', large_data)

        # Проверяем, что отчет сгенерирован корректно
        assert 'Позиция' in result
        assert 'Средняя эффективность' in result
        assert 'Developer' in result

        # Проверяем, что отчет содержит данные (хотя бы одну строку с данными)
        lines = result.split('\n')
        data_lines = [line for line in lines if 'Employee' in line]
        assert len(data_lines) > 0
