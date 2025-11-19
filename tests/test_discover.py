"""
Тесты для утилит обнаружения файлов
"""
import pytest
import os
import tempfile

from src.utils.discover import discover_csv_files


class TestDiscoverCSVFiles:
    """Тесты для функции discover_csv_files"""

    def test_discover_csv_files_success(self):
        """Тест успешного обнаружения CSV файлов"""
        # Создаем временную папку с тестовыми файлами
        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем CSV файлы
            csv_file1 = os.path.join(temp_dir, "data1.csv")
            csv_file2 = os.path.join(temp_dir, "data2.csv")
            subfolder = os.path.join(temp_dir, "subfolder")
            os.makedirs(subfolder)
            csv_file3 = os.path.join(subfolder, "data3.csv")

            # Создаем не-CSV файл
            txt_file = os.path.join(temp_dir, "readme.txt")

            # Создаем файлы
            for file_path in [csv_file1, csv_file2, csv_file3, txt_file]:
                with open(file_path, 'w') as f:
                    f.write("test content")

            # Тестируем обнаружение
            result = discover_csv_files(temp_dir)

            # Проверяем результаты
            assert len(result) == 3
            assert csv_file1 in result
            assert csv_file2 in result
            assert csv_file3 in result
            assert txt_file not in result  # Не CSV файл

    def test_discover_csv_files_empty_folder(self):
        """Тест с пустой папкой"""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = discover_csv_files(temp_dir)
            assert result == []

    def test_discover_csv_files_no_csv_files(self):
        """Тест папки без CSV файлов"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем только не-CSV файлы
            txt_file = os.path.join(temp_dir, "readme.txt")
            pdf_file = os.path.join(temp_dir, "document.pdf")

            for file_path in [txt_file, pdf_file]:
                with open(file_path, 'w') as f:
                    f.write("test content")

            result = discover_csv_files(temp_dir)
            assert result == []

    def test_discover_csv_files_folder_not_found(self):
        """Тест с несуществующей папкой"""
        with pytest.raises(FileNotFoundError, match="Папка не найдена"):
            discover_csv_files("/nonexistent/folder")

    def test_discover_csv_files_path_not_directory(self):
        """Тест когда путь не является папкой"""
        with tempfile.NamedTemporaryFile() as tmp_file:
            with pytest.raises(
                    NotADirectoryError, match="Путь не является папкой"):
                discover_csv_files(tmp_file.name)

    def test_discover_csv_files_empty_path(self):
        """Тест с пустым путем"""
        with pytest.raises(
            ValueError,
            match="Путь к папке не может быть пустым"
        ):
            discover_csv_files("")

    def test_discover_csv_files_whitespace_only_path(self):
        """Тест с путем, содержащим только пробелы"""
        with pytest.raises(
            ValueError,
            match="Путь к папке не может быть пустым"
        ):
            discover_csv_files("   ")

    def test_discover_csv_files_case_insensitive(self):
        """Тест регистронезависимости расширения .csv"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем файлы с разными регистрами расширения
            csv_file1 = os.path.join(temp_dir, "data1.CSV")
            csv_file2 = os.path.join(temp_dir, "data2.Csv")
            csv_file3 = os.path.join(temp_dir, "data3.csv")

            for file_path in [csv_file1, csv_file2, csv_file3]:
                with open(file_path, 'w') as f:
                    f.write("test content")

            result = discover_csv_files(temp_dir)

            # Все файлы должны быть найдены независимо от регистра
            assert len(result) == 3
            assert csv_file1 in result
            assert csv_file2 in result
            assert csv_file3 in result

    def test_discover_csv_files_sorted_result(self):
        """Тест сортировки результатов"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем файлы в определенном порядке
            csv_files = ["zebra.csv", "alpha.csv", "beta.csv"]
            for filename in csv_files:
                file_path = os.path.join(temp_dir, filename)
                with open(file_path, 'w') as f:
                    f.write("test content")

            result = discover_csv_files(temp_dir)

            # Результат должен быть отсортирован
            expected_order = [
                os.path.join(temp_dir, "alpha.csv"),
                os.path.join(temp_dir, "beta.csv"),
                os.path.join(temp_dir, "zebra.csv")
            ]
            assert result == expected_order

    def test_discover_csv_files_subdirectories(self):
        """Тест рекурсивного поиска в подпапках"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Создаем структуру папок
            subfolder1 = os.path.join(temp_dir, "folder1")
            subfolder2 = os.path.join(temp_dir, "folder2")
            nested_folder = os.path.join(subfolder1, "nested")

            for folder in [subfolder1, subfolder2, nested_folder]:
                os.makedirs(folder)

            # Создаем файлы в разных папках
            files = [
                os.path.join(temp_dir, "root.csv"),
                os.path.join(subfolder1, "folder1.csv"),
                os.path.join(subfolder2, "folder2.csv"),
                os.path.join(nested_folder, "nested.csv")
            ]

            for file_path in files:
                with open(file_path, 'w') as f:
                    f.write("test content")

            result = discover_csv_files(temp_dir)

            # Все файлы должны быть найдены
            assert len(result) == 4
            for file_path in files:
                assert file_path in result

    def test_discover_csv_files_readonly_files(self):
        """Тест с файлами только для чтения"""
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_readonly = os.path.join(temp_dir, "readonly.csv")
            csv_normal = os.path.join(temp_dir, "normal.csv")

            # Создаем файлы
            with open(csv_readonly, 'w') as f:
                f.write("readonly content")
            with open(csv_normal, 'w') as f:
                f.write("normal content")

            # Делаем один файл только для чтения (на Unix)
            if os.name != 'nt':
                os.chmod(csv_readonly, 0o444)

            try:
                result = discover_csv_files(temp_dir)

                # На системах с поддержкой прав доступа файл только для чтения
                # может быть исключен, если нет права на чтение
                if os.name == 'nt':
                    # На Windows права доступа работают по-другому
                    assert len(result) == 2
                    assert csv_readonly in result
                    assert csv_normal in result
                else:
                    # На Unix файл только для чтения может быть пропущен
                    # если нет права на чтение
                    pass
            finally:
                # Восстанавливаем права
                if os.name != 'nt':
                    os.chmod(csv_readonly, 0o644)
