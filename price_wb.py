#import telebot
import json
import time
import requests

#необходимо указать токен своего бота, созданного через Botfather
#bot = telebot.TeleBot('TOKEN')

filename_articles = "articles.json"
filename_prices = "prices.json"
def load_from_file(filename):
    try:
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = None
    return data

def mainloop():
    if not articles:
        print(f"Empty articles list. Fill {filename_articles}")
    while articles:
        for article in articles:
            url = f'https://card.wb.ru/cards/detail?spp=27&nm={article}'

            response = requests.get(url)
            if response.status_code != 200:
                print(response)
                break
            response_json = response.json()
            products = response_json['data']['products']

            product = products[0]
            title = product['name']
            brand = product['brand']
            price = product['salePriceU'] / 100

            if title in prices:
                    print(f'Товар "{title}" (от {brand}) подешевел на {prices[title] - price} рублей.\n'
                          f'Ссылка на товар: https://www.wildberries.ru/catalog/{article}/detail.aspx')
            prices[title] = price

            print("Gone sleep")
            time.sleep(420)


articles = load_from_file(filename_articles) or []
prices = load_from_file(filename_prices) or {}
try:
    mainloop()
except KeyboardInterrupt:
    print("Stopped by keyboard")
with open(filename_prices, 'w', encoding='utf-8') as write_test:
    json.dump(prices, write_test, ensure_ascii=False)