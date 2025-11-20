"""
Unit-тесты для ReportService
"""
import pytest
from unittest.mock import Mock
from typing import List, Dict, Any

from src.services.report_service import ReportService
from src.interfaces.report_generator import ReportGeneratorInterface


class MockReportGenerator(ReportGeneratorInterface):
    """Mock-реализация ReportGeneratorInterface для тестирования"""

    def __init__(self, report_to_return: str):
        self.report_to_return = report_to_return
        self.generate_report_calls = []

    def generate_report(self, report_type: str, data: List[Dict[str, Any]]) -> str:
        self.generate_report_calls.append({
            'report_type': report_type,
            'data': data
        })
        return self.report_to_return


class TestReportService:
    """Тесты для класса ReportService"""

    def test_init_with_report_generator(self):
        """Тест инициализации с генератором отчетов"""
        mock_generator = MockReportGenerator("Mock Report")
        service = ReportService(mock_generator)

        assert service._report_generator is mock_generator

    def test_generate_report_success(self):
        """Тест успешной генерации отчета"""
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

        expected_report = "Performance Report Generated Successfully"
        mock_generator = MockReportGenerator(expected_report)
        service = ReportService(mock_generator)

        # Генерируем отчет
        result = service.generate_report('performance', test_data)

        # Проверяем результат
        assert result == expected_report

        # Проверяем, что генератор был вызван с правильными параметрами
        assert len(mock_generator.generate_report_calls) == 1
        call_args = mock_generator.generate_report_calls[0]
        assert call_args['report_type'] == 'performance'
        assert call_args['data'] == test_data

    def test_generate_report_empty_data_raises_error(self):
        """Тест ошибки при генерации отчета с пустыми данными"""
        mock_generator = MockReportGenerator("Report")
        service = ReportService(mock_generator)

        with pytest.raises(ValueError, match="Нет данных для генерации отчета"):
            service.generate_report('performance', [])

    def test_generate_report_with_none_data_raises_error(self):
        """Тест ошибки при генерации отчета с None данными"""
        mock_generator = MockReportGenerator("Report")
        service = ReportService(mock_generator)

        with pytest.raises(ValueError, match="Нет данных для генерации отчета"):
            service.generate_report('performance', None)

    def test_generate_report_different_types(self):
        """Тест генерации отчетов разных типов"""
        test_data = [
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

        # Создаем генератор, который возвращает разные отчеты в зависимости от типа
        def mock_generate_report(report_type: str, data: List[Dict[str, Any]]) -> str:
            if report_type == 'performance':
                return f"Performance Report: {len(data)} employees"
            elif report_type == 'skills':
                return f"Skills Report: {len(data)} employees"
            else:
                return f"Unknown Report: {report_type}"

        mock_generator = Mock(spec=ReportGeneratorInterface)
        mock_generator.generate_report = mock_generate_report

        service = ReportService(mock_generator)

        # Тестируем разные типы отчетов
        performance_result = service.generate_report('performance', test_data)
        skills_result = service.generate_report('skills', test_data)

        assert "Performance Report" in performance_result
        assert "Skills Report" in skills_result

    def test_generate_report_multiple_calls(self):
        """Тест множественных вызовов генерации отчетов"""
        test_data1 = [{'name': 'User1', 'performance': 4.5}]
        test_data2 = [{'name': 'User2', 'performance': 4.0}]
        test_data3 = [{'name': 'User3', 'performance': 4.8}]

        mock_generator = MockReportGenerator("Report")
        service = ReportService(mock_generator)

        # Генерируем несколько отчетов
        service.generate_report('performance', test_data1)
        service.generate_report('skills', test_data2)
        service.generate_report('performance', test_data3)

        # Проверяем, что все вызовы были зарегистрированы
        assert len(mock_generator.generate_report_calls) == 3

        # Проверяем параметры каждого вызова
        assert mock_generator.generate_report_calls[0]['report_type'] == 'performance'
        assert mock_generator.generate_report_calls[0]['data'] == test_data1

        assert mock_generator.generate_report_calls[1]['report_type'] == 'skills'
        assert mock_generator.generate_report_calls[1]['data'] == test_data2

        assert mock_generator.generate_report_calls[2]['report_type'] == 'performance'
        assert mock_generator.generate_report_calls[2]['data'] == test_data3

    def test_dependency_injection(self):
        """Тест инверсии зависимостей"""
        # Создаем mock-генератор
        mock_generator = MockReportGenerator("Test Report")

        # Создаем сервис
        service = ReportService(mock_generator)

        # Проверяем, что зависимость правильно внедрена
        assert service._report_generator is mock_generator

        # Проверяем, что сервис может использовать генератор
        test_data = [{'name': 'Test', 'performance': 4.5}]
        result = service.generate_report('performance', test_data)
        assert result == "Test Report"

    def test_service_isolation(self):
        """Тест изоляции сервиса"""
        # Создаем два разных генератора
        generator1 = MockReportGenerator("Report 1")
        generator2 = MockReportGenerator("Report 2")

        service1 = ReportService(generator1)
        service2 = ReportService(generator2)

        test_data = [{'name': 'Test', 'performance': 4.5}]

        # Проверяем, что сервисы изолированы
        result1 = service1.generate_report('performance', test_data)
        result2 = service2.generate_report('performance', test_data)

        assert result1 == "Report 1"
        assert result2 == "Report 2"
        assert result1 != result2

    def test_error_propagation(self):
        """Тест распространения ошибок от генератора"""
        def mock_generate_with_error(report_type: str, data: List[Dict[str, Any]]) -> str:
            if report_type == 'error':
                raise ValueError("Custom error from generator")
            return "Normal report"

        mock_generator = Mock(spec=ReportGeneratorInterface)
        mock_generator.generate_report = mock_generate_with_error

        service = ReportService(mock_generator)
        test_data = [{'name': 'Test', 'performance': 4.5}]

        # Ошибка должна распространяться от генератора к сервису
        with pytest.raises(ValueError, match="Custom error from generator"):
            service.generate_report('error', test_data)

        # Нормальный отчет должен работать
        result = service.generate_report('performance', test_data)
        assert result == "Normal report"

    def test_large_data_handling(self):
        """Тест обработки больших объемов данных"""
        # Создаем большой набор данных
        large_data = [
            {
                'name': f'User{i}',
                'position': 'Developer',
                'completed_tasks': 25,
                'performance': 4.5,
                'skills': 'Python',
                'team': 'Team',
                'experience_years': 3
            }
            for i in range(1000)
        ]

        expected_report = f"Large Report: {len(large_data)} employees"
        mock_generator = MockReportGenerator(expected_report)
        service = ReportService(mock_generator)

        # Генерируем отчет для больших данных
        result = service.generate_report('performance', large_data)

        # Проверяем, что отчет сгенерирован корректно
        assert result == expected_report

        # Проверяем, что данные переданы генератору
        assert len(mock_generator.generate_report_calls) == 1
        assert mock_generator.generate_report_calls[0]['data'] == large_data
