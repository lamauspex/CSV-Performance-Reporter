# Application

Главный класс приложения, координирующий работу всех компонентов системы.

## Обзор

Application является центральной точкой входа в систему CSV Performance Reporter. Класс координирует работу между сервисами данных и отчетов, управляет аргументами командной строки и обеспечивает единый интерфейс для запуска приложения.

## Архитектура

```
Application
├── DataService (загрузка данных)
└── ReportService (генерация отчетов)
```

## Конструктор

### __init__(data_service: DataService, report_service: ReportService)

Создает экземпляр приложения с указанными сервисами.

**Параметры:**
- `data_service: DataService` - сервис для работы с данными
- `report_service: ReportService` - сервис для генерации отчетов

**Атрибуты:**
- `_data_service: DataService` - сервис данных
- `_report_service: ReportService` - сервис отчетов

**Пример использования:**

```python
from src.services.data_service import DataService
from src.services.report_service import ReportService
from src.application import Application

# Создаем сервисы
data_service = DataService()
report_service = ReportService()

# Создаем приложение
app = Application(data_service, report_service)
```

## Основные методы

### run()

Запускает приложение с указанными аргументами.

```python
app.run(args)
```

**Параметры:**
- `args: argparse.Namespace` - аргументы командной строки

**Процесс выполнения:**
1. Загружает данные с помощью `_load_data()`
2. Определяет тип отчета (из аргументов или конфигурации)
3. Генерирует отчет с помощью ReportService
4. Выводит результат в консоль

**Пример:**

```python
import argparse

# Создаем аргументы
args = argparse.Namespace()
args.folder = './data/'
args.report = 'performance'

# Запускаем приложение
app.run(args)
```

### run_with_args()

Запускает приложение с автоматическим парсингом аргументов командной строки.

```python
app.run_with_args()
```

**Функциональность:**
- Создает парсер аргументов через `create_parser()`
- Парсит `sys.argv`
- Обрабатывает ошибки парсинга
- Вызывает `run()` с распарсенными аргументами

**Обработка ошибок:**
- При ошибке аргументов выводит сообщение об ошибке и завершается с кодом 2
- При других ошибках передает их системе

**Пример:**

```python
# Запуск из командной строки
# python main.py --folder data --report performance
app.run_with_args()
```

## Вспомогательные методы

### _load_data()

Загружает данные на основе аргументов командной строки.

**Параметры:**
- `args: argparse.Namespace` - аргументы командной строки

**Логика работы:**
- Если указан `args.folder` - загружает данные из папки
- Если указаны `args.files` - загружает данные из файлов
- Использует DataService для фактической загрузки

**Возвращает:**
- `List[Dict[str, Any]]` - загруженные данные сотрудников

### create_parser()

Создает парсер аргументов командной строки.

```python
parser = Application.create_parser()
```

**Возвращает:**
- `argparse.ArgumentParser` - настроенный парсер аргументов

**Поддерживаемые аргументы:**

#### Обязательные (взаимоисключающие):
- `--files` - пути к CSV файлам (можно указать несколько)
- `--folder` - путь к папке с CSV файлами

#### Опциональные:
- `--report` - тип отчета ('performance' или 'skills', по умолчанию из конфигурации)

**Примеры команд:**

```bash
# Использование папки
python main.py --folder data --report performance

# Использование файлов
python main.py --files data/employees1.csv data/employees2.csv --report skills

# Использование типа отчета по умолчанию
python main.py --folder data
```

**Справка парсера:**

Парсер автоматически генерирует справку:

```
usage: main.py [-h] (--files FILES [FILES ...] | --folder FOLDER) [--report {performance,skills}]

Генератор отчетов производительности из CSV файлов

optional arguments:
  -h, --help            show this help message and exit
  --files FILES [FILES ...]
                        Пути к CSV файлам с данными сотрудников
  --folder FOLDER       Папка для автоматического поиска CSV файлов
  --report {performance,skills}
                        Тип отчета для генерации (по умолчанию: performance)

Доступные типы отчетов:
  performance  Отчет по эффективности сотрудников по позициям
  skills       Отчет по навыкам сотрудников

Примеры использования:
  python main.py --folder data --report performance
  python main.py --folder data --report skills
  python main.py --files data/employees1.csv --report performance
```

## Интеграция с компонентами

### DataService
Application использует DataService для:
- Загрузки данных из файлов (`load_data(file_paths=...)`)
- Загрузки данных из папок (`load_data(folder_path=...)`)

### ReportService
Application использует ReportService для:
- Генерации отчетов (`generate_report(report_type, data)`)
- Получения поддерживаемых типов отчетов

### Конфигурация
Application использует конфигурацию для:
- Получения типа отчета по умолчанию (`DEFAULT_REPORT_TYPE`)
- Настройки поведения парсера аргументов

## Примеры использования

### Программный запуск

```python
from src.application import Application
from src.services.data_service import DataService
from src.services.report_service import ReportService
import argparse

# Создаем компоненты
data_service = DataService()
report_service = ReportService()
app = Application(data_service, report_service)

# Создаем аргументы
args = argparse.Namespace()
args.folder = './data/'
args.report = 'performance'

# Запускаем
app.run(args)
```

### Запуск из командной строки

```python
from src.application import Application
from src.services.data_service import DataService
from src.services.report_service import ReportService

# Создаем компоненты
data_service = DataService()
report_service = ReportService()
app = Application(data_service, report_service)

# Запуск с парсингом sys.argv
app.run_with_args()
```

### Обработка ошибок

```python
try:
    app.run_with_args()
except SystemExit as e:
    if e.code == 2:
        print("Ошибка в аргументах командной строки")
    else:
        print(f"Приложение завершено с кодом: {e.code}")
```

## Жизненный цикл приложения

```
1. Создание Application с сервисами
   ↓
2. Парсинг аргументов (run_with_args) ИЛИ
   Получение аргументов (run)
   ↓
3. Загрузка данных через DataService
   ↓
4. Генерация отчета через ReportService
   ↓
5. Вывод результата в консоль
```

## Связанные компоненты

- **DataService**: `src/services/data_service.py`
- **ReportService**: `src/services/report_service.py`
- **Конфигурация**: `src/config/config.py`
- **Точка входа**: `main.py`