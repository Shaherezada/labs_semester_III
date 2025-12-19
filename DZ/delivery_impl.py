# delivery_impl.py
from bs4 import BeautifulSoup
from domain import Delivery, Dish, HtmlProvider


class SushiFast(Delivery):
    """
    Реализация доставки SushiFast.
    Умеет парсить меню с пагинацией.
    """

    def __init__(self, provider: HtmlProvider):
        super().__init__(provider)

    def _parse_html(self, html_content: str) -> None:
        """
        Абстрактный метод из родителя.
        Не используется, т.к. мы переопределили load_menu().
        """
        pass

    def load_menu(self, source: str) -> None:
        """
        Переопределяем load_menu для обработки пагинации.
        """
        print(f"[SushiFast] Запрос данных из: {source}")
        try:
            # Получаем первую страницу
            html_content = self.provider.get_html(source)
            soup = BeautifulSoup(html_content, "lxml")

            # Парсим первую страницу
            self._parse_page(soup)

            # Проверяем пагинацию
            pagination = soup.find("nav", class_="woocommerce-pagination")
            if pagination:
                page_links = pagination.find_all("a", class_="page-numbers")
                max_page = 1

                for link in page_links:
                    try:
                        page_num = int(link.get_text(strip=True))
                        if page_num > max_page:
                            max_page = page_num
                    except ValueError:
                        continue

                # Определяем базовый URL
                if source.startswith("http://") or source.startswith("https://"):
                    base_url = source.rstrip("/")

                    # Загружаем остальные страницы
                    for page_num in range(2, max_page + 1):
                        print(f"[SushiFast] Загрузка страницы {page_num}/{max_page}...")
                        page_url = f"{base_url}/page/{page_num}/"

                        page_html = self.provider.get_html(page_url)
                        page_soup = BeautifulSoup(page_html, "lxml")
                        self._parse_page(page_soup)

            print(f"[SushiFast] Меню успешно загружено ({len(self.menu)} позиций).")

        except Exception as e:
            print(f"[SushiFast] Ошибка загрузки: {e}")
            if not self.menu:
                self.menu[1] = Dish("Тестовое блюдо (Заглушка)", "100 ₽")

    def _parse_page(self, soup: BeautifulSoup) -> None:
        """
        Парсит одну страницу меню.
        """
        items_container = soup.find("ul", class_="products")

        if not items_container:
            return

        items = items_container.find_all("li", class_="product")
        current_index = len(self.menu) + 1

        for item in items:
            name_tag = item.find("h2", class_="woocommerce-loop-product__title")
            if not name_tag:
                continue

            name = name_tag.get_text(strip=True)
            price_tag = item.find("span", class_="woocommerce-Price-amount")
            price = price_tag.get_text(strip=True) if price_tag else "Без цены"

            self.menu[current_index] = Dish(name, price)
            current_index += 1


# Соблюдение Liskov Substitution Principle (LSP):
# Класс WaffuruCo ведет себя именно так, как ожидает базовый класс Delivery.
# Он не меняет поведение публичного метода load_menu.
class WaffuruCo(Delivery):
    """
    Реализация доставки Waffuru & CO.
    """

    def __init__(self, provider: HtmlProvider):
        super().__init__(provider)

    def _parse_html(self, html_content: str) -> None:
        """
        Реализация абстрактного метода.
        Парсит HTML структуру Waffuru & CO.
        """
        soup = BeautifulSoup(html_content, "lxml")

        # Находим контейнеры (карточки товаров)
        items = soup.find_all("div", class_="ddish")

        current_index = len(self.menu) + 1

        for item in items:
            # Ищем название
            name_tag = item.find("a", class_="ddish__name")
            if not name_tag:
                continue

            name = name_tag.get_text(strip=True)

            # Ищем блок с ценой
            price_tag = item.find("div", class_="ddish__sum")

            if price_tag:
                # ВАРИАНТ 1 (Лучший): Берем цену из атрибута data-price="485"
                if price_tag.has_attr("data-price"):
                    clean_price = price_tag["data-price"]
                    price = f"{clean_price} ₽"
                else:
                    # ВАРИАНТ 2 (Запасной): Если атрибута нет, чистим текст
                    # Текст вида: "от 485 ₽" -> заменяем "от" на пустоту
                    raw_text = price_tag.get_text(strip=True)
                    price = raw_text.replace("от", "").strip()
            else:
                price = "0 ₽"
            # -----------------------

            self.menu[current_index] = Dish(name, price)
            current_index += 1
