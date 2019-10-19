import serial
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#conn = ser = serial.Serial('/dev/ttyyUSB0', 115200)


def obtain_targets():
    with open("targets.json") as jtargets:
        return json.load(jtargets)

def obtain_config():
    with open("config.json") as jtargets:
        return json.load(jtargets)


def start(update, context):
    keyboard = []
    targets = obtain_targets()
    for target in targets:
        keyboard.append([InlineKeyboardButton(target, callback_data=target)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose a victim', reply_markup=reply_markup)


def button(update, context):
    if update.callback_query.from_user.id in obtain_config()["admins"]:
        query = update.callback_query.data
        logger.info("Option {} chosen".format(query))
        target = obtain_targets()[query]
        info = deauth(target["ap"],target["client"], target["channel"])
        update.callback_query.edit_message_text(text="Deauthing {}\n{}".format(query, info))


def deauth(ap, client, channel):
    #conn.write(b"send deauth {} {} 0 {}").format(ap, client, channel)
    #return conn.read_all()
    return "test"

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    logger.info("Starting deautherBot")

    updater = Updater(obtain_config()["token"], use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()