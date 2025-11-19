"""
Тесты для ReportGenerator
"""
import pytest
from src.report_generator import ReportGenerator, PerformanceReport
from src.config import config


class TestPerformanceReport:
    """Тесты для класса PerformanceReport"""

    def test_generate_performance_report(self):
        """Тест генерации отчета по эффективности"""
        report = PerformanceReport()

        # Используем реальные тестовые данные
        test_file = config.get('test_data_file')
        from src.csv_processor import CSVProcessor

        processor = CSVProcessor()
        data = processor.load_data([test_file])

        result = report.generate(data)

        # Проверяем, что результат содержит заголовки
        assert 'Позиция' in result
        assert 'Средняя эффективность' in result
        assert 'Количество сотрудников' in result

        # Проверяем, что отчет содержит данные из тестового файла
        assert 'Backend Developer' in result
        assert 'Frontend Developer' in result
        assert 'Data Scientist' in result
        assert 'DevOps Engineer' in result
        assert 'QA Engineer' in result
        assert 'Fullstack Developer' in result

    def test_empty_data(self):
        """Тест генерации отчета с пустыми данными"""
        report = PerformanceReport()

        result = report.generate([])

        # Должна быть создана пустая таблица
        assert 'Позиция' in result
        assert 'Средняя эффективность' in result

    def test_config_sorting(self):
        """Тест сортировки согласно конфигурации"""
        report = PerformanceReport()

        # Создаем тестовые данные
        data = [
            {
                'name': 'User1',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.5,
                'skills': 'Python',
                'team': 'Team',
                'experience_years': 2
            },
            {
                'name': 'User2',
                'position': 'Designer',
                'completed_tasks': 10,
                'performance': 4.8,
                'skills': 'Figma',
                'team': 'Team',
                'experience_years': 2
            }
        ]

        result = report.generate(data)

        # Проверяем, что Designer (4.8) идет перед Developer (4.5)
        lines = result.split('\n')
        designer_line_idx = None
        developer_line_idx = None

        for i, line in enumerate(lines):
            if 'Designer' in line:
                designer_line_idx = i
            if 'Developer' in line:
                developer_line_idx = i

        assert designer_line_idx is not None
        assert developer_line_idx is not None
        assert designer_line_idx < developer_line_idx


class TestReportGenerator:
    """Тесты для класса ReportGenerator"""

    def test_generate_supported_report(self):
        """Тест генерации поддерживаемого отчета"""
        generator = ReportGenerator()

        test_file = config.get('test_data_file')
        from src.csv_processor import CSVProcessor

        processor = CSVProcessor()
        data = processor.load_data([test_file])

        result = generator.generate_report('performance', data)

        assert 'performance' in result.lower() or 'эффективность' in result.lower()
        assert 'Backend Developer' in result

    def test_generate_unsupported_report(self):
        """Тест генерации неподдерживаемого отчета"""
        generator = ReportGenerator()

        # Используем минимальные тестовые данные
        data = [
            {
                'name': 'Test User',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.5,
                'skills': 'Python',
                'team': 'Team',
                'experience_years': 2
            }
        ]

        with pytest.raises(ValueError, match="Неподдерживаемый тип отчета"):
            generator.generate_report('unsupported_report', data)

    def test_multiple_positions_same_performance(self):
        """Тест обработки позиций с одинаковой эффективностью"""
        report = PerformanceReport()

        data = [
            {
                'name': 'User1',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.5,
                'skills': 'Python',
                'team': 'Team',
                'experience_years': 2
            },
            {
                'name': 'User2',
                'position': 'Designer',
                'completed_tasks': 10,
                'performance': 4.5,
                'skills': 'Figma',
                'team': 'Team',
                'experience_years': 2
            }
        ]

        result = report.generate(data)

        # Обе позиции должны быть в отчете
        assert 'Developer' in result
        assert 'Designer' in result

        # Должны иметь одинаковую среднюю эффективность
        lines = result.split('\n')
        developer_line = [line for line in lines if 'Developer' in line][0]
        designer_line = [line for line in lines if 'Designer' in line][0]

        # Проверяем, что обе строки содержат 4.5
        assert '4.5' in developer_line
        assert '4.5' in designer_line
