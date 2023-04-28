import telebot
import googletrans
from telebot import types # для указание типов

bot = telebot.TeleBot("5693296256:AAFQsYHKkbIKMhpKF8mYbTvL09hjpyt0Uyc") # токен лежит в файле config.py

@bot.message_handler(commands=['start']) #создаем команду
def start(message):
    markup = types.InlineKeyboardMarkup()
    for i, name in enumerate(googletrans.LANGUAGES.keys()):
        button = types.InlineKeyboardButton(str(name))
        markup.add(button)
        break
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Нажми на кнопку и перейди на сайт)".format(message.from_user), reply_markup=markup)
bot.polling(none_stop=True)