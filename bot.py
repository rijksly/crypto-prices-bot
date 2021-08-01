from sys import argv
import requests
from time import sleep
from datetime import datetime

import telebot

try:
    key = argv[1]
except IndexError:
    print('Usage: python cryptoratesbot.py <key>')
    exit(1)
bot = telebot.TeleBot(key)

users = {}

def compound(name):
    return name['data']['name'] + ': ' + str(round(name['data']['market_data']['price_usd'], 2)) + ', ' + str(round(name['data']['market_data']['percent_change_usd_last_24_hours'], 2)) + '%\n'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'This bot once a day sends BTC/USD, ETH/USD and DOGE/USD price and price change')

@bot.message_handler(commands=['startthis'])
def startthis(message):
    users[message.from_user.id] = True
    while users[message.from_user.id]:
        btc = requests.get('https://data.messari.io/api/v1/assets/btc/metrics/market-data').json()
        eth = requests.get('https://data.messari.io/api/v1/assets/eth/metrics/market-data').json()
        doge = requests.get('https://data.messari.io/api/v1/assets/doge/metrics/market-data').json()

        mess = compound(btc) + compound(eth) + compound(doge)
        bot.send_message(message.from_user.id, mess)

        print('Sent to @' + message.from_user.username + ', id: ' + str(message.from_user.id) + ' ' + str(datetime.now()))

        sleep(60*60*24)

@bot.message_handler(commands=['stop'])
def stop(message):
    users[message.from_user.id] = False

bot.infinity_polling()
