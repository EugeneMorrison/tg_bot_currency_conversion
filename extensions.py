import requests
import json
from config import CURRENCIES


class APIException(Exception):
    """Custom exception for user-related errors."""
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> float:
        if base == quote:
            raise APIException(f'Невозможно перевести одинаковые валюты: {base}.')

        try:
            base_ticker = CURRENCIES[base.lower()]
        except KeyError:
            raise APIException(f'Не удалось найти валюту "{base}".')

        try:
            quote_ticker = CURRENCIES[quote.lower()]
        except KeyError:
            raise APIException(f'Не удалось найти валюту "{quote}".')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество: "{amount}".')

        url = f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}'
        response = requests.get(url)

        try:
            price = json.loads(response.content)[quote_ticker]
        except KeyError:
            raise APIException('Ошибка при получении курса валют.')

        return round(price * amount, 4)