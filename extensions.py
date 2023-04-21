import requests
import json
from config import headers

keys = {
    'Доллар' : 'USD',
    'Рубль' : 'RUB',
    'Евро' : 'EUR',
    'Юань' : 'CNY',
    'Йена' : 'JPY'
}

value_keys = {
    'Доллар' : '$',
    'Рубль' : '₽',
    'Евро' : '€',
    'Юань' : '¥',
    'Йена' : '¥'
}

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(message):
        query = message.text.title().split()

        if len(query) != 3:
            raise APIException('Некорректный ввод. Введите 3 параметра.\n/help')

        base, quote, amount = query

        if base not in keys:
            raise APIException(f'К сожалению, не удалось обработать валюту: "{base}"\n/values')

        if quote not in keys:
            raise APIException(f'К сожалению, не удалось обработать валюту: "{quote}"\n/values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать сумму: "{amount}"\n/help')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={keys[quote]}&from={keys[base]}&amount={amount}"
        response = requests.get(url, headers=headers)
        result = json.loads(response.content)["result"]
        text = f'{amount} {value_keys[base]} = {result} {value_keys[quote]}'
        return text
