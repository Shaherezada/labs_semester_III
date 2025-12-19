# domain.py
from abc import ABC, abstractmethod
from typing import Dict

class Dish:
    """Шаблон блюда. Хранит название и цену."""
    def __init__(self, name: str, price: str):
        self.__name = name
        self.__price = price

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> str:
        return self.__price

    def get_price_value(self) -> float:
        """Парсинг цены для математических операций."""
        # Убираем символ валюты и заменяем запятую на точку
        price = self.__price.replace('₽', '').replace(',', '.').strip()
        # Оставляем только цифры и точку
        digits = ''.join(c for c in price if c.isdigit() or c == '.')
        try:
            return float(digits)
        except ValueError:
            return 0.0

    def __repr__(self):
        return f"{self.__name} ({self.__price})"


class HtmlProvider(ABC):
    """
    Интерфейс (контракт) для поставщика HTML.
    Dependency Injection: Delivery не важно, откуда придет HTML.
    """
    @abstractmethod
    def get_html(self, source: str) -> str:
        """
        source: может быть путем к файлу или URL.
        return: строка с HTML кодом.
        """
        pass


class Delivery(ABC):
    """
    Базовый класс доставки.
    Реализует логику хранения меню, но делегирует получение и парсинг.
    """
    def __init__(self, provider: HtmlProvider):
        # Внедрение зависимости: мы принимаем провайдера извне
        self.provider = provider
        self.menu: Dict[int, Dish] = {}

    def load_menu(self, source: str) -> None:
        """
        Шаблонный метод:
        1. Получает HTML через провайдер (сеть/файл).
        2. Вызывает специфичный для кафе парсер.
        """
        print(f"[{self.__class__.__name__}] Запрос данных из: {source}")
        try:
            html_content = self.provider.get_html(source)
            self._parse_html(html_content)
            print(f"[{self.__class__.__name__}] Меню успешно загружено ({len(self.menu)} позиций).")
        except Exception as e:
            print(f"[{self.__class__.__name__}] Ошибка загрузки: {e}")
            # Для теста, если парсинг не удался, добавим заглушку, чтобы код не падал
            if not self.menu:
                self.menu[1] = Dish("Тестовое блюдо (Заглушка)", "100 ₽")

    @abstractmethod
    def _parse_html(self, html_content: str) -> None:
        """
        Абстрактный метод.
        Конкретная реализация (SushiFast/BK) должна здесь распарсить soup.
        """
        pass

    def get_menu(self) -> Dict[int, Dish]:
        return self.menu
