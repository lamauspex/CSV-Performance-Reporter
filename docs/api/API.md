# API Reference

Полная справочная документация по API CSV Performance Reporter.

## Обзор

CSV Performance Reporter предоставляет программный интерфейс для анализа данных сотрудников из CSV файлов и генерации различных типов отчетов.

## Основные классы

### CSVProcessor
Основной класс для загрузки и обработки CSV файлов с данными сотрудников.

**Расположение:** `src/csv_processor.py`

### ReportGenerator
Фабрика для создания отчетов различных типов.

**Расположение:** `src/report_generator.py`

### Application
Главный класс приложения, координирующий работу всех компонентов.

**Расположение:** `src/application.py`

### DataService
Сервис для работы с данными и их загрузки.

**Расположение:** `src/services/data_service.py`

### ReportService
Сервис для генерации и управления отчетами.

**Расположение:** `src/services/report_service.py`

## Интерфейсы

### DataLoaderInterface
Интерфейс для загрузчиков данных.

**Расположение:** `src/interfaces/data_loader.py`

### ReportGeneratorInterface
Интерфейс для генераторов отчетов.

**Расположение:** `src/interfaces/report_generator.py`

## Адаптеры

### CSVProcessorAdapter
Адаптер для интеграции CSVProcessor с остальной системой.

**Расположение:** `src/adapters/csv_processor_adapter.py`

### ReportGeneratorAdapter
Адаптер для интеграции ReportGenerator с остальной системой.

**Расположение:** `src/adapters/report_generator_adapter.py`

## Конфигурация

### Config
Основной класс конфигурации.

**Расположение:** `src/config/config.py`

---

*Для подробной документации каждого класса перейдите к соответствующим разделам.*