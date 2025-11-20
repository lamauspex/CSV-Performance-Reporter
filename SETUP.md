# Инструкция по установке и использованию CSV Performance Reporter

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/lamauspex/CSV-Performance-Reporter/tree/master
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование

### Базовое использование

```bash
python main.py --files data/employees1.csv --report performance
```

#### Работа с несколькими файлами

```bash
python main.py --files data/employees1.csv data/employees2.csv --report performance
```
```bash
python main.py --folder data --report performance
```

### Для анализа навыков сотрудников используйте:

```bash
python main.py --files data/employees1.csv --report skills
```

### Работа с несколькими файлами
```bash
python main.py --files data/employees1.csv data/employees2.csv --report skills
```
```bash
python main.py --folder data --report skills
```

## Параметры командной строки

### Обязательные параметры

- `--files`: Пути к CSV файлам с данными (можно указать несколько файлов)
- `--folder`: Путь к папке с CSV файлами (альтернатива параметру --files)
- `--report`: Название отчета для генерации

### Поддерживаемые отчеты

- `performance` - отчет по эффективности сотрудников (средняя эффективность по позициям)
- `skills` - отчет по навыкам сотрудников (распределение навыков и статистика по сотрудникам)

### Примеры команд

#### Анализ производительности
```bash
# Один файл
python main.py --files data/employees1.csv --report performance

# Несколько файлов
python main.py --files data/employees1.csv data/employees2.csv data/employees3.csv --report performance

# Вся папка
python main.py --folder data --report performance
```

#### Анализ навыков
```bash
# Один файл
python main.py --files data/employees1.csv --report skills

# Несколько файлов
python main.py --files data/employees1.csv data/employees2.csv --report skills

# Вся папка
python main.py --folder data --report skills
```

## Пример вывода

### Отчет по производительности
```
╔════╤══════════════════════╤═════════════════════╤═══════════════════════════╗
║ №  │ Позиция              │Средняя эффективность│ Количество сотрудников    ║
╠════╪══════════════════════╪═════════════════════╪═══════════════════════════╣
║ 1  │ Backend Developer    │ 4.67                │ 3                         ║
║ 2  │ Mobile Developer     │ 4.63                │ 3                         ║
║ 3  │ DevOps Engineer      │ 4.73                │ 2                         ║
║ 4  │ Data Engineer        │ 4.80                │ 2                         ║
╚════╧══════════════════════╧═════════════════════╧═══════════════════════════╝
```

### Отчет по навыкам
```
╔════╤═══════════════════╤═══════════════════════╤═══════════════════════════╗
║ №  │ Навык             │ Количество сотрудников│ Средняя эффективность     ║
╠════╪═══════════════════╪═══════════════════════╪═══════════════════════════╣
║ 1  │ Python            │ 8                     │ 4.65                      ║
║ 2  │ JavaScript        │ 6                     │ 4.58                      ║
║ 3  │ Docker            │ 4                     │ 4.75                      ║
║ 4  │ Kubernetes        │ 3                     │ 4.67                      ║
╚════╧═══════════════════╧═══════════════════════╧═══════════════════════════╝

Сотрудники с навыком 'Python':
╔════╤═══════════════════════╤═══════════════════════╤═══════════════════╗
║ №  │ Имя                   │ Позиция               │ Эффективность     ║
╠════╪═══════════════════════╪═══════════════════════╪═══════════════════╣
║ 1  │ Иван Петров           │ Backend Developer     │ 4.5               ║
║ 2  │ Мария Сидорова        │ Data Engineer         │ 4.8               ║
╚════╧═══════════════════════╧═══════════════════════╧═══════════════════╝
```

## Обработка ошибок

Скрипт корректно обрабатывает следующие ситуации:

### Ошибки файлов
- **Файл не найден**: `Ошибка: Файл 'data/employees1.csv' не найден`
- **Папка не найдена**: `Ошибка: Папка 'data' не найдена`
- **Папка пуста**: `Ошибка: В папке 'data' не найдено CSV файлов`

### Ошибки данных
- **Некорректная структура CSV**: `Ошибка: Некорректные колонки в файле 'data/employees1.csv'`
- **Недопустимое значение performance**: `Ошибка: Недопустимое значение performance=10 в файле 'data/employees1.csv' (должно быть от 0 до 5)`
- **Отсутствует обязательное поле**: `Ошибка: Отсутствует обязательное поле 'name' в файле 'data/employees1.csv'`

### Ошибки отчетов
- **Неподдерживаемый тип отчета**: `Ошибка: Неподдерживаемый тип отчета 'unknown'. Доступные: performance, skills`

## Тестирование

### Запуск всех тестов
```bash
pytest tests/ -v
```

### Запуск тестов с покрытием
```bash
pytest tests/ --cov=. --cov-report=html
```

### Запуск конкретного теста
```bash
pytest tests/test_csv_processor.py -v
```

### Запуск тестов с подробным выводом
```bash
pytest tests/ -v --tb=long
```



## Дополнительная информация

- Подробное описание проекта: [README.md](README.md)
