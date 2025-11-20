"""
Обработчик ошибок приложения
"""
import sys
from typing import Callable


class ErrorHandler:
    """Централизованный обработчик ошибок"""

    @staticmethod
    def handle_file_not_found(error: FileNotFoundError) -> None:
        """Обрабатывает ошибки отсутствия файлов"""
        print(f"Ошибка: Файл не найден - {error}", file=sys.stderr)
        sys.exit(1)

    @staticmethod
    def handle_value_error(error: ValueError) -> None:
        """Обрабатывает ошибки валидации данных"""
        print(f"Ошибка: Некорректные данные - {error}", file=sys.stderr)
        sys.exit(1)

    @staticmethod
    def handle_unexpected_error(error: Exception) -> None:
        """Обрабатывает неожиданные ошибки"""
        print(f"Неожиданная ошибка: {error}", file=sys.stderr)
        sys.exit(1)

    @staticmethod
    def handle_argument_error(error: SystemExit) -> None:
        """Обрабатывает ошибки парсинга аргументов"""
        if error.code == 2:  # Ошибка аргументов
            print("Ошибка: Неподдерживаемый тип отчета", file=sys.stderr)
            sys.exit(2)
        sys.exit(error.code)

    @classmethod
    def safe_execute(cls, func: Callable, *args, **kwargs) -> None:
        """
        Выполняет функцию с безопасной обработкой ошибок

        Args:
            func: Функция для выполнения
            *args: Аргументы функции
            **kwargs: Именованные аргументы функции
        """
        try:
            func(*args, **kwargs)
        except FileNotFoundError as e:
            cls.handle_file_not_found(e)
        except ValueError as e:
            cls.handle_value_error(e)
        except SystemExit as e:
            cls.handle_argument_error(e)
        except Exception as e:
            cls.handle_unexpected_error(e)
