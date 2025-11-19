"""
Модуль для обнаружения и работы с файлами
"""
import os
from typing import List
from pathlib import Path


def discover_csv_files(folder_path: str) -> List[str]:
    """
    Рекурсивно находит все CSV файлы в папке и подпапках.

    Args:
        folder_path: Путь к папке для поиска CSV файлов

    Returns:
        Список полных путей к найденным CSV файлам

    Raises:
        FileNotFoundError: Если указанная папка не существует
        NotADirectoryError: Если указанный путь не является папкой
        PermissionError: Если нет прав доступа к папке
    """
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
        # Рекурсивный обход всех папок и подпапок
        for root, _, files in os.walk(folder_path):
            for file in files:
                # Проверяем расширение файла (регистронезависимо)
                if file.lower().endswith('.csv'):
                    full_path = os.path.join(root, file)
                    # Дополнительная проверка, что файл доступен для чтения
                    if os.access(full_path, os.R_OK):
                        csv_files.append(full_path)
    except (OSError, IOError) as e:
        raise IOError(f"Ошибка при обходе папки {folder_path}: {e}")

    # Сортируем файлы для предсказуемого порядка
    csv_files.sort()

    return csv_files
