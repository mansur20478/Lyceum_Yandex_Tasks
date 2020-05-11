# -*- coding: utf-8 -*-
import datetime, random, json, requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler

TOKEN = "822970120:AAG3G4OSG0I1XUqUh45MwkHrEa7PZjb6TeU"


sender_info = {}


def start(update, context):
    buttons = [
        ['/change_lang', '/trans'],
    ]
    markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=False)
    update.message.reply_text("Здраствуйте, /trans текс для перевода текста\n"
                              "/change_lang что бы сменить сторону перевода", reply_markup=markup)


def change_lang(update, context):
    buttons = [
        ['/change_lang', '/trans'],
    ]
    markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=False)
    chat_id = update.message.chat_id
    if chat_id not in sender_info or sender_info[chat_id] == "ru-en":
        sender_info[chat_id] = "en-ru"
    else:
        sender_info[chat_id] = "ru-en"
    update.message.reply_text(f"Готово, теперь {sender_info[chat_id]}", reply_markup=markup)


def trans(update, context):
    buttons = [
        ['/change_lang', '/trans'],
    ]
    markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=False)
    chat_id = update.message.chat_id
    if len(context.args) == 0:
        update.message.reply_text("Введи текст", reply_markup=markup)
        return
    if chat_id not in sender_info:
        sender_info[chat_id] = "ru-en"
    params = {
        'key': 'trnsl.1.1.20200510T063837Z.9d452e880ab33516.ac524792a3446e1ae81742675030dde8fa99134e',
        'text': ' '.join(context.args),
        'lang': sender_info[chat_id]
    }
    info = requests.get("https://translate.yandex.net/api/v1.5/tr.json/translate", params=params).json()
    print(info)
    update.message.reply_text(info['text'][0], reply_markup=markup)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('change_lang', change_lang))
    dp.add_handler(CommandHandler('trans', trans))
    updater.start_polling()
    updater.idle()


running = -1
data = []
ans, was = 0, 0
if __name__ == '__main__':
    main()
