"""
CSV Performance Reporter

Скрипт для анализа производительности сотрудников на основе CSV данных.
"""

from src.application import Application
from src.services.data_service import DataService
from src.services.report_service import ReportService
from src.services.error_handler import ErrorHandler
from src.adapters.csv_processor_adapter import CSVProcessorAdapter
from src.adapters.report_generator_adapter import ReportGeneratorAdapter


def main() -> None:
    """Основная функция приложения"""
    # Создаем адаптеры для существующих классов
    csv_adapter = CSVProcessorAdapter()
    report_adapter = ReportGeneratorAdapter()

    # Создаем сервисы с инверсией зависимостей
    data_service = DataService(csv_adapter)
    report_service = ReportService(report_adapter)

    # Создаем приложение
    app = Application(data_service, report_service)

    # Запускаем приложение с безопасной обработкой ошибок
    ErrorHandler.safe_execute(lambda: app.run_with_args())


if __name__ == '__main__':
    main()
