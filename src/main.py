import requests
from datetime import datetime
import json
import os


API_KEY = os.getenv('VARIABLE_NAME')
CURRENCY_RATES_FILE = "currency_rates.json"
def main():
    while True:
        currency = input("Введите название валюты(EUR, USD): ")
        if currency not in ["USD", "EUR", ""]:
            print("Некоректный ввод")

        rate = get_currency_rate(currency)
        timesamp = datetime.now()

        print(f'Курс {currency} к рублю {rate}')

        data = {'currency': currency, 'rate': rate, 'timestamp': timesamp.strftime("%Y-%m-%d %H")}
        save_to_json(data)

        choice = input('Выберите действие: 1 - Пролдолжить 2 - Выйти\n>')
        if choice == '1':
            continue
        elif choice == '2':
            break
        else:
            print("Некорректный ввод")
def get_currency_rate(base: str) -> float:
    'Получает Курс от API и возвращает его валюту'
    url = "https://api.apilayer.com/exchangerates_data/latest"

    response = requests.get(url, headers={'apikey': API_KEY}, params={'base': base})
    rate = response.json()['rates']['RUB']
    status_code = response.status_code
    result = response.text
    return rate

def save_to_json(data: dict) -> None:
    '''Сохраняет данные в json файл'''
    with open(CURRENCY_RATES_FILE, 'a') as file:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], file)
        else:
            with open(CURRENCY_RATES_FILE) as file:
                data_list = json.load(file)
                data_list.append(data)
            with open(CURRENCY_RATES_FILE, 'w') as file:
                json.dump(data_list, file)


if __name__ == "__main__":
    main()