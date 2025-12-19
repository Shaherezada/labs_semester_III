# main.py
import os
from random_math import convert_signed
from infrastructure import LocalFileProvider, HttpProvider
from delivery_impl import SushiFast, WaffuruCo

# Создадим фейковый файл ключей для теста, если его нет
if not os.path.exists('keys.txt'):
    with open('keys.txt', 'w') as f:
        f.write("12345\n-67890\n42\n")

if __name__ == '__main__':
    # Фильтр по деньгам
    cash = 5000 # Бюджет в рублях

    # ============================================================
    # ДЕМОНСТРАЦИЯ DEPENDENCY INJECTION
    # ============================================================

    # ВАРИАНТ 1: Работаем через Интернет с пагинацией
    provider = HttpProvider()
    delivery = SushiFast(provider)
    delivery.load_menu("https://sushifast.ru/menu")

    # ВАРИАНТ 2: Работаем локально (без интернета)
    # provider = LocalFileProvider()
    # delivery = SushiFast(provider)
    # delivery.load_menu("Меню — SushiFast.html")

    # ВАРИАНТ 3: Другая доставка (тоже без интернета)
    # provider = LocalFileProvider()
    # delivery = WaffuruCo(provider)
    # delivery.load_menu("Меню — Waffuru & CO.html")

    # ============================================================
    # Преимущество DI: мы можем легко переключаться между
    # источниками данных (файл/интернет), не меняя класс SushiFast
    # ============================================================

    # Получаем готовый словарь {id: Dish}
    menu = delivery.get_menu()

    # Вывод меню
    print("\n--- ДОСТУПНОЕ МЕНЮ ---")
    for i in range(len(menu)):
        if (i + 1) in menu:
            print(f'{i + 1} — {menu[i + 1]}')
    print("----------------------\n")

    # Загрузка ключей из файла
    with open('keys.txt', 'r', encoding='utf-8') as file:
        keys = [line.strip() for line in file.readlines() if line.strip()]

    # Создаем имя временного файла
    temp_file = "keys_temp.txt"

    used_keys = 0

    while keys:
        input("Нажмите Enter для генерации следующего заказа...")

        # Берем следующий ключ и удаляем его из списка
        seed = keys.pop(0)
        used_keys += 1

        print(f"Ключ #{used_keys}: {seed}")

        # Генерация заказа с использованием математики
        try:
            order = convert_signed(int(seed), len(menu))
        except ValueError as e:
            print(f"Ошибка: неверный формат ключа '{seed}' ({e}). Пропускаем.")
            # Сохраняем оставшиеся ключи
            with open(temp_file, 'w', encoding='utf-8') as file:
                file.write('\n'.join(keys))
            os.replace(temp_file, 'keys.txt')
            continue

        total = 0.0
        order_output = []  # Буфер для хранения вывода заказа

        # Собираем информацию о заказе
        for id in order:
            dish = menu[id]
            dish_name = dish.get_name()
            dish_price = dish.get_price()
            price_value = dish.get_price_value()

            # Формируем строку для вывода
            order_line = f"{id}. {dish_name} ({dish_price})"
            order_output.append(order_line)
            total += price_value

        if total > cash:
            print(f"Заказ отфильтрован: сумма {total:.2f}₽ превышает {cash}₽", end='\n\n')

            # Сохраняем оставшиеся ключи
            with open(temp_file, 'w', encoding='utf-8') as file:
                file.write('\n'.join(keys))
            os.replace(temp_file, 'keys.txt')
            continue

        # Выводим заказ, если он прошел проверку
        for line in order_output:
            print(line)
        print(f"Итого: {total:.2f}₽", end='\n\n')

        # Сохраняем оставшиеся ключи после успешной итерации
        with open(temp_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(keys))
        os.replace(temp_file, 'keys.txt')

    # Удаляем временный файл, если он остался
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print("Все ключи из файла были использованы")
