"""
Интерфейс для генерации отчетов
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ReportGeneratorInterface(ABC):
    """Интерфейс для генераторов отчетов"""

    @abstractmethod
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
        """
        pass
