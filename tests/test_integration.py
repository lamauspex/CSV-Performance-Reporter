"""
Интеграционные тесты
"""
import pytest
from io import StringIO
from unittest.mock import patch

from src.config import config


class TestIntegration:
    """Интеграционные тесты для полного цикла работы"""

    def test_main_with_valid_files(self):
        """Тест полного цикла с валидными файлами"""
        # Используем реальные файлы данных
        demo_file = config.get('DEMO_DATA_FILE')
        test_file = config.get('TEST_DATA_FILE')

        # Импортируем main после создания файлов
        from main import main

        # Перехватываем вывод
        with patch(
            'sys.argv',
            [
                'main.py', '--files',
                demo_file, test_file,
                '--report', 'performance'
            ]
        ):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()

                # Проверяем, что отчет содержит ожидаемые данные
                assert 'Позиция' in output
                assert 'Средняя эффективность' in output

                # Проверяем данные из первого файла
                assert 'Mobile Developer' in output
                assert 'Backend Developer' in output

                # Проверяем данные из второго файла
                assert 'Frontend Developer' in output
                assert 'DevOps Engineer' in output
                assert 'QA Engineer' in output

    def test_main_with_demo_file_only(self):
        """Тест с только демонстрационным файлом"""
        demo_file = config.get('DEMO_DATA_FILE')

        from main import main

        with patch(
            'sys.argv',
            ['main.py', '--files', demo_file, '--report', 'performance']
        ):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()

                assert 'Позиция' in output
                assert 'Mobile Developer' in output
                assert 'Backend Developer' in output
                assert 'David Chen' in output or 'Tom Anderson' in output

    def test_main_with_test_file_only(self):
        """Тест с только тестовым файлом"""
        test_file = config.get('TEST_DATA_FILE')

        from main import main

        with patch(
            'sys.argv',
            [
                'main.py', '--files',
                test_file, '--report',
                'performance'
            ]
        ):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()

                assert 'Позиция' in output
                assert 'Backend Developer' in output
                assert 'Alex Ivanov' in output

    def test_main_with_nonexistent_file(self):
        """Тест обработки отсутствующего файла"""
        from main import main

        with patch(
            'sys.argv',
            [
                'main.py', '--files',
                'nonexistent.csv', '--report',
                'performance'
            ]
        ):
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 1
                stderr_output = mock_stderr.getvalue()
                assert 'Файл не найден' in stderr_output

    def test_main_with_invalid_report_type(self):
        """Тест с неподдерживаемым типом отчета"""
        test_file = config.get('TEST_DATA_FILE')

        from main import main

        with patch(
            'sys.argv',
            [
                'main.py', '--files',
                test_file, '--report',
                'invalid_report'
            ]
        ):
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()

                assert exc_info.value.code == 2
                stderr_output = mock_stderr.getvalue()
                assert 'Неподдерживаемый тип отчета' in stderr_output

    def test_config_loading(self):
        """Тест загрузки конфигурации"""
        # Проверяем, что конфигурация загружается корректно
        assert config.get('default_report_type') == 'performance'
        assert 'employees1.csv' in config.get('DEMO_DATA_FILE')
        assert 'employees2.csv' in config.get('TEST_DATA_FILE')
        assert config.get('min_performance') == 0.0
        assert config.get('max_performance') == 5.0
