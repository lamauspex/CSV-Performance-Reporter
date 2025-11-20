"""
Главный класс приложения
"""
import argparse
import sys
from typing import List, Dict, Any

from src.services.data_service import DataService
from src.services.report_service import ReportService


class Application:
    """Главный класс приложения"""

    def __init__(self,
                 data_service: DataService,
                 report_service: ReportService):
        """
        Инициализация приложения

        Args:
            data_service: Сервис для работы с данными
            report_service: Сервис для генерации отчетов
        """
        self._data_service = data_service
        self._report_service = report_service

    def run(self, args: argparse.Namespace) -> None:
        """
        Запускает приложение с указанными аргументами

        Args:
            args: Аргументы командной строки
        """
        # Загружаем данные
        data = self._load_data(args)

        # Генерируем отчет
        report = self._report_service.generate_report(args.report, data)

        # Выводим результат
        print(report)

    def run_with_args(self) -> None:
        """
        Запускает приложение с парсингом аргументов командной строки
        """
        parser = self.create_parser()
        try:
            args = parser.parse_args()
        except SystemExit as e:
            if e.code == 2:  # Ошибка аргументов
                print("Ошибка: Неподдерживаемый тип отчета", file=sys.stderr)
                sys.exit(2)
            else:
                sys.exit(e.code)

        self.run(args)

    def _load_data(self, args: argparse.Namespace) -> List[Dict[str, Any]]:
        """
        Загружает данные на основе аргументов

        Args:
            args: Аргументы командной строки

        Returns:
            Список словарей с данными
        """
        if args.folder:
            return self._data_service.load_data(folder_path=args.folder)
        else:
            return self._data_service.load_data(file_paths=args.files)

    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        """Создает парсер аргументов командной строки"""
        parser = argparse.ArgumentParser(
            description='Генератор отчетов производительности из CSV файлов',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Доступные типы отчетов:
  performance  Отчет по эффективности сотрудников по позициям
  skills       Отчет по навыкам сотрудников

Примеры использования:
  python main.py --folder data --report performance
  python main.py --folder data --report skills
  python main.py --files data/employees1.csv --report performance
            """
        )

        # Группа для файлов - либо --files, либо --folder
        file_group = parser.add_mutually_exclusive_group(required=True)
        file_group.add_argument(
            '--files',
            nargs='+',
            help='Пути к CSV файлам с данными сотрудников'
        )
        file_group.add_argument(
            '--folder',
            help='Папка для автоматического поиска CSV файлов'
        )

        parser.add_argument(
            '--report',
            required=True,
            choices=['performance', 'skills'],
            help='Тип отчета для генерации (performance или skills)'
        )
        return parser
