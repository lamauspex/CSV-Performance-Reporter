"""
Тесты для ReportGenerator
"""
import pytest

from src.report_generator import (
    ReportGenerator, PerformanceReport, SkillsReport)
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


class TestSkillsReport:
    """Тесты для класса SkillsReport"""

    def test_generate_skills_report(self):
        """Тест генерации отчета по навыкам"""
        report = SkillsReport()

        # Используем реальные тестовые данные
        test_file = config.get('test_data_file')
        from src.csv_processor import CSVProcessor

        processor = CSVProcessor()
        data = processor.load_data([test_file])

        result = report.generate(data)

        # Проверяем заголовки отчета
        assert 'ОТЧЕТ ПО НАВЫКАМ СОТРУДНИКОВ' in result
        assert 'Навык' in result
        assert 'Кол-во сотрудников' in result
        assert 'Ср. эффективность' in result
        assert 'Сотрудники' in result

        # Проверяем наличие данных из тестового файла
        assert 'Python' in result  # Навык из Alex Ivanov
        assert 'Alex Ivanov' in result
        assert 'Maria Petrova' in result
        assert 'John Smith' in result

    def test_skills_report_empty_data(self):
        """Тест генерации отчета по навыкам с пустыми данными"""
        report = SkillsReport()

        result = report.generate([])

        # Должен быть создан отчет для пустых данных
        assert 'Нет данных для анализа навыков' in result

    def test_skills_parsing(self):
        """Тест парсинга навыков из строки"""
        report = SkillsReport()

        # Тест корректного парсинга
        skills_string = "Python, Django, PostgreSQL, Docker"
        result = report._parse_skills_string(skills_string)
        expected = ['Python', 'Django', 'PostgreSQL', 'Docker']
        assert result == expected

        # Тест с лишними пробелами
        skills_string = " Python , Django , PostgreSQL "
        result = report._parse_skills_string(skills_string)
        expected = ['Python', 'Django', 'PostgreSQL']
        assert result == expected

        # Тест с пустой строкой
        result = report._parse_skills_string("")
        expected = []
        assert result == expected

        # Тест с None
        result = report._parse_skills_string(None)
        expected = []
        assert result == expected

    def test_skills_distribution_analysis(self):
        """Тест анализа распределения навыков"""
        report = SkillsReport()

        # Создаем тестовые данные
        data = [
            {
                'name': 'User1',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.5,
                'skills': 'Python, Django',
                'team': 'Team',
                'experience_years': 2
            },
            {
                'name': 'User2',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.8,
                'skills': 'Python, Flask',
                'team': 'Team',
                'experience_years': 2
            },
            {
                'name': 'User3',
                'position': 'Designer',
                'completed_tasks': 10,
                'performance': 4.0,
                'skills': 'Figma, Sketch',
                'team': 'Team',
                'experience_years': 2
            }
        ]

        # Парсим данные
        parsed_data = report._parse_skills_from_data(data)

        # Анализируем распределение навыков
        skills_stats = report._analyze_skills_distribution(parsed_data)

        # Проверяем результаты
        assert len(skills_stats) > 0

        # Python должен быть самым популярным (2 сотрудника >= MIN_OCCURRENCE)
        python_stats = next(
            (s for s in skills_stats if s['skill'] == 'Python'), None)
        assert python_stats is not None
        assert python_stats['employee_count'] == 2
        assert python_stats['avg_performance'] == 4.65  # (4.5 + 4.8) / 2

        # Flask должен быть (1 сотрудник, но MIN_OCCURRENCE=2, поэтому не попадает)
        # Этот тест проверяет, что редкие навыки фильтруются согласно конфигурации
        flask_stats = next(
            (s for s in skills_stats if s['skill'] == 'Flask'), None)
        assert flask_stats is None  # Flask встречается только у 1 сотрудника

        # Figma должен быть (1 сотрудник, но MIN_OCCURRENCE=2, поэтому не попадает)
        figma_stats = next(
            (s for s in skills_stats if s['skill'] == 'Figma'), None)
        assert figma_stats is None  # Figma встречается только у 1 сотрудника

    def test_employees_skills_analysis(self):
        """Тест анализа сотрудников по навыкам"""
        report = SkillsReport()

        # Создаем тестовые данные
        data = [
            {
                'name': 'User1',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.5,
                'skills': 'Python, Django, Flask',
                'team': 'Team',
                'experience_years': 2
            },
            {
                'name': 'User2',
                'position': 'Designer',
                'completed_tasks': 10,
                'performance': 4.0,
                'skills': 'Figma',
                'team': 'Team',
                'experience_years': 2
            }
        ]

        # Парсим данные
        parsed_data = report._parse_skills_from_data(data)

        # Анализируем сотрудников по навыкам
        employees_stats = report._analyze_employees_skills(parsed_data)

        # Проверяем результаты
        assert len(employees_stats) == 2

        # User1 должен быть первым (больше навыков)
        assert employees_stats[0]['name'] == 'User1'
        assert employees_stats[0]['skills_count'] == 3
        assert employees_stats[0]['skills'] == ['Python', 'Django', 'Flask']

        # User2 должен быть вторым
        assert employees_stats[1]['name'] == 'User2'
        assert employees_stats[1]['skills_count'] == 1
        assert employees_stats[1]['skills'] == ['Figma']

    def test_skills_report_min_occurrence_config(self):
        """Тест конфигурации минимального количества сотрудников для навыка"""
        report = SkillsReport()

        # Создаем данные с редкими навыками
        data = [
            {
                'name': 'User1',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.5,
                'skills': 'Python, Django',
                'team': 'Team',
                'experience_years': 2
            },
            {
                'name': 'User2',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.8,
                'skills': 'Python, Flask',
                'team': 'Team',
                'experience_years': 2
            },
            {
                'name': 'User3',
                'position': 'Designer',
                'completed_tasks': 10,
                'performance': 4.0,
                'skills': 'RareSkill',
                'team': 'Team',
                'experience_years': 2
            }
        ]

        # Парсим данные
        parsed_data = report._parse_skills_from_data(data)

        # Анализируем с минимальным количеством 2
        skills_stats = report._analyze_skills_distribution(parsed_data)

        # Python должен быть (2 сотрудника >= 2)
        python_stats = next(
            (s for s in skills_stats if s['skill'] == 'Python'), None)
        assert python_stats is not None

        # RareSkill не должен быть (1 сотрудник < 2)
        rare_stats = next(
            (s for s in skills_stats if s['skill'] == 'RareSkill'), None)
        assert rare_stats is None


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

    def test_generate_skills_report_via_generator(self):
        """Тест генерации отчета по навыкам через ReportGenerator"""
        generator = ReportGenerator()

        # Создаем минимальные тестовые данные
        data = [
            {
                'name': 'Test User',
                'position': 'Developer',
                'completed_tasks': 10,
                'performance': 4.5,
                'skills': 'Python, Django',
                'team': 'Team',
                'experience_years': 2
            }
        ]

        result = generator.generate_report('skills', data)

        # Проверяем, что отчет генерируется
        assert 'ОТЧЕТ ПО НАВЫКАМ СОТРУДНИКОВ' in result
        assert 'Python' in result
        assert 'Test User' in result

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
