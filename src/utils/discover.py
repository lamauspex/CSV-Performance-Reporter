"""
Модуль для обнаружения и работы с файлами
"""
import os
from typing import List
from pathlib import Path
from src.config import config


def discover_csv_files(
    folder_path: str,
    include_subfolders: bool = None
) -> List[str]:
    """
    Рекурсивно находит все CSV файлы в папке и подпапках.

    Args:
        folder_path:
        Путь к папке для поиска CSV файлов

        include_subfolders:
        Включать ли подпапки (берется из конфигурации если None)

    Returns:
        Список полных путей к найденным CSV файлам

    Raises:
        FileNotFoundError: Если указанная папка не существует
        NotADirectoryError: Если указанный путь не является папкой
        PermissionError: Если нет прав доступа к папке
    """
    # Получаем настройку из конфигурации если не указана явно
    if include_subfolders is None:
        include_subfolders = config.get('INCLUDE_SUBFOLDERS', False)

    path = Path(folder_path)

    # Валидация входного параметра
    if not folder_path or not folder_path.strip():
        raise ValueError("Путь к папке не может быть пустым")

    # Проверка существования папки
    if not path.exists():
        raise FileNotFoundError(f"Папка не найдена: {folder_path}")

    # Проверка, что это именно папка
    if not path.is_dir():
        raise NotADirectoryError(f"Путь не является папкой: {folder_path}")

    # Проверка прав доступа
    if not os.access(folder_path, os.R_OK):
        raise PermissionError(
            f"Нет прав доступа для чтения папки: {folder_path}")

    csv_files: List[str] = []

    try:
        if include_subfolders:
            # Рекурсивный обход всех папок и подпапок
            for root, _, files in os.walk(folder_path):
                for file in files:
                    # Проверяем расширение файла (регистронезависимо)
                    if file.lower().endswith('.csv'):
                        full_path = os.path.join(root, file)
                        # Дополнительная проверка, что файл доступен для чтения
                        if os.access(full_path, os.R_OK):
                            csv_files.append(full_path)
        else:
            # Поиск только в указанной папке (без подпапок)
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                # Проверяем, что это файл (не папка) и он доступен для чтения
                if os.path.isfile(file_path) and os.access(file_path, os.R_OK):
                    # Проверяем расширение файла (регистронезависимо)
                    if file.lower().endswith('.csv'):
                        csv_files.append(file_path)
    except (OSError, IOError) as e:
        raise IOError(f"Ошибка при обходе папки {folder_path}: {e}")

    # Сортируем файлы для предсказуемого порядка
    csv_files.sort()

    return csv_files


def discover_default_csv_folder() -> str:
    """
    Автоматически обнаруживает папку с CSV файлами на основе конфигурации.

    Returns:
        Путь к папке с CSV файлами

    Raises:
        ValueError: Если папка не найдена или не существует
    """
    # Получаем путь к папке из конфигурации
    csv_folder = config.get('CSV_FOLDER_PATH', 'data')

    # Проверяем, существует ли папка
    if not os.path.exists(csv_folder):
        raise ValueError(f"Папка с CSV файлами не найдена: {csv_folder}")

    if not os.path.isdir(csv_folder):
        raise ValueError(f"Указанный путь не является папкой: {csv_folder}")

    return csv_folder
