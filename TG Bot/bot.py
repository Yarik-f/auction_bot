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
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Инициализация бота

bot = telebot.TeleBot('7144969796:AAFbgqLtJrnR0NYZLabca-Kd3gLpB2_bpaE')
channel_id = '@aucton_bot'

# Хранение баланса пользователей
user_balances = {}

def create_lot_button(lot_id): #Кнопки в канале
    keyboard = types.InlineKeyboardMarkup()
    button_time = types.InlineKeyboardButton("Время", callback_data=f"time_{lot_id}")
    button_info = types.InlineKeyboardButton("Инфо", callback_data="info")
    button_link = types.InlineKeyboardButton("Перейти к лоту", url=f"https://t.me/{bot.get_me().username}?start=lot_{lot_id}")
    keyboard.add(button_time, button_info)
    keyboard.add(button_link)
    return keyboard

def bot_lot_button(lot_id): #Кнопки в боте
    keyboard = types.InlineKeyboardMarkup()
    button_time = types.InlineKeyboardButton("Время", callback_data=f"time_{lot_id}")
    button_info = types.InlineKeyboardButton("Инфо", callback_data="info")
    button_bid = types.InlineKeyboardButton("Сделать ставку", callback_data=f"bid_{lot_id}")
    button_invisible_bid = types.InlineKeyboardButton("Настроить скрытую ставку", callback_data=f"invise_bid_{lot_id}")
    button_my_bid = types.InlineKeyboardButton("Предложить свою ставку", callback_data=f"my_bid_{lot_id}")
    keyboard.add(button_time, button_info)
    keyboard.add(button_bid)
    keyboard.add(button_invisible_bid)
    keyboard.add(button_my_bid)
    return keyboard
def yes_no_button(lot_id, max_bid):
    keyboard = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton("Да", callback_data=f"yes_{lot_id}:{max_bid}")
    button_no = types.InlineKeyboardButton("Нет", callback_data="no")
    keyboard.add(button_yes, button_no)
    return keyboard

def yes_no_button_my_bid(lot_id, my_bid):
    keyboard = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton("Да", callback_data=f"call_{lot_id}:{my_bid}")
    button_no = types.InlineKeyboardButton("Нет", callback_data="fold")
    keyboard.add(button_yes, button_no)
    return keyboard

def send_lot_at_time(lot_data): # Отправка картинки с переданными параметрами(картинка, текст, ...)
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


def get_members(user_id, lot_id):
    bot.send_message(user_id, f'Ваша автоставка на лот {lot_id} оказалась меньше ставки которую предложил другой пользователь')

def delete_auto_bid(lot_id):
    user_tg_id = db.get_user_tg_id_by_auto_bid(lot_id)
    db.delete_auto_bid(lot_id)
    get_members(user_tg_id, lot_id)
def update_auto_bid(my_bid, auto_bid, lot_id, bid, user_id, bid_time):
    user_auto_bid = db.get_user_id_by_auto_bid(lot_id)
    user_tg_auto_bid = db.get_user_tg_id_by_auto_bid(lot_id)
    user_tg = db.get_user_tg_id_by_bid(lot_id, user_id)
    if auto_bid > bid:
        if my_bid is None:
            db.add_bid(lot_id, user_id, bid, bid_time)
        else:
            db.update_bid_user(bid, bid_time, user_id, lot_id)
        new_bid = int(db.get_bid_lot(lot_id))
        new_bid = new_bid + 25
        if auto_bid == new_bid:
            db.update_bid_user(new_bid, bid_time, user_auto_bid, lot_id)
            bot.send_message(user_tg_auto_bid,
                             f'Ваша ставка на лот {lot_id} обновилась до {new_bid}, также Ваша автоставка дошла до придела так что будет удаленна')
            db.update_bid_user(bid, bid_time, user_auto_bid, lot_id)
            db.delete_auto_bid(lot_id)
            return new_bid
        else:
            db.update_bid_user(new_bid, bid_time, user_auto_bid, lot_id)
            db.update_auto_bid(new_bid, user_auto_bid, lot_id)
            bot.send_message(user_tg, f'Вы совершили ставку на лот {lot_id}, но у другого рользователя стоит автоставка до {auto_bid}.'
                                  f'Чтобы перебить ставку пользователя, нужно совершить ставку превышающую автоставку.'
                                  f'Для того чтобы перебить автоставку пользователя Вам нужно либо предложить свою ставку превышающию автоставку, либо поставить свою автоставку, либо пребить автоставку обычными ставками ')
            bot.send_message(user_tg_auto_bid,
                             f'Ваша ставка на лот {lot_id} обновилась до {new_bid}')
            print(new_bid)
            return new_bid
    elif auto_bid == bid:
        bot.send_message(user_tg,
                         f'Вы совершили ставку на лот {lot_id}, но у другого рользователя стоит автоставка до {auto_bid}.'
                         f'Ваша ставка не будет засчитана т.к пользователь поставил автоставку раньше Вас, при этом автоставка пользователя будет удаленна')
        bot.send_message(user_tg_auto_bid,
                         f'Ваша ставка на лот {lot_id} обновилась до {bid}, также Ваша автоставка дошла до придела так что будет удаленна')
        db.update_bid_user(bid, bid_time, user_auto_bid, lot_id)
        db.delete_auto_bid(lot_id)
        return bid
    elif auto_bid < bid:
        bot.send_message(user_tg_auto_bid,
                         f'Вашу автоставку на лот {lot_id} перебили, из-за этого она удаленна')
        db.update_bid_user(auto_bid, bid_time, user_auto_bid, lot_id)
        db.delete_auto_bid(lot_id)
        db.update_bid_user(bid, bid_time, user_id, lot_id)
        return bid

def process_bid(call): # Обработка Ставок
    lot_id = call.data.split("bid_")[1]
    bid_time = datetime.now()
    bid_time = bid_time.strftime('%Y-%m-%d %H:%M')
    username = call.from_user.username
    user_id = db.get_user_id(username)
    lot_data = db.get_lot_data_by_id(lot_id)
    message_bot_id = call.message.message_id
    message_id = db.get_message_id(lot_id)
    auto_bid = db.get_max_bid_auto_bid(lot_id)
    if message_id:
        bid = db.get_bid_lot(lot_id)
        my_bid = db.my_get_bid_lot(lot_id, user_id)
        for lot in lot_data:
            lot_id, starting_price, start_time, title, description, location, image_path = lot
            if my_bid is None:
                if bid is None:
                    db.add_bid(lot_id, user_id, starting_price, bid_time)
                    bid = db.get_bid_lot(lot_id)
                    new_bid = bid
                else:
                    new_bid = bid + 25
                    if auto_bid:
                        new_bid = update_auto_bid(my_bid, auto_bid, lot_id, new_bid, user_id, bid_time)
                    else:
                        db.add_bid(lot_id, user_id, new_bid, bid_time)
            else:
                new_bid = bid + 25
                if auto_bid:
                    new_bid = update_auto_bid(my_bid, auto_bid, lot_id, new_bid, user_id, bid_time)
                else:
                    db.update_bid_user(new_bid, bid_time, user_id, lot_id)
            message_text = (
                f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка'
                f': {new_bid + 25}\nТекущая ставка: {new_bid}')
            print(message_id)
            bot.edit_message_caption(chat_id=channel_id, message_id=message_id, caption=message_text,
                                     reply_markup=create_lot_button(lot_id))
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=message_bot_id,
                                     caption=message_text, reply_markup=bot_lot_button(lot_id))

    else:
        bot.answer_callback_query(call.id, "Лот не найден.")

    bot.answer_callback_query(call.id, f"Вы сделали ставку на лот {lot_id}")  #
def process_my_bid(call):
    lot_id = call.data.split("call_")[1].split(":")[0]
    my_call_bid = call.data.split("call_")[1].split(":")[1]
    bid_time = datetime.now()
    bid_time = bid_time.strftime('%Y-%m-%d %H:%M')
    username = call.from_user.username
    user_id = db.get_user_id(username)
    lot_data = db.get_lot_data_by_id(lot_id)
    message_id = db.get_message_id(lot_id)
    auto_bid = db.get_max_bid_auto_bid(lot_id)
    new_bid = 0
    if message_id:
        bid = db.get_bid_lot(lot_id)
        my_bid = db.my_get_bid_lot(lot_id, user_id)
        for lot in lot_data:
            lot_id, starting_price, start_time, title, description, location, image_path = lot
            if my_bid is None:
                if int(my_call_bid) <= starting_price:
                    bot.send_message(call.message.chat.id,
                                     f"Вы не иожете установить ставку для лота {lot_id}.\nТак как минимальная автоставка {starting_price}")
                else:
                    if bid is None:
                        db.add_bid(lot_id, user_id, my_call_bid, bid_time)
                        bid = db.get_bid_lot(lot_id)
                        new_bid = bid
                    else:
                        new_bid = my_call_bid
                        if auto_bid:
                            new_bid = update_auto_bid(my_bid, auto_bid, lot_id, my_call_bid, user_id, bid_time)
                        else:
                            db.add_bid(lot_id, user_id, my_call_bid, bid_time)
            else:
                new_bid = my_call_bid
                if auto_bid:
                    new_bid = update_auto_bid(my_bid, auto_bid, lot_id, my_call_bid, user_id, bid_time)
                else:
                    db.update_bid_user(my_call_bid, bid_time, user_id, lot_id)

            message_text = (
                f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка'
                f': {new_bid + 25}\nТекущая ставка: {new_bid}')
            bot.edit_message_caption(chat_id=channel_id, message_id=message_id, caption=message_text,
                                     reply_markup=create_lot_button(lot_id))
            bot.send_photo(chat_id=call.message.chat.id, photo=image_path, caption=message_text,
                           reply_markup=bot_lot_button(lot_id))

def process_auto_bid(call): #Добавление автоставки, только добавления
    lot_id = call.data.split("yes_")[1].split(":")[0]
    max_bid = call.data.split("yes_")[1].split(":")[1]
    bid_time = datetime.now()
    bid_time = bid_time.strftime('%Y-%m-%d %H:%M')
    username = call.from_user.username
    user_id = db.get_user_id(username)
    lot_data = db.get_lot_data_by_id(lot_id)
    message_id = db.get_message_id(lot_id)
    bid = db.get_bid_lot(lot_id)
    my_bid = db.my_get_bid_lot(lot_id, user_id)
    auto_bid = db.get_max_bid_auto_bid(lot_id)
    new_bid = 0
    if message_id:
        for lot in lot_data:
            lot_id, starting_price, start_time, title, description, location, image_path = lot
            if my_bid is None:
                if int(max_bid) <= starting_price:
                    bot.send_message(call.message.chat.id,
                                     f"Вы не иожете установить авто ставку для лота {lot_id}.\nТак как минимальная автоставка {starting_price + 50}")
                else:
                    if bid is None:
                        db.add_auto_bid(lot_id, user_id, max_bid, starting_price)
                        db.add_bid(lot_id, user_id, starting_price, bid_time)
                        bid = db.get_bid_lot(lot_id)
                        bot.send_message(call.message.chat.id, f"Вы установили авто ставку для лота {lot_id}.")
                    else:
                        if auto_bid is None:
                            new_bid = bid + 25
                            db.add_auto_bid(lot_id, user_id, max_bid, bid)
                            db.add_bid(lot_id, user_id, bid, bid_time)
                            bot.send_message(call.message.chat.id, f"Вы установили авто ставку для лота {lot_id}.")
                        elif auto_bid < int(max_bid):
                            delete_auto_bid(lot_id)
                            if int(max_bid) - auto_bid > 25:
                                new_bid = auto_bid + 25
                            elif int(max_bid) - auto_bid > 0 and int(max_bid) - auto_bid < 25:
                                new_bid = int(max_bid)
                            db.add_auto_bid(lot_id, user_id, max_bid, new_bid)
                            db.add_bid(lot_id, user_id, new_bid, bid_time)
                            bot.send_message(call.message.chat.id, f"Вы установили авто ставку для лота {lot_id}.")
                        else:
                            bot.send_message(call.message.chat.id, f"Вы не иожете установить авто ставку для лота {lot_id}.\nТак как минимальная автоставка доступная для это лота равнв {auto_bid + 25}")
            else:
                if auto_bid is None:
                    new_bid = bid + 25
                    db.update_bid_user(bid, bid_time, user_id, lot_id)
                    db.add_auto_bid(lot_id, user_id, max_bid, bid)
                    bot.send_message(call.message.chat.id, f"Вы установили авто ставку для лота {lot_id}.")
                elif auto_bid < int(max_bid):
                    delete_auto_bid(lot_id)
                    if int(max_bid) - auto_bid > 25:
                        new_bid = auto_bid + 25
                    elif int(max_bid) - auto_bid > 0 and int(max_bid) - auto_bid < 25:
                        new_bid = int(max_bid)
                    db.update_bid_user(new_bid, bid_time, user_id, lot_id)
                    db.add_auto_bid(lot_id, user_id, max_bid, new_bid)
                    bot.send_message(call.message.chat.id, f"Вы установили авто ставку для лота {lot_id}.")
                else:
                    bot.send_message(call.message.chat.id,
                                     f"Вы не можете установить авто ставку для лота {lot_id}.\nТак как минимальная автоставка доступная для это лота равнв {auto_bid + 25}")
            message_text = (
                f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка'
                f': {new_bid + 25}\nТекущая ставка: {new_bid}')
            bot.edit_message_caption(chat_id=channel_id, message_id=message_id, caption=message_text,
                                     reply_markup=create_lot_button(lot_id))
            bot.send_photo(chat_id=call.message.chat.id, photo=image_path, caption=message_text,
                           reply_markup=bot_lot_button(lot_id))

@bot.callback_query_handler(func=lambda call: True) #Обработка кнопок
def callback_handler(call):
    if call.data.startswith("bid_"):
        threading.Thread(target=process_bid, args=(call,)).start()
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
    elif call.data.startswith("my_bid_"):
        lot_id = call.data.split("my_bid_")[1]
        bot.send_message(call.message.chat.id, "Сколько вы хотите поставить на этот лот? Введите сумму:")
        bot.register_next_step_handler(call.message, set_my_bid, lot_id)
    elif call.data.startswith("invise_bid_"):
        lot_id = call.data.split("invise_bid_")[1]
        username = call.from_user.username
        user_id = db.get_user_id(username)
        auto_bid = db.get_auto_bid(lot_id, user_id)
        if auto_bid is None:
            bot.send_message(call.message.chat.id, "Сколько вы готовы потратить на этот лот? Введите сумму:")
            bot.register_next_step_handler(call.message, set_max_bid, lot_id)
        else:
            bot.send_message(call.message.chat.id, "На этот лот ваша авто ставка уже стоит")

    elif call.data.startswith("yes_"):
        threading.Thread(target=process_auto_bid, args=(call,)).start()
    elif call.data.startswith("call_"):
        threading.Thread(target=process_my_bid, args=(call,)).start()
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, "Вы отменили установку авто ставки.")

    elif call.data.startswith("lot_"):
        lot_id = call.data.split("lot_")[1] 
        lot_data = db.get_lot_data_by_id(lot_id) 
        if lot_data:
            for lot in lot_data:
                lot_id, starting_price, start_time, title, description, location, image_path = lot
                bid = db.get_bid_lot(lot_id)
                if bid:
                    message_text = (
                        f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка'
                        f': {bid + 25}\nТекущая ставка: {bid}')
                    bot.send_photo(chat_id=call.message.chat.id, photo=image_path, caption=message_text, reply_markup=bot_lot_button(lot_id))
                else:
                    message_text = (f'Название: {title}\nОписание: {description}\nМестоположение: {location}\nСледующая ставка'
                                        f': {starting_price}\nТекущая ставка: --')
                    bot.send_photo(chat_id=call.message.chat.id, photo=image_path, caption=message_text, reply_markup=bot_lot_button(lot_id))
        username = call.from_user.username
        user_id = db.get_user_id(username)
        bid = db.get_bid_lot(lot_id)
        my_bid = db.my_get_bid_lot(lot_id, user_id)
        bot.send_message(call.message.chat.id, f'Вы выбрали лот №{lot_id}\n'
                                                f'Ваша ставка {my_bid}\n'
                                                f'Победная ставка {bid + 25}')

def set_max_bid(message, lot_id):
    max_bid = int(message.text)

    bot.send_message(message.chat.id, f"Вы готовы потратить: {max_bid} на этот лот.\nВы готовы сделать ставку", reply_markup=yes_no_button(lot_id, max_bid))

def set_my_bid(message, lot_id):
    my_bid = int(message.text)

    bot.send_message(message.chat.id, f"Вы готовы потратить: {my_bid} на этот лот.\nВы готовы сделать ставку", reply_markup=yes_no_button_my_bid(lot_id, my_bid))

def send_auction_lot():# Получение и формирование данных о лоте + обновление через потоки для обработки в реал тайме
    processed_lots = set()

    while True:
        lots = db.get_lot_data_auction()
        for lot in lots:
            lot_id, starting_price, start_time, title, description, location, image_path = lot
            if lot_id in processed_lots:
                continue

            target_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
            time_send = datetime.now() - target_time
            if 0 <= time_send.total_seconds() <= 300: # Если время старта < нынешнего на 5 минут и меньше
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
    if "lot_" in message.text: #Отправка и изменение сообщения о лоте в боте
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
        username = message.from_user.username
        user_tg_id = message.from_user.id
        check = db.check_user(username, user_tg_id)
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
                       types.KeyboardButton('Авто-ставка'), types.KeyboardButton('Правила и помощь'),
                       types.KeyboardButton('Мои лоты'), types.KeyboardButton('Назад'))


            name = message.from_user.first_name
            bot.send_message(message.chat.id,
                             f'Привет, {name}!\nПереходи по ссылке в канал https://t.me/+qaZa5fdmZyU2NGNi:',
                             reply_markup=button)

        elif check == 2 or check == 3:
            button = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button.add(types.KeyboardButton('Добавить товар'), types.KeyboardButton('Удалить товар'),
                       types.KeyboardButton('Редактировать товар'), types.KeyboardButton('Завершить аукцион'))
            name = message.from_user.first_name
            bot.send_message(message.chat.id, f'Привет, {name}!\nВыберите действие:', reply_markup=button)

        else:
            bot.send_message(message.chat.id, f'Привет, нет данных {check}')


@bot.message_handler(func=lambda message: message.text == 'Войти как пользователь')
def user(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton('Баланс'), types.KeyboardButton('Пополнить баланс'),
               types.KeyboardButton('Авто-ставка'), types.KeyboardButton('Правила и помощь'),
               types.KeyboardButton('Мои лоты'), types.KeyboardButton('Назад'))

    bot.send_message(message.chat.id,
                     f'Чтобы принять участие в аукционах\nПереходи по ссылке в канал https://t.me/+qaZa5fdmZyU2NGNi:',
                     reply_markup=button)
@bot.message_handler(func=lambda message: message.text == 'Войти как админ')
def admin(message):
    button = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button.add(types.KeyboardButton('Добавить товар'), types.KeyboardButton('Удалить товар'),
               types.KeyboardButton('Редактировать аукцион'), types.KeyboardButton('Назад'))

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

@bot.message_handler(func=lambda message: message.text == 'Мои лоты')
def show_my_lots(message):
    username = message.from_user.username or str(message.from_user.id)  # Получаем имя пользователя или ID
    user_id = db.get_user_id(username)  # Получаем ID пользователя из базы данных
    lots = db.get_user_lots(user_id)  # Получаем все лоты, на которые пользователь сделал ставки

    if not lots:
        bot.send_message(message.chat.id, "Вы еще не сделали ставки на лоты.")
    else:
        # Отправка списка лотов
        myLots = InlineKeyboardMarkup() # Создаем переменную с кнопками 
        Lots = [] # Список для всех возможных кнопок 
        # Заполняем список всевозможными кнопками
        for s in lots:
            Buttons = InlineKeyboardButton(f'{s[1]} Лот №{s[0]}', callback_data=f"lot_{s[0]}" ) # Создаём кнопку определённого лота в котором мы участвуем    
            Lots.append(Buttons) # Добавляем кнопки в наш список  
        myLots.add(*Lots) # Заполняем нашу переменную всеми кнопками из списка       
        bot.send_message(message.chat.id,"Выбирайте 🥰",reply_markup=myLots) # Отображаем все кнопки в телеграмме    

def my():
    while True:
        t = db.lotTime()
        time.sleep(5)
        dt_now = datetime.now()
        if len(t) == 1:
            t1 = datetime.strptime(t[0][1], '%Y-%m-%d %H:%M')
            if dt_now > t1:
                p = db.history(t[0][0])
        
                bot.send_message(p[3], f"Вы выйграли в ставках на лот № {t[0][0]}")
        #

threading.Thread(target=my, daemon=True).start()


if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
