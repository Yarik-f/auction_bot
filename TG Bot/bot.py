import telebot
from telebot import types
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
from py_currency_converter import convert
from _datetime import datetime


bot = telebot.TeleBot('7653723379:AAFFS0_0T7MbH5P_ubAvAcJneUKYz-HJJB0')
@bot.message_handler(commands=['start'])
def main(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton('Баланс'), types.KeyboardButton('Авто-ставка'),
               types.KeyboardButton('Правила и помощь'))

    msg = bot.send_message(message.chat.id, 'Привет!', reply_markup=button)

bot.infinity_polling()