#import telebot
import json
import time
import requests

#необходимо указать токен своего бота, созданного через Botfather
#bot = telebot.TeleBot('TOKEN')

filename_articles = "articles.json"
filename_prices = "prices.json"
try:
    with open(filename_articles, encoding='utf-8') as read_art:
        articles = json.load(read_art)
except:
    articles = []

try:
    with open(filename_prices, 'r', encoding='utf-8') as read_test:
        prices = json.load(read_test)
except:
    prices = {}

def mainloop():
    while True:
        for elem in articles:
            url = 'https://card.wb.ru/cards/detail?spp=27&nm='
            r = requests.get(f"{url}{elem}").content

            text = json.loads(r)

            title = text.get('data').get('products')[0].get('name')
            price = text.get('data').get('products')[0].get('salePriceU')//100
            average_price = text.get('data').get('products')[0].get('averagePrice', 0)//100
            benefit = text.get('data').get('products')[0].get('benefit')

            if prices.get(title):
                if prices[title] > price:
                    print(f'Товар {title} подешевел на {prices[title] - price} рублей. \n'
                                                       f'Актуальная цена: {price}.\n'
                                                       f'Средняя цена на данный товар на ВБ: {average_price}\n'
                                                       f'Выгода: {benefit}%\n'
                                                       f'Ссылка на товар: https://www.wildberries.ru/catalog/{elem}/detail.aspx')
                    prices[title] = price
            else:
                prices[title] = price

            print("Gone sleep")
            time.sleep(420)

try:
    mainloop()
except KeyboardInterrupt:
    pass
with open(filename_prices, 'w', encoding='utf-8') as write_test:
    json.dump(prices, write_test, ensure_ascii=False)