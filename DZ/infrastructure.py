# infrastructure.py
import os
import requests
from domain import HtmlProvider


class LocalFileProvider(HtmlProvider):
    """
    Реализация провайдера для чтения локальных файлов.
    Полезно для тестов или если нет интернета.
    """

    def get_html(self, source: str) -> str:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Файл {source} не найден в директории.")

        with open(source, 'r', encoding='utf-8') as f:
            return f.read()


class HttpProvider(HtmlProvider):
    """
    Реализация провайдера для HTTP запросов.
    Использует библиотеку requests.
    """

    def __init__(self):
        # Притворяемся обычным браузером, чтобы сайт не блокировал бота (Spijuniro Golubiro)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_html(self, source: str) -> str:
        print(f"[HttpProvider] Отправка GET запроса на {source}...")
        response = requests.get(source, headers=self.headers)

        # Если статус не 200 OK, выбросит исключение
        response.raise_for_status()

        # Пытаемся корректно определить кодировку
        response.encoding = response.apparent_encoding
        return response.text
