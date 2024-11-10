import threading
import time
from datetime import datetime, timedelta
import os, sys
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(project_root)
from DataBase.database import db

import telebot
from telebot import types

# Инициализация бота

channel_id = '@aucton_bot'

# Хранение баланса пользователей
user_balances = {}

def create_lot_button(lot_id):
    keyboard = types.InlineKeyboardMarkup()
    button_time = types.InlineKeyboardButton("Время", callback_data=f"time_{lot_id}")
    button_info = types.InlineKeyboardButton("Инфо", callback_data="info")
    button_link = types.InlineKeyboardButton("Перейти к лоту", url=f"https://t.me/{bot.get_me().username}?start=lot_{lot_id}")
    keyboard.add(button_time, button_info)
    keyboard.add(button_link)
    return keyboard

def bot_lot_button(lot_id):
    keyboard = types.InlineKeyboardMarkup()
    button_time = types.InlineKeyboardButton("Время", callback_data=f"time_{lot_id}")
    button_info = types.InlineKeyboardButton("Инфо", callback_data="info")
    button_bid = types.InlineKeyboardButton("Сделать ставку", callback_data=f"bid_{lot_id}")
    button_invisible_bid = types.InlineKeyboardButton("Настроить скрытую ставку", callback_data=f"bid_{lot_id}")
    button_my_bid = types.InlineKeyboardButton("Предложить свою ставку", callback_data=f"bid_{lot_id}")
    keyboard.add(button_time, button_info)
    keyboard.add(button_bid)
    keyboard.add(button_invisible_bid)
    keyboard.add(button_my_bid)
    return keyboard


def send_lot_at_time(lot_data):
    message_text, image_path, target_time, lot_id = lot_data

    delay = (target_time - datetime.now()).total_seconds()
    if delay >= 0:
        time.sleep(delay)

    if image_path.startswith('http://') or image_path.startswith('https://'):
        sent_photo = bot.send_photo(chat_id=channel_id, photo=image_path, caption=message_text, reply_markup=create_lot_button(lot_id))
        db.update_image_tg(sent_photo.photo[-1].file_id, image_path)
        msg_id = sent_photo.message_id
        db.add_message(msg_id, lot_id)
    elif os.path.isfile(image_path):
        with open(image_path, 'rb') as photo:
            sent_photo = bot.send_photo(chat_id=channel_id, photo=photo, caption=message_text, reply_markup=create_lot_button(lot_id))
            db.update_image_tg(sent_photo.photo[-1].file_id, image_path)
            msg_id = sent_photo.message_id
            db.add_message(msg_id, lot_id)
    else:
        print("Ошибка: Неверный путь к изображению")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data.startswith("bid_"):
        lot_id = call.data.split("bid_")[1]
        bid_time = datetime.now()
        bid_time = bid_time.strftime('%Y-%m-%d %H:%M')
        username = call.from_user.username
        user_id = db.get_user_id(username)
        lot_data = db.get_lot_data_by_id(lot_id)
        message_bot_id = call.message.message_id
        message_id = db.get_message_id(lot_id)
        if message_id:
            bid = db.get_bid_lot(lot_id)
            if bid is None:
                for lot in lot_data:
                    lot_id, starting_price, start_time, title, description, location, image_path = lot
                    db.add_bid(lot_id, user_id, starting_price, bid_time)
                    bid = db.get_bid_lot(lot_id)
                    message_text = (
                        f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка'
                        f': {bid + 25}\nТекущая ставка: {bid}')
                    print(message_id)
                    bot.edit_message_caption(chat_id=channel_id, message_id=message_id, caption=message_text, reply_markup=create_lot_button(lot_id))
                    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=message_bot_id, caption=message_text, reply_markup=bot_lot_button(lot_id))
            else:
                yes_bid = db.get_bid_user(user_id)
                if yes_bid:
                    for lot in lot_data:
                        lot_id, starting_price, start_time, title, description, location, image_path = lot
                        bid = bid + 25
                        db.update_bid_user(bid, bid_time, user_id)
                        message_text = (
                            f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка'
                            f': {bid + 25}\nТекущая ставка: {bid}')
                        print(
                            f"Editing message in chat_id={channel_id}, message_id={message_id}, new caption={message_text}")
                        bot.edit_message_caption(chat_id=channel_id, message_id=message_id, caption=message_text, reply_markup=create_lot_button(lot_id))
                        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=message_bot_id,
                                                 caption=message_text, reply_markup=bot_lot_button(lot_id))

                else:
                    for lot in lot_data:
                        lot_id, starting_price, start_time, title, description, location, image_path = lot
                        bid = bid + 25
                        db.add_bid(lot_id, user_id, bid, bid_time)
                        message_text = (
                            f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка'
                            f': {bid + 25}\nТекущая ставка: {bid}')
                        bot.edit_message_caption(chat_id=channel_id, message_id=message_id, caption=message_text, reply_markup=create_lot_button(lot_id))
                        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=message_bot_id,
                                                 caption=message_text, reply_markup=bot_lot_button(lot_id))

        else:
            bot.answer_callback_query(call.id, "Лот не найден.")

        bot.answer_callback_query(call.id, f"Вы сделали ставку на лот {lot_id}")
    elif call.data.startswith("time_"):
        lot_id = call.data.split("time_")[1]

        my_time = datetime.strptime(db.get_end_time(lot_id), '%Y-%m-%d %H:%M')
        end_time = my_time - datetime.now()
        all_seconds = int(end_time.total_seconds())

        days = all_seconds // 86400
        hours = (all_seconds % 86400) // 3600
        minutes = (all_seconds % 3600) // 60
        seconds = all_seconds % 60

        bot.answer_callback_query(call.id, f"Осталось {days} дней: {hours} часов: {minutes} минут: {seconds} секунд")
    elif call.data == "info":

        bot.answer_callback_query(call.id, f"После окночания торгов, победитель должен выйти на связь с продавцом самостоятельно в течении суток. Победитель обязан выкупить лот в течении 3-ех дней, после окончания аукциона.\nНЕ ВЫКУП ЛОТА -- БАН", show_alert=True)


def send_auction_lot():
    processed_lots = set()

    while True:
        lots = db.get_lot_data_auction()
        for lot in lots:
            lot_id, starting_price, start_time, title, description, location, image_path = lot
            if lot_id in processed_lots:
                continue

            target_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            time_send = datetime.now() - target_time
            if 0 <= time_send.total_seconds() <= 300:
                message = f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка: {starting_price}\nТекущая ставка: --'
                lot_data = (message, image_path, datetime.now(), lot_id)
                threading.Thread(target=send_lot_at_time, args=(lot_data,)).start()
                processed_lots.add(lot_id)
            elif target_time > datetime.now():
                message = f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка: {starting_price}\nТекущая ставка: --'
                lot_data = (message, image_path, target_time, lot_id)
                threading.Thread(target=send_lot_at_time, args=(lot_data,)).start()
                processed_lots.add(lot_id)

        time.sleep(10)

threading.Thread(target=send_auction_lot, daemon=True).start()

@bot.message_handler(commands=['start'])
def start_command(message):
    if "lot_" in message.text:
        lot_id = message.text.split("lot_")[1]
        lot_data = db.get_lot_data_by_id(lot_id)
        if lot_data:
            for lot in lot_data:
                lot_id, starting_price, start_time, title, description, location, image_path = lot

                bid = db.get_bid_lot(lot_id)
                if bid:
                    message_text = (
                        f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка'
                        f': {bid + 25}\nТекущая ставка: {bid}')
                    bot.send_photo(chat_id=message.chat.id, photo=image_path, caption=message_text, reply_markup=bot_lot_button(lot_id))
                else:
                    message_text = (f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка'
                                    f': {starting_price}\nТекущая ставка: --')
                    bot.send_photo(chat_id=message.chat.id, photo=image_path, caption=message_text, reply_markup=bot_lot_button(lot_id))
    else:
        username = message.from_user.username or str(message.from_user.id)
        check = db.check_user(username)
        print(check)
        if check == 0:
            button = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button.add(types.KeyboardButton('Войти как пользователь'), types.KeyboardButton('Войти как админ'))
            name = message.from_user.first_name
            bot.send_message(message.chat.id, f'Привет, {name}!\nКак вы хотите продолжить:', reply_markup=button)
        elif check == 1:
            user_id = message.chat.id
            if user_id not in user_balances:
                user_balances[user_id] = 0  # Изначальный баланс 0

            button = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button.add(types.KeyboardButton('Баланс'), types.KeyboardButton('Пополнить баланс'),
                       types.KeyboardButton('Авто-ставка'), types.KeyboardButton('Правила и помощь'))

            name = message.from_user.first_name
            bot.send_message(message.chat.id,
                             f'Привет, {name}!\nПереходи по ссылке в канал https://t.me/+qaZa5fdmZyU2NGNi:',
                             reply_markup=button)

        elif check == 2 or check == 3:
            button = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button.add(types.KeyboardButton('БУГАГАГАГА'), types.KeyboardButton('Пополнить баланс'),
                       types.KeyboardButton('Авто-ставка'), types.KeyboardButton('Правила и помощь'))
            name = message.from_user.first_name
            bot.send_message(message.chat.id, f'Привет, {name}!\nВыберите действие:', reply_markup=button)

        else:
            bot.send_message(message.chat.id, f'Привет, нет данных {check}')

@bot.message_handler(func=lambda message: message.text == 'Войти как пользователь')
def user(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton('Баланс'), types.KeyboardButton('Пополнить баланс'),
               types.KeyboardButton('Авто-ставка'), types.KeyboardButton('Правила и помощь'), types.KeyboardButton('Назад'))

    bot.send_message(message.chat.id, f'Чтобы принять участие в аукционах\nПереходи по ссылке в канал https://t.me/+qaZa5fdmZyU2NGNi:',
                     reply_markup=button)
@bot.message_handler(func=lambda message: message.text == 'Войти как админ')
def admin(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton('БУГАГАГАГА'), types.KeyboardButton('Пополнить баланс'),
               types.KeyboardButton('ХЗХЗХЗ'), types.KeyboardButton('Назад'))

    bot.send_message(message.chat.id, f'Ну тут еще не придумал:',
                     reply_markup=button)
@bot.message_handler(func=lambda message: message.text == 'Назад')
def back_menu(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton('Войти как пользователь'), types.KeyboardButton('Войти как админ'))
    bot.send_message(message.chat.id, f'Ну тут еще не придумал:',
                     reply_markup=button)

# Обработка для кнопки "Баланс"
@bot.message_handler(func=lambda message: message.text == 'Баланс')
def show_balance(message):
    username = message.from_user.username or str(message.from_user.id) # Определяем имя пользователя 
    balance = db.balance_db(username) # Получаем баланс пользователя из БД
    bot.send_message(message.chat.id, f'Ваш текущий баланс: {balance} у.е.') # Отправляем сообщения с балансом пользователя


# Обработка для кнопки "Пополнить баланс"
@bot.message_handler(func=lambda message: message.text == 'Пополнить баланс')
def request_deposit(message):
    msg = bot.send_message(message.chat.id, 'Введите сумму для пополнения баланса:')
    bot.register_next_step_handler(msg, deposit_balance)


# Функция для пополнения баланса
def deposit_balance(message):
    try:
        amount = float(message.text)  # Принимаем сообщения о сумме пополнения
        if amount > 0:
            username = message.from_user.username or str(message.from_user.id) # Определяем имя пользователя
            balance = db.addBalance(username, amount) # Получаем баланс пользователя из БД
            bot.send_message(message.chat.id,
                             f'Баланс успешно пополнен на {amount} у.е.\nВаш новый баланс: {balance} у.е.')  # Выводим сообщения насколько увеличен баланс  и сколько теперь на счету
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введите положительное число для пополнения баланса.')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка: введите числовое значение для пополнения баланса.')


if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
