"""
Модуль для генерации отчетов
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, DefaultDict
from collections import defaultdict
from tabulate import tabulate
from .config import config


class BaseReport(ABC):
    """Базовый класс для всех отчетов"""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def generate(self, data: List[Dict[str, Any]]) -> str:
        """
        Генерирует отчет на основе данных

        Args:
            data: Список словарей с данными сотрудников

        Returns:
            Строка с отформатированным отчетом
        """
        pass


class PerformanceReport(BaseReport):
    """Отчет по эффективности сотрудников"""

    def __init__(self):
        super().__init__("performance")

    def generate(self, data: List[Dict[str, Any]]) -> str:
        """
        Генерирует отчет по эффективности

        Отчет включает:
        - Позиции сотрудников
        - Среднюю эффективность по каждой позиции
        - Сортировку по эффективности

        Args:
            data: Список словарей с данными сотрудников

        Returns:
            Отформатированный отчет в виде таблицы
        """
        if not data:
            return self._generate_empty_report()

        # Группируем данные по позициям
        position_performance = self._group_by_position(data)

        # Вычисляем среднюю эффективность для каждой позиции
        report_data = self._calculate_average_performance(position_performance)

        # Сортируем данные согласно конфигурации
        sorted_data = self._sort_data(report_data)

        # Формируем таблицу
        return self._format_table(sorted_data)

    def _group_by_position(
        self,
        data: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """Группирует данные по позициям"""
        position_data: DefaultDict[str, Dict[str, Any]] = defaultdict(
            lambda: {'performances': [], 'names': []}
        )

        for employee in data:
            position = employee['position']
            performance = employee['performance']
            name = employee['name']

            position_data[position]['performances'].append(performance)
            position_data[position]['names'].append(name)

        return dict(position_data)

    def _calculate_average_performance(
        self,
        position_data: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Вычисляет среднюю эффективность для каждой позиции"""
        report_data: List[Dict[str, Any]] = []

        for position, data in position_data.items():
            performances = data['performances']
            names = data['names']
            avg_performance = sum(performances) / len(performances)
            report_data.append({
                'position': position,
                'avg_performance': round(avg_performance, 2),
                'employee_count': len(performances),
                'employee_names': names
            })

        return report_data

    def _sort_data(
        self,
        report_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Сортирует данные согласно конфигурации"""
        sort_by_performance = config.get('sort_by_performance')
        sort_order = config.get('sort_order')

        if not sort_by_performance:
            return report_data

        reverse = sort_order.lower() == 'desc'
        return sorted(
            report_data,
            key=lambda x: x['avg_performance'],
            reverse=reverse
        )

    def _format_table(self, sorted_data: List[Dict[str, Any]]) -> str:
        """Формирует данные в таблицу"""
        table_data: List[List[Any]] = []

        for i, item in enumerate(sorted_data, 1):
            # Собираем имена сотрудников для данной позиции
            employee_names = ', '.join(item['employee_names'])
            table_data.append([
                i,
                f"{item['position']}\n({employee_names})",
                item['avg_performance'],
                item['employee_count']
            ])

        headers = ['№', 'Позиция', 'Средняя эффективность',
                   'Количество сотрудников']
        table_format = config.get('table_format', 'grid')

        return tabulate(
            table_data,
            headers=headers,
            tablefmt=table_format
        )

    def _generate_empty_report(self) -> str:
        """Генерирует отчет для пустых данных"""
        headers = ['№', 'Позиция', 'Средняя эффективность',
                   'Количество сотрудников']
        table_format = config.get('table_format', 'grid')

        return tabulate([], headers=headers, tablefmt=table_format)


class ReportGenerator:
    """Генератор отчетов с поддержкой различных типов"""

    def __init__(self):
        self.reports: Dict[str, BaseReport] = {
            'performance': PerformanceReport()
        }

    def generate_report(
            self,
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
            ValueError: Если тип отчета не поддерживается
        """
        if report_type not in self.reports:
            available_reports = ', '.join(self.reports.keys())
            raise ValueError(
                f"Неподдерживаемый тип отчета: '{report_type}'. "
                f"Доступные отчеты: {available_reports}"
            )

        report = self.reports[report_type]
        return report.generate(data)
