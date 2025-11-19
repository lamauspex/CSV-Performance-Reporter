"""
CSV Performance Reporter

Скрипт для анализа производительности сотрудников на основе CSV данных.
"""
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

from src.csv_processor import CSVProcessor
from src.report_generator import ReportGenerator


def main() -> None:
    """Основная функция приложения"""
    parser = create_argument_parser()

    try:
        args = parser.parse_args()
    except SystemExit as e:
        # Обрабатываем ошибки парсинга аргументов
        if e.code == 2:  # Ошибка аргументов
            print(
                "Ошибка: Неподдерживаемый тип отчета",
                file=sys.stderr
            )
            sys.exit(2)
        else:
            sys.exit(e.code)

    try:
        # Определяем источник файлов
        if args.folder:
            data = load_and_process_data_from_folder(args.folder)
        else:
            # Валидируем файлы
            validate_files(args.files)
            data = load_and_process_data(args.files)

        # Генерируем и выводим отчет
        report = generate_report(args.report, data)
        print(report)

    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка: Некорректные данные - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


def create_argument_parser() -> argparse.ArgumentParser:
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


def validate_files(file_paths: List[str]) -> None:
    """Валидирует существование файлов"""
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        if not path.is_file():
            raise ValueError(f"Путь не является файлом: {file_path}")
        if not file_path.lower().endswith('.csv'):
            raise ValueError(f"Файл должен иметь расширение .csv: {file_path}")


def load_and_process_data(file_paths: List[str]) -> List[Dict[str, Any]]:
    """Загружает и обрабатывает данные из файлов"""
    processor = CSVProcessor()
    return processor.load_data(file_paths)


def load_and_process_data_from_folder(
        folder_path: str) -> List[Dict[str, Any]]:
    """Загружает и обрабатывает данные из всех CSV файлов в папке"""
    processor = CSVProcessor()
    csv_files = processor.discover_and_validate_files(folder_path)
    return processor.load_data(csv_files)


def generate_report(report_type: str, data: List[Dict[str, Any]]) -> str:
    """Генерирует отчет"""
    report_gen = ReportGenerator()

    # Проверяем, что данные не пусты
    if not data:
        raise ValueError("Нет данных для генерации отчета")

    return report_gen.generate_report(report_type, data)


if __name__ == '__main__':
    main()
