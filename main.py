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
    args = parser.parse_args()

    try:
        # Валидируем файлы
        validate_files(args.files)

        # Загружаем и обрабатываем данные
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
        description='Генератор отчетов производительности из CSV файлов'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Пути к CSV файлам с данными'
    )
    parser.add_argument(
        '--report',
        required=True,
        help='Название отчета для генерации'
    )
    return parser


def validate_files(file_paths: List[str]) -> None:
    """Валидирует существование файлов"""
    for file_path in file_paths:
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")


def load_and_process_data(file_paths: List[str]) -> List[Dict[str, Any]]:
    """Загружает и обрабатывает данные из файлов"""
    processor = CSVProcessor()
    return processor.load_data(file_paths)


def generate_report(report_type: str, data: List[Dict[str, Any]]) -> str:
    """Генерирует отчет"""
    report_gen = ReportGenerator()
    return report_gen.generate_report(report_type, data)


if __name__ == '__main__':
    main()
