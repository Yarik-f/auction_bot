import telebot
from telebot import types
from py_currency_converter import convert
from _datetime import datetime

#бот
bot = telebot.TeleBot('7653723379:AAFFS0_0T7MbH5P_ubAvAcJneUKYz-HJJB0')

#Хранение баланса пользователей
user_balances = {}


@bot.message_handler(commands=['start'])
def main(message):
    user_id = message.chat.id
    if user_id not in user_balances:
        user_balances[user_id] = 0  # Изначальный баланс 0

    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton('Баланс'), types.KeyboardButton('Пополнить баланс'),
               types.KeyboardButton('Авто-ставка'), types.KeyboardButton('Правила и помощь'))

    bot.send_message(message.chat.id, 'Привет! Выберите действие:', reply_markup=button)


# Обработка для кнопки "Баланс"
@bot.message_handler(func=lambda message: message.text == 'Баланс')
def show_balance(message):
    user_id = message.chat.id
    balance = user_balances.get(user_id, 0)  # Получаем баланс пользователя или 0, если его нет
    bot.send_message(message.chat.id, f'Ваш текущий баланс: {balance} у.е.')


# Обработчик для кнопки "Пополнить баланс"
@bot.message_handler(func=lambda message: message.text == 'Пополнить баланс')
def request_deposit(message):
    msg = bot.send_message(message.chat.id, 'Введите сумму для пополнения баланса:')
    bot.register_next_step_handler(msg, deposit_balance)


# Функция для пополнения баланса
def deposit_balance(message):
    try:
        user_id = message.chat.id
        amount = float(message.text)  #
        if amount > 0:
            user_balances[user_id] = user_balances.get(user_id, 0) + amount
            bot.send_message(message.chat.id,
                             f'Баланс успешно пополнен на {amount} у.е.\nВаш новый баланс: {user_balances[user_id]} у.е.')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введите положительное число для пополнения баланса.')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка: введите числовое значение для пополнения баланса.')


bot.infinity_polling()
