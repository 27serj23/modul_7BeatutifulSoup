# Уровень 1
# С помощью библиотеки beautifulsoup4 получить с сайта
# http://mfd.ru/currency/?currency=USD
# (http://mfd.ru/currency/?currency=USD) данные о курсе доллара в разные моменты времени.
# Можно с любого другого сайта, если с этим окажется неудобно работать

"""
Модуль для сбора, парсинга и представления данных о курсах валют с сайта MFD.
Модуль предоставляет гибкую систему для работы с финансовыми данными,
построенную на принципах ООП и разделения ответственности.
Основные компоненты:
- DataFetcher: абстракция для получения данных
- DataParser: абстракция для парсинга данных
- DataFormatter: абстракция для форматирования вывода
- CurrencyService: сервис для оркестрации процесса
Пример использования:
     from currency_parser import CurrencyService, MFDDataFetcher, MFDCurrencyParser, TableFormatter
     service = CurrencyService(MFDDataFetcher(), MFDCurrencyParser())
     rates = service.get_currency_rates()
     formatter = TableFormatter()
     print(formatter.format(rates))
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import requests
from bs4 import BeautifulSoup

@dataclass
class CurrencyRate:
    """
    Data Transfer Object (DTO) для представления данных о курсе валюты.
    Используется для передачи структурированных данных между компонентами системы
    без привязки к источнику данных или формату вывода.
    Атрибуты:
        date (str): Дата в формате строки
        rate (str): Значение курса валюты
        change (str): Изменение курса по сравнению с предыдущим периодом
    """
    date: str
    rate: str
    change: str

class DataFetcher(ABC):
    """
    Абстрактный базовый класс для получения данных.
    Определяет интерфейс для всех классов-источников данных.
    Реализации могут получать данные из различных источников:
    веб-сайтов, API, файлов, баз данных и т.д.
    """

    @abstractmethod
    def fetch_data(self) -> str:
        """
        Получить сырые данные из источника.
        Returns:
            str: Сырые данные в строковом формате (HTML, JSON, XML, etc.)
        Raises:
            ConnectionError: При проблемах с подключением к источнику
            TimeoutError: При превышении времени ожидания
            Exception: Другие ошибки, специфичные для реализации
        """
        pass

class MFDDataFetcher(DataFetcher):
    """
    Конкретная реализация DataFetcher для получения данных с сайта MFD.
    Отправляет HTTP GET запрос к указанному URL и возвращает HTML контент.
    """

    def __init__(self, url: str = 'https://mfd.ru/currency/?currency=USD'):
        """
        Инициализация фетчера.
        Args:
            url (str): URL целевой страницы с курсами валют. По умолчанию - страница USD.
        """
        self.url = url

    def fetch_data(self) -> str:
        """
        Получить HTML контент с сайта MFD.
        Returns:
            str: HTML код страницы в виде строки
        Raises:
            requests.RequestException: При ошибках сетевого запроса
            requests.HTTPError: При HTTP ошибках (404, 500, etc.)
        """
        response = requests.get(self.url)
        response.raise_for_status()  # Выбрасывает исключение для HTTP ошибок
        return response.text

class DataParser(ABC):
    """
    Абстрактный базовый класс для парсинга данных.
    Определяет интерфейс для всех классов-парсеров.
    Реализации могут парсить различные форматы данных: HTML, JSON, XML, CSV и т.д.
    """

    @abstractmethod
    def parse(self, html: str) -> List[CurrencyRate]:
        """
        Преобразовать сырые данные в структурированный формат.
        Args:
            html (str): Сырые данные для парсинга
        Returns:
            List[CurrencyRate]: Список объектов CurrencyRate с распарсенными данными
        Raises:
            ValueError: При невозможности распарсить данные
            Exception: Другие ошибки парсинга, специфичные для реализации
        """
        pass

class MFDCurrencyParser(DataParser):
    """
    Конкретная реализация DataParser для парсинга таблицы курсов валют с MFD.
    Использует BeautifulSoup для извлечения данных из HTML таблицы.
    """

    def parse(self, html: str) -> List[CurrencyRate]:
        """
        Распарсить HTML и извлечь данные о курсах валют.
        Args:
            html (str): HTML код страницы
        Returns:
            List[CurrencyRate]: Список объектов CurrencyRate
        Raises:
            ValueError: Если таблица с курсами не найдена в HTML
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Ищем таблицу с курсами валют по классу
        # Примечание: класс 'mfd-table' может измениться на сайте -
        # в реальном проекте нужно предусмотреть обработку таких изменений
        table = soup.find('table', class_='mfd-table')

        if not table:
            raise ValueError("Таблица с курсами не найдена в HTML контенте")

        rates = []
        # Пропускаем заголовок таблицы (первая строка) и обрабатываем данные
        rows = table.find_all('tr')[1:]

        for row in rows:
            columns = row.find_all('td')
            # Проверяем, что строка содержит ожидаемое количество колонок
            if len(columns) == 3:
                rate = CurrencyRate(
                    date=columns[0].get_text().strip(),  # Дата
                    rate=columns[1].get_text().strip(),  # Курс
                    change=columns[2].get_text().strip()  # Изменение
                )
                rates.append(rate)

        return rates

class DataFormatter(ABC):
    """
    Абстрактный базовый класс для форматирования вывода данных.
    Определяет интерфейс для всех классов-форматеров.
    Реализации могут предоставлять различные форматы вывода:
    табличный, JSON, CSV, графический и т.д.
    """

    @abstractmethod
    def format(self, rates: List[CurrencyRate]) -> str:
        """
        Преобразовать структурированные данные в строку для вывода.
        Args:
            rates (List[CurrencyRate]): Список данных о курсах валют
        Returns:
            str: Отформатированная строка для вывода
        """
        pass

class TableFormatter(DataFormatter):
    """
    Конкретная реализация DataFormatter для табличного вывода данных.
    Форматирует данные в виде читаемой текстовой таблицы с выравниванием колонок.
    """

    def format(self, rates: List[CurrencyRate]) -> str:
        """
        Форматировать данные в виде текстовой таблицы.
        Args:
            rates (List[CurrencyRate]): Список данных о курсах валют
        Returns:
            str: Отформатированная таблица в виде строки
        """
        if not rates:
            return "Нет данных для отображения"

        # Заголовок таблицы с выравниванием
        header = "Дата".ljust(15) + " |" + "Курс".rjust(10) + "  |" + "Изменение".rjust(10)
        separator = "-" * 40  # Разделительная линия
        lines = [header, separator]

        # Данные таблицы
        for rate in rates:
            line = f"{rate.date.ljust(15)} | {rate.rate.rjust(10)} | {rate.change.rjust(10)}"
            lines.append(line)

        return "\n".join(lines)

class CurrencyService:
    """
    Сервис для работы с курсами валют.
    Осуществляет оркестрацию процесса: получение, парсинг и возврат данных.
    Реализует паттерн "Фасад", предоставляя простой интерфейс для сложной системы.
    """

    def __init__(self, fetcher: DataFetcher, parser: DataParser):
        """
        Инициализация сервиса с внедрением зависимостей.
        Args:
            fetcher (DataFetcher): Объект для получения данных
            parser (DataParser): Объект для парсинга данных
        """
        self.fetcher = fetcher
        self.parser = parser

    def get_currency_rates(self) -> List[CurrencyRate]:
        """
        Получить актуальные курсы валют.
        Returns:
            List[CurrencyRate]: Список данных о курсах валют
        Raises:
            Exception: Любые ошибки, возникшие в процессе получения или парсинга данных
        """
        html = self.fetcher.fetch_data()
        return self.parser.parse(html)

def main():
    """
    Основная функция программы.
    Демонстрирует использование всех компонентов системы:
    1. Создание и компоновка зависимостей
    2. Получение и обработка данных
    3. Форматирование и вывод результатов
    4. Обработка возможных ошибок
    """
    try:
        # Компоновка зависимостей (Dependency Injection Pattern)
        # Это позволяет легко заменять компоненты без изменения основной логики
        fetcher = MFDDataFetcher()
        parser = MFDCurrencyParser()
        formatter = TableFormatter()

        # Создание сервиса с внедренными зависимостями
        service = CurrencyService(fetcher, parser)

        # Получение и обработка данных
        rates = service.get_currency_rates()

        # Вывод результатов
        print(formatter.format(rates))
        print(f"\nУспешно получено {len(rates)} записей")

    except requests.RequestException as e:
        # Ошибки сетевого запроса
        print(f"Ошибка при получении данных: {e}")
        print("Проверьте подключение к интернету и доступность сайта")
    except ValueError as e:
        # Ошибки парсинга (не найден ожидаемый элемент)
        print(f"Ошибка при обработке данных: {e}")
        print("Возможно, изменилась структура сайта - требуется обновление парсера")
    except Exception as e:
        # Все остальные непредвиденные ошибки
        print(f"Неожиданная ошибка: {e}")
        print("Обратитесь к разработчику для решения проблемы")

# Точка входа в программу
if __name__ == "__main__":
    main()




