import telebot
from telebot import types
from py_currency_converter import convert
from _datetime import datetime

#словарь для хранения балансов пользователей
user_balances = {}

bot = telebot.TeleBot('7653723379:AAFFS0_0T7MbH5P_ubAvAcJneUKYz-HJJB0')

@bot.message_handler(commands=['start'])
def main(message):
    # баланс пользователя, если он не задан
    if message.chat.id not in user_balances:
        user_balances[message.chat.id] = 0  # Начальный баланс 0

    #кнопки для главного меню
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton('Баланс'), types.KeyboardButton('Авто-ставка'),
               types.KeyboardButton('Правила и помощь'))

    bot.send_message(message.chat.id, 'Привет! Выберите опцию ниже.', reply_markup=button)

@bot.message_handler(func=lambda message: message.text == 'Баланс')
def balance(message):
    #текущий баланс
    balance = user_balances.get(message.chat.id, 0)
    msg = bot.send_message(message.chat.id, f"Ваш баланс: {balance} руб.\nВведите сумму для пополнения:")
    bot.register_next_step_handler(msg, deposit)

def deposit(message):
    try:
        #введенное значение в число
        amount = float(message.text)
        if amount > 0:
            # Обновления баланса пользователя
            user_balances[message.chat.id] += amount
            bot.send_message(message.chat.id, f"Баланс успешно пополнен на {amount} руб.\n"
                                              f"Ваш текущий баланс: {user_balances[message.chat.id]} руб.")
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите положительную сумму для пополнения.")
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Пожалуйста, введите корректную сумму.")

bot.infinity_polling()