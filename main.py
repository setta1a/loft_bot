import datetime
import logging
import os
import random
import hashlib
from typing import List
from aiogram.dispatcher.filters import MediaGroupFilter
from aiogram.types import ContentType, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, types, executor


API_TOKEN = "6136347228:AAFHIdMcQrbbuUXr2JzYbmIUNkTzXPakVS8"

admin_id = "6420712889"

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    try:
        st = str(message["from"].username) + " " + str(message["from"].id)
        print(1)
    except:
        st = message.chat.id
        print(2)

    button1 = types.InlineKeyboardButton("Точно приду", callback_data=f'1 {st}')
    button2 = types.InlineKeyboardButton("Скорее всего приду", callback_data=f'2 {st}')
    keyboard.add(button1, button2)


    await bot.send_message(chat_id=message.chat.id,
                               text="*** Привет, это макс пэ напиши текст ***",
                               parse_mode="Markdown",
                               reply_markup=keyboard)


@dp.callback_query_handler(lambda c: c.data)
async def process_callback(callback_query: types.CallbackQuery):
    # Обработка нажатия на кнопку
    f = open("members.txt", "r")
    arr = f.readlines()
    usr = callback_query.data.split()
    f.close()
    f = open("members.txt", "a")
    print(usr)
    if usr[0] == '1':
        st = "@" + usr[1] + " Точно идёт" + "\n"
    elif usr[0] == '2':
        st = "@" + usr[1] + " Скорее всего идёт" + "\n"

    if st not in arr:
        await bot.send_message(usr[-1], "***Вы добавлены в лист ожидания ***", parse_mode="Markdown")
        f.write(st)
    else:
        await bot.send_message(usr[-1], "***Вы уже добавлены в лист ожидания ***", parse_mode="Markdown")


    f.close()


@dp.message_handler(commands=['members'])
async def members(message: types.Message):
    if str(message["from"].id) == admin_id:
        f = open("members.txt").readlines()
        st = "\n".join(f)

        prob1 = st.count("Точно идёт")
        prob2 = st.count("Скорее всего идёт")
        st = f' ***Точно идёт*** : {prob1}\n***Скорее всего идёт*** : {prob2}\n\n' + st

        await bot.send_message(admin_id, st, parse_mode="Markdown")
    else:
        await bot.send_message(message.chat.id, "**Вы не явялетесь администратором данного бота**")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)