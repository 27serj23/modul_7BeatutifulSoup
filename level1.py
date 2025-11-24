# Уровень 1
# С помощью библиотеки beautifulsoup4 получить с сайта
# http://mfd.ru/currency/?currency=USD
# (http://mfd.ru/currency/?currency=USD) данные о курсе доллара в разные моменты времени.
# Можно с любого другого сайта, если с этим окажется неудобно работать

import requests
from bs4 import BeautifulSoup

url = 'https://mfd.ru/currency/?currency=USD'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

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
else:
    print("Таблица не найдена.")


