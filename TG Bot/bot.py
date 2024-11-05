import telebot
from telebot import types

from DataBase.database import db



bot = telebot.TeleBot('7653723379:AAFFS0_0T7MbH5P_ubAvAcJneUKYz-HJJB0')


def add_user(username):
    db.add_user(username)
@bot.message_handler(commands=['start'])
def main(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton('Баланс'), types.KeyboardButton('Авто-ставка'),
               types.KeyboardButton('Правила и помощь'))

    msg = bot.send_message(message.chat.id, 'Привет!', reply_markup=button)

    username = message.from_user.username or str(message.from_user.id)
    add_user(username)

bot.infinity_polling()