import telebot
from telebot import types

token = '5572267888:AAEXv1yvL4oDLbaG8Lzd4fNH3cDnF8Luz-k'
bot = telebot.TeleBot(token)

k1 = "-----"
k2 = "-----"
k3 = "-----"
k4 = "-----"
k5 = "-----"
k6 = "-----"
kz1 = 0
kz2 = 0
kz3 = 0
kz4 = 0
kz5 = 0
kz6 = 0
item1 = types.KeyboardButton(k1)
item2 = types.KeyboardButton(k2)
item3 = types.KeyboardButton(k3)
item4 = types.KeyboardButton(k4)
item5 = types.KeyboardButton(k5)
item6 = types.KeyboardButton(k6)
item7 = types.KeyboardButton("Изменить категорию")
izm = False

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')

@bot.message_handler(commands=['button'])
def button_message(message):
    global izm
    izm = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    markup.add(item6)
    markup.add(item7)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Изменить категорию":
        global izm
        global k1
        global k2
        global k3
        global k4
        global k5
        global k6
        global kz1
        global kz2
        global kz3
        global kz4
        global kz5
        global kz6
        bot.send_message(message.chat.id, "Все категории", reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(message.chat.id, "Выберите для изменения(Выйти: /button)", reply_markup=markup)
        izm = True
    if message.text == k1:
      if izm:
        k1 = message.text
        izm = False
      else:
        kz1 += message.text
        bot.send_message(message.chat.id, "Ваши затраты в категории:" + k1 + ' : ' + kz1)
    if message.text == k2:
      if izm:
        k2 = message.text
        izm = False
      else:
        kz2 += message.text
        bot.send_message(message.chat.id, "Ваши затраты в категории:" + k2 + ' : ' + kz2)
    if message.text == k3:
      if izm:
        k3 = message.text
        izm = False
      else:
        kz3 += message.text
        bot.send_message(message.chat.id, "Ваши затраты в категории:" + k3 + ' : ' + kz3)
    if message.text == k4:
      if izm:
        k4 = message.text
        izm = False
      else:
        kz4 += message.text
        bot.send_message(message.chat.id, "Ваши затраты в категории:" + k4 + ' : ' + kz4)
    if message.text == k5:
      if izm:
        k5 = message.text
        izm = False
      else:
        kz5 += message.text
        bot.send_message(message.chat.id, "Ваши затраты в категории:" + k5 + ' : ' + kz5)
    if message.text == k6:
      if izm:
        k6 = message.text
        izm = False
      else:
        kz6 += message.text
        bot.send_message(message.chat.id, "Ваши затраты в категории:" + k6 + ' : ' + kz6)

bot.infinity_polling()