#import telebot
import json
import time, datetime
import requests
from collections import namedtuple

Product = namedtuple("Product", ["name", "price", "brand"])
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

def fetch_info_by_article(article):
    url = f'https://card.wb.ru/cards/detail?spp=27&nm={article}'

    response = requests.get(url)
    if response.status_code != 200:
        print(response)
        return None
    response_json = response.json()
    products = response_json['data']['products']

    product = products[0]
    title = product['name']
    brand = product['brand']
    price = product['salePriceU'] / 100

    print(f'Ссылка на товар: https://www.wildberries.ru/catalog/{article}/detail.aspx')
    return Product(title, price, brand)


articles = load_from_file(filename_articles) or []
prices = load_from_file(filename_prices) or {}

try:
    today = datetime.datetime.today().strftime("%d.%m.%Y")
    if not articles:
        print(f"Empty articles list. Fill {filename_articles}")
    while articles:
        for article in articles:
            article = str(article)
            product = fetch_info_by_article(article)

            if article not in prices:
                prices[article]={}
            prices[article][today] = product.price

            print("Gone sleep")
            time.sleep(420)
except KeyboardInterrupt:
    print("Stopped by keyboard")
finally:
    print(prices)
    with open(filename_prices, 'w', encoding='utf-8') as write_test:
        json.dump(prices, write_test, ensure_ascii=False)