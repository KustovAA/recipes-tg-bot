import logging

from environs import Env
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

logging.basicConfig(
    filename='app.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

AGREEMENT, NAME, PHONE_NUMBER, EMAIL = range(4)


def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Согласен', 'Я против']]

    update.message.reply_text(
        'Привет, мы собираем личные данные',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
            input_field_placeholder='Согласен or Я против?'
        ),
    )

    return AGREEMENT


def agreement(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Agreement of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Напишите вашу Фамилию Имя',
        reply_markup=ReplyKeyboardRemove(),
    )

    return NAME


def name(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Name of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Прекрасно. Теперь напишите ваш номер телефона'
    )

    return PHONE_NUMBER


def phone_number(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Phone number of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Отлично. И последнее, напишите ваш email'
    )

    return EMAIL


def email(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("Email of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Спасибо. Добро пожаловать в наше царство блюд=))'
    )
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.',
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    env = Env()
    env.read_env(override=True)
    updater = Updater(env.str("TG_TOKEN"))
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            AGREEMENT: [MessageHandler(
                Filters.regex('^(Согласен|Я против)$'),
                agreement)],
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            PHONE_NUMBER: [
                MessageHandler(Filters.text & ~Filters.command, phone_number)
            ],
            EMAIL: [MessageHandler(Filters.text & ~Filters.command, email)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
