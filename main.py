from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, CallbackQuery, MenuButton, \
    InlineKeyboardMarkup, ReplyKeyboardMarkup, InlineKeyboardButton, Message
from telegram.ext import CallbackContext, CommandHandler, Updater, MessageHandler, Filters, InlineQueryHandler

import logging

from environs import Env


env = Env()
env.read_env(override=True)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def start(update: Update, context: CallbackContext):
    like = InlineKeyboardButton(text='Я согласен', callback_data=msg)
    dislike = InlineKeyboardButton(text='Откажусь', callback_data=msg)
    likes = InlineKeyboardMarkup(inline_keyboard=[[like], [dislike]])
    msg = context.bot.send_message(chat_id=update.effective_chat.id, text="Привет. Мы собираем личные данные",
                                   reply_markup=likes)


def menu(update: Update, context: CallbackContext):
    like = InlineKeyboardButton(text='Like', callback_data='start')
    dislike = InlineKeyboardButton(text='Dislike', callback_data='meta')
    likes = InlineKeyboardMarkup(inline_keyboard=[[like], [dislike]])

    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.blizzstatic.com%2Fdynamicmedia%2Fimage%2F115%2F5838e223c5d7a.jpg%3Fw%3D1200%26zc%3D1&f=1&nofb=1",
        reply_markup=likes
    )


def registr(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ваше имя')

    # context.bot.send_message(chat_id=update.effective_chat.id, text='Введите фамилию:')
    # print(update.message.text)


def caps(update: Update, context: CallbackContext):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def inline_caps(update: Update, context: CallbackContext):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def reply(chat_id, text):
    print("Привет! Пользователь с ID {} написал мне: {}".format(chat_id, text))


updater = Updater(env.str("TG_TOKEN"), use_context=True)
dispatcher = updater.dispatcher

inline_caps_handler = InlineQueryHandler(inline_caps)

start_handler = CommandHandler('start', start)
menu_handler = CommandHandler('menu', menu)
registr_handler = MessageHandler('registr', registr)
# print(echo_handler)
dispatcher.add_handler(registr_handler)
caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

dispatcher.add_handler(start_handler)

dispatcher.add_handler(menu_handler)

updater.start_polling()
