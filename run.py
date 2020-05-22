import requests
import graphyte
import logging
import time

logging.getLogger().setLevel(logging.INFO)

GRAPHITE_HOST = 'graphite'
CURRENCIES = ['RUB', 'EUR', 'JPY', 'CNY']
SENDER = graphyte.Sender(GRAPHITE_HOST, prefix='currencies')
BASE_URL = 'https://www.alphavantage.co/query'
API_KEY = 'your api key'


def main():
    for currency in CURRENCIES:
        resp = requests.get(BASE_URL, params={
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': currency,
            'to_currency': 'USD',
            'apikey': API_KEY
            })
        resp = resp.json()
        logging.info('Accepted response: %s', resp)
        rate = resp['Realtime Currency Exchange Rate']["5. Exchange Rate"]
        logging.info('Accepted rate: %s', rate)
        SENDER.send(currency, float(rate))


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception:
            logging.exception("Unhandled exception")
        time.sleep(60)
