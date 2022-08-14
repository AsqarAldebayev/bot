import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from settings import *

bot = telebot.TeleBot(token, threaded=False)


@bot.message_handler(commands=['start'])
def start(message):
    catalogKBoard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    murojaatlar = KeyboardButton(text="Murojaat yo'llash")
    takliflar = KeyboardButton(text="Taklif yuborish")
    anonim = KeyboardButton(text="Anonim murojaat")
    catalogKBoard.add(murojaatlar, takliflar, anonim)
    if message.chat.id in ADMINISTRATOR_ID:
        bot.send_message(
            chat_id=message.chat.id,
            text='Бот муваффақиятли ишга туширилди🎉')
        return
    bot.send_message(
        message.chat.id,
        text="Ассалому алайкум!\nЭлликкалъа тумани истеъмолчилар ҳуқуқини ҳимоя қилиш жамияти телеграмм ботига хуш "
             "келибсиз. \n\nМурожаатингизни йўллашингиз мумкин".format(),
        reply_markup=catalogKBoard)


bot.infinity_polling()
