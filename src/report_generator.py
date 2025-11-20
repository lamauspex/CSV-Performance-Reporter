"""
Модуль для генерации отчетов
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, DefaultDict
from collections import defaultdict
from tabulate import tabulate

from src.config import config


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
        sort_by_performance = config.get('SORT_BY_PERFORMANCE')
        sort_order = config.get('SORT_ORDER')

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


class SkillsReport(BaseReport):
    """Отчет по навыкам сотрудников"""

    def __init__(self):
        super().__init__("skills")

    def generate(self, data: List[Dict[str, Any]]) -> str:
        """
        Генерирует отчет по навыкам

        Отчет включает:
        - Топ навыков по популярности
        - Топ сотрудников по количеству навыков
        - Статистику по навыкам

        Args:
            data: Список словарей с данными сотрудников

        Returns:
            Отформатированный отчет по навыкам
        """
        if not data:
            return self._generate_empty_report()

        # Парсинг навыков из данных
        parsed_data = self._parse_skills_from_data(data)

        # Анализ распределения навыков
        skills_stats = self._analyze_skills_distribution(parsed_data)

        # Анализ сотрудников по навыкам
        employees_stats = self._analyze_employees_skills(parsed_data)

        # Формирование отчета
        return self._format_skills_report(skills_stats, employees_stats)

    def _parse_skills_from_data(
            self,
            data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Парсит навыки из данных сотрудников"""
        parsed_data = []

        for employee in data:
            skills_str = employee.get('skills', '')
            skills_list = self._parse_skills_string(skills_str)

            parsed_employee = employee.copy()
            parsed_employee['skills_list'] = skills_list
            parsed_data.append(parsed_employee)

        return parsed_data

    def _parse_skills_string(self, skills_string: str) -> List[str]:
        """Парсит строку навыков в список"""
        if not skills_string:
            return []

        # Разделяем по запятой и убираем лишние пробелы
        skills = [skill.strip() for skill in skills_string.split(',')]
        # Убираем пустые строки
        skills = [skill for skill in skills if skill]

        return skills

    def _analyze_skills_distribution(
            self,
            data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Анализирует распределение навыков"""
        skills_stats: DefaultDict[str, Dict[str, Any]] = defaultdict(
            lambda: {'employees': [], 'performances': []}
        )

        min_occurrence = config.get('SKILLS_REPORT_MIN_OCCURRENCE', 2)

        # Собираем статистику по каждому навыку
        for employee in data:
            name = employee['name']
            performance = employee['performance']
            skills_list = employee['skills_list']

            for skill in skills_list:
                skills_stats[skill]['employees'].append(name)
                skills_stats[skill]['performances'].append(performance)

        # Формируем результат
        result = []
        for skill, stats in skills_stats.items():
            if len(stats['employees']) >= min_occurrence:
                avg_performance = sum(
                    stats['performances']) / len(stats['performances'])
                result.append({
                    'skill': skill,
                    'employee_count': len(stats['employees']),
                    'avg_performance': round(avg_performance, 2),
                    'employees': stats['employees']
                })

        # Сортируем по количеству сотрудников (по убыванию)
        return sorted(result, key=lambda x: x['employee_count'], reverse=True)

    def _analyze_employees_skills(
            self,
            data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Анализирует сотрудников по количеству навыков"""
        employees_stats = []

        for employee in data:
            name = employee['name']
            position = employee['position']
            performance = employee['performance']
            skills_list = employee['skills_list']

            employees_stats.append({
                'name': name,
                'position': position,
                'performance': performance,
                'skills_count': len(skills_list),
                'skills': skills_list
            })

        # Сортируем по количеству навыков (по убыванию)
        return sorted(
            employees_stats,
            key=lambda x: x['skills_count'],
            reverse=True
        )

    def _format_skills_report(
            self,
            skills_stats: List[Dict],
            employees_stats: List[Dict]) -> str:
        """Форматирует полный отчет по навыкам"""
        report_parts = []

        # Заголовок отчета
        report_parts.append("=== ОТЧЕТ ПО НАВЫКАМ СОТРУДНИКОВ ===\n")

        # Топ навыков
        report_parts.append(self._format_skills_table(
            skills_stats[:10]))  # Топ 10
        report_parts.append("\n")

        # Топ сотрудников по навыкам
        report_parts.append(self._format_employees_table(
            employees_stats[:10]))  # Топ 10

        return "".join(report_parts)

    def _format_skills_table(self, skills_stats: List[Dict]) -> str:
        """Форматирует таблицу навыков"""
        if not skills_stats:
            return "Навыки не найдены"

        table_data = []
        for i, skill_data in enumerate(skills_stats, 1):
            employees_str = ', '.join(
                skill_data['employees'][:3])  # Показываем первых 3
            if len(skill_data['employees']) > 3:
                employees_str += f" и еще {len(skill_data['employees']) - 3}"

            table_data.append([
                i,
                skill_data['skill'],
                skill_data['employee_count'],
                skill_data['avg_performance'],
                employees_str
            ])

        headers = ['№', 'Навык', 'Кол-во сотрудников',
                   'Ср. эффективность', 'Сотрудники']
        table_format = config.get('table_format', 'grid')

        return tabulate(table_data, headers=headers, tablefmt=table_format)

    def _format_employees_table(self, employees_stats: List[Dict]) -> str:
        """Форматирует таблицу сотрудников"""
        if not employees_stats:
            return "Данные о сотрудниках не найдены"

        table_data = []
        for i, emp_data in enumerate(employees_stats, 1):
            skills_str = ', '.join(emp_data['skills'])
            table_data.append([
                i,
                emp_data['name'],
                emp_data['position'],
                emp_data['skills_count'],
                emp_data['performance'],
                skills_str
            ])

        headers = ['№', 'Имя', 'Позиция',
                   'Кол-во навыков', 'Эффективность', 'Навыки']
        table_format = config.get('table_format', 'grid')

        return tabulate(table_data, headers=headers, tablefmt=table_format)

    def _generate_empty_report(self) -> str:
        """Генерирует отчет для пустых данных"""
        return "Нет данных для анализа навыков"


class ReportGenerator:
    """Генератор отчетов с поддержкой различных типов"""

    def __init__(self):
        self.reports: Dict[str, BaseReport] = {
            'performance': PerformanceReport(),
            'skills': SkillsReport()
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
