# CSVProcessor

Класс для загрузки, валидации и обработки CSV файлов с данными сотрудников.

## Обзор

CSVProcessor является центральным компонентом системы, отвечающим за:
- Загрузку данных из CSV файлов
- Валидацию структуры и содержимого данных
- Преобразование строковых данных в корректные типы
- Объединение данных из множественных файлов

## Константы

### REQUIRED_COLUMNS
Список обязательных колонок в CSV файлах:

```python
REQUIRED_COLUMNS = [
    'name',            # Имя сотрудника
    'position',        # Должность
    'completed_tasks', # Количество выполненных задач
    'performance',     # Оценка эффективности (0-5)
    'skills',          # Навыки (через запятую)
    'team',            # Команда
    'experience_years' # Опыт работы в годах
]
```

## Конструктор

### __init__()

Создает новый экземпляр CSVProcessor.

```python
processor = CSVProcessor()
```

**Параметры:**
- Отсутствуют

**Атрибуты:**
- `data: List[Dict[str, Any]]` - загруженные данные сотрудников

## Основные методы

### load_data()

Загружает и объединяет данные из нескольких CSV файлов.

```python
data = processor.load_data(['employees1.csv', 'employees2.csv'])
```

**Параметры:**
- `file_paths: List[str]` - список путей к CSV файлам

**Возвращает:**
- `List[Dict[str, Any]]` - объединенные данные всех файлов

**Исключения:**
- `FileNotFoundError` - если файл не найден
- `ValueError` - если файл имеет некорректную структуру

**Примеры использования:**

```python
# Загрузка одного файла
data = processor.load_data(['employees.csv'])

# Загрузка нескольких файлов
data = processor.load_data(['emp1.csv', 'emp2.csv', 'emp3.csv'])

# Пустой список вернет пустые данные
data = processor.load_data([])
```

### discover_and_validate_files()

Находит и валидирует все CSV файлы в указанной папке.

```python
csv_files = processor.discover_and_validate_files('./data/')
```

**Параметры:**
- `folder_path: str` - путь к папке для поиска CSV файлов

**Возвращает:**
- `List[str]` - список путей к найденным CSV файлам

**Исключения:**
- `FileNotFoundError` - если папка не найдена
- `NotADirectoryError` - если путь не является папкой
- `PermissionError` - если нет доступа к папке
- `ValueError` - если в папке не найдено CSV файлов

### discover_default_folder()

Автоматически обнаруживает папку с CSV файлами на основе конфигурации.

```python
default_folder = processor.discover_default_folder()
```

**Возвращает:**
- `str` - путь к папке с CSV файлами

**Исключения:**
- `ValueError` - если папка не найдена или не существует

## Приватные методы

### _load_single_file()

Загружает данные из одного CSV файла.

**Параметры:**
- `file_path: str` - путь к CSV файлу

**Возвращает:**
- `List[Dict[str, Any]]` - данные из файла

### _validate_columns()

Проверяет наличие всех обязательных колонок.

**Параметры:**
- `columns: List[str]` - список колонок из файла
- `file_path: str` - путь к файлу для сообщений об ошибках

**Исключения:**
- `ValueError` - если отсутствуют обязательные колонки

### _process_row()

Обрабатывает и валидирует одну строку данных.

**Параметры:**
- `row: Dict[str, str]` - словарь с данными строки
- `row_num: int` - номер строки в файле
- `file_path: str` - путь к файлу

**Возвращает:**
- `Dict[str, Any]` - обработанный словарь с правильными типами данных

### _process_string_fields()

Обрабатывает строковые поля: name, position, skills, team.

**Параметры:**
- `row: Dict[str, str]` - исходная строка

**Возвращает:**
- `Dict[str, str]` - обработанные строковые поля

**Валидация:**
- Поля не должны быть пустыми
- Значения обрезаются от лишних пробелов

### _process_numeric_fields()

Обрабатывает числовые поля: completed_tasks, performance, experience_years.

**Параметры:**
- `row: Dict[str, str]` - исходная строка

**Возвращает:**
- `Dict[str, Any]` - обработанные числовые поля

**Валидация:**
- `completed_tasks` - должно быть неотрицательным целым числом
- `performance` - должно быть в диапазоне от MIN_PERFORMANCE до MAX_PERFORMANCE (по умолчанию 0-5)
- `experience_years` - должно быть не меньше MIN_EXPERIENCE_YEARS (по умолчанию 0)

## Примеры использования

### Базовое использование

```python
from src.csv_processor import CSVProcessor

# Создаем процессор
processor = CSVProcessor()

# Загружаем данные
try:
    data = processor.load_data(['employees.csv'])
    print(f"Загружено {len(data)} записей")
except (FileNotFoundError, ValueError) as e:
    print(f"Ошибка: {e}")
```

### Работа с папками

```python
# Находим все CSV файлы в папке
csv_files = processor.discover_and_validate_files('./data/')
data = processor.load_data(csv_files)

# Используем папку по умолчанию
default_folder = processor.discover_default_folder()
csv_files = processor.discover_and_validate_files(default_folder)
data = processor.load_data(csv_files)
```

### Обработка ошибок

```python
try:
    data = processor.load_data(['nonexistent.csv'])
except FileNotFoundError as e:
    print(f"Файл не найден: {e}")
except ValueError as e:
    print(f"Некорректные данные: {e}")
```

## Валидация данных

CSVProcessor автоматически валидирует:

1. **Структуру файлов:**
   - Наличие всех обязательных колонок
   - Корректность заголовков

2. **Строковые поля:**
   - Не должны быть пустыми
   - Автоматически обрезаются пробелы

3. **Числовые поля:**
   - `completed_tasks` - целое неотрицательное
   - `performance` - число в диапазоне 0-5
   - `experience_years` - целое неотрицательное

## Связанные компоненты

- **Конфигурация:** Использует `src.config.config` для настройек валидации
- **Поиск файлов:** Использует `src.utils.discover` для обнаружения файлов
- **Интеграция:** Может быть адаптирован через `src.adapters.csv_processor_adapter`