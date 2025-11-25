# Уровень 2
# С помощью библиотеке matplotlib отобразить результаты на графике.

"""
Скрипт для получения и визуализации данных о курсе доллара США с сайта mfd.ru.
Цель: Показать динамику изменений курса доллара США в графическом виде.
Используются библиотеки: Requests, Beautiful Soup, Matplotlib.

Последовательность шагов:
1. Отправляется запрос на сайт для получения HTML-контента.
2. Парсим полученный HTML-документ с помощью BeautifulSoup.
3. Извлекаем данные из таблицы на странице.
4. Преобразуем полученные данные в пригодный для построения графика формат.
5. Создаем график с помощью Matplotlib.

Дата: Текущая дата
Версия: 1.0
"""

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime

# Шаг 1: Запрашиваем данные с сайта
url = 'https://mfd.ru/currency/?currency=USD'
response = requests.get(url)

# Шаг 2: Создаем объект BeautifulSoup для парсинга HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Шаг 3: Поиск таблицы с нужными данными
table = soup.find('table')

if table is not None:
    # Шаг 4: Извлечение строк из таблицы, пропуская первый ряд (заголовок)
    rows = table.find_all('tr')[1:]

    # Подготовим массивы для хранения данных
    dates = []  # Список дат
    rates = []  # Список значений курса доллара

    # Проход по каждой строке таблицы
    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 2:  # Проверяем, достаточно ли колонок
            # Чистка и подготовка данных
            date_str = columns[0].get_text().strip()[2:]  # Убираем лишнюю букву "с" и пробелы
            value = columns[1].get_text().strip()  # Чистим значение курса

            # Попытка преобразования в число (если возникают ошибки — пропустим данную запись)
            try:
                rate = float(value.replace('*', ''))  # Преобразуем строку в число, удаляя звездочку *
                date_obj = datetime.strptime(date_str, '%d.%m.%Y')  # Приводим дату к формату datetime
                dates.append(date_obj)  # Сохраняем объект даты
                rates.append(rate)  # Сохраняем значение курса
            except ValueError:
                continue  # Продолжаем цикл, пропустив неудачную запись

    # Шаг 5: Создание графика с помощью Matplotlib
    plt.figure(figsize=(10, 6))  # Настройка размера окна графика
    plt.plot(dates, rates, marker='o', color='blue', label='Курс доллара США')  # Линия графика с точками-маркерами
    plt.title('Динамика курса доллара США')  # Заголовок графика
    plt.xlabel('Дата')  # Название оси X
    plt.ylabel('Курс ($)')  # Название оси Y
    plt.grid(True)  # Включаем сеточную разметку
    plt.legend()  # Отображаем легенду
    plt.tight_layout()  # Оптимизация компоновки элементов
    plt.show()  # Отображение графика
else:
    print("Таблица не найдена.")  # Сообщение об отсутствии таблицы



