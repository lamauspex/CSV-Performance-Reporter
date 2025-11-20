"""
Адаптер для ReportGenerator
"""
from typing import List, Dict, Any
from src.interfaces.report_generator import ReportGeneratorInterface
from src.report_generator import ReportGenerator


class ReportGeneratorAdapter(ReportGeneratorInterface):
    """Адаптер для ReportGenerator, реализующий ReportGeneratorInterface"""

    def __init__(self):
        self._generator = ReportGenerator()

    def generate_report(self,
                        report_type: str,
                        data: List[Dict[str, Any]]) -> str:
        """Реализация генерации отчета"""
        return self._generator.generate_report(report_type, data)
