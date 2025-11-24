# Уровень 2
# С помощью библиотеке matplotlib отобразить результаты на графике.

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime

url = 'https://mfd.ru/currency/?currency=USD'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Получаем таблицу
table = soup.find('table')

if table is not None:
    rows = table.find_all('tr')[1:]  # Пропускаем заголовок таблицы

    # Готовим массивы для хранения данных
    dates = []  # Массив дат
    rates = []  # Массив курсов

    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 2:
            date_str = columns[0].get_text().strip()[2:]  # Удаляем "с " в начале
            value = columns[1].get_text().strip()

            # преобразовать значение в число
            try:
                rate = float(value.replace('', ''))  # Убираем звездочки ()
                date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                dates.append(date_obj)
                rates.append(rate)
            except ValueError:
                continue  # Просто пропускаем текущую итерацию

    # График
    plt.figure(figsize=(10, 6))
    plt.plot(dates, rates, marker='o', color='blue', label='Курс доллара США')
    plt.title('Динамика курса доллара США')
    plt.xlabel('Дата')
    plt.ylabel('Курс ($)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print("Таблица не найдена.")


