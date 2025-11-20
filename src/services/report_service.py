"""
Сервис для генерации отчетов
"""
from typing import List, Dict, Any
from src.interfaces.report_generator import ReportGeneratorInterface


class ReportService:
    """Сервис для генерации отчетов"""

    def __init__(self, report_generator: ReportGeneratorInterface):
        """
        Инициализация сервиса

        Args:
            report_generator: Генератор отчетов (инверсия зависимостей)
        """
        self._report_generator = report_generator

    def generate_report(self,
                        report_type: str,
                        data: List[Dict[str, Any]]) -> str:
        """
        Генерирует отчет указанного типа

        Args:
            report_type: Тип отчета
            data: Данные для анализа

        Returns:
            Отформатированный отчет

        Raises:
            ValueError: Если данные пусты
        """
        if not data:
            raise ValueError("Нет данных для генерации отчета")

        return self._report_generator.generate_report(report_type, data)
