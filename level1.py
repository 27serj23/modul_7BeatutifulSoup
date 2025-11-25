# Уровень 1
# С помощью библиотеки beautifulsoup4 получить с сайта
# http://mfd.ru/currency/?currency=USD
# (http://mfd.ru/currency/?currency=USD) данные о курсе доллара в разные моменты времени.
# Можно с любого другого сайта, если с этим окажется неудобно работать

"""
Скрипт предназначен для сбора и представления данных о курсах доллара США с сайта https://mfd.ru/currency/.
Данные представляются в формате таблицы с возможностью последующей визуализации или анализа.

Использование:
    python script_name.py
Требуется установить пакеты:
    pip install requests beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup

def fetch_data():
    """
    Функция отправляет GET-запрос на указанный URL и возвращает объект BeautifulSoup.
    Возвращает:
        - Объект BeautifulSoup с распаршенной страницей.
    """
    url = 'https://mfd.ru/currency/?currency=USD'
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def extract_table(soup):
    """
    Эта функция ищет первую таблицу на странице и обрабатывает её данные.
    Аргументы:
        - soup: Объект BeautifulSoup, содержащий весь контент страницы.
    Возвращает:
        - True, если таблица найдена и данные извлечены успешно.
        - False, если таблица не найдена.
    """
    # Находим первую таблицу на странице
    table = soup.find('table')

    if table is not None:
        rows = table.find_all('tr')[1:]  # Пропускаем заголовок таблицы

        # Шапочка таблицы
        print("Дата".ljust(15) + " |" + "Курс".rjust(10) + "  |" + "Изменение".rjust(10))
        print("-" * 40)  # Разделительная линия

        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 3:  # Убедимся, что есть именно 3 колонки
                date = columns[0].get_text().strip()  # Дата
                rate = columns[1].get_text().strip()  # Курс доллара
                change = columns[2].get_text().strip()  # Изменение курса

                # Красивый вывод
                print(f"{date.ljust(15)} | {rate.rjust(10)} | {change.rjust(10)}")
        return True
    else:
        print("Таблица не найдена.")
        return False


# Основная логика программы
if __name__ == "__main__":
    soup = fetch_data()
    result = extract_table(soup)
    if result:
        print("\nТаблица успешно извлечена и представлена!")
    else:
        print("\nНе удалось извлечь данные.")



