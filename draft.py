chat_id = message.chat.id
markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
itembtn1 = types.KeyboardButton('addd')
itembtn2 = types.KeyboardButton('vewdf')
itembtn3 = types.KeyboardButton('dferws')
markup.add(itembtn1, itembtn2, itembtn3)
bot.send_message(chat_id, "Choose one letter:", reply_markup=markup)



import telebot
from telebot import types

bot = telebot.TeleBot("5693296256:AAFQsYHKkbIKMhpKF8mYbTvL09hjpyt0Uyc")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	chat_id = message.chat.id
	bot.send_message(message.chat.id, "Choose language please")
	markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
	btn1 = types.KeyboardButton('Русский')
	btn2 = types.KeyboardButton('English')
	markup.add(btn1, btn2)
	if message.text == 'Russian':
		bot.send_message(chat_id, f'Хорошо', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def send_all(message):
	pass

# ----------------------------------------------------------------------------------
bot.infinity_polling()


#=====================================================
import telebot
from telebot import types

bot = telebot.TeleBot("5693296256:AAFQsYHKkbIKMhpKF8mYbTvL09hjpyt0Uyc")


class WrongWord(Exception):
	pass

class TextWithoutWords(Exception):
	pass


class User:
	def __init__(self, slovar, level='A1', mix=True):
		self.slovar = slovar
		self.level = level
		self.mix = mix
user = User({'choose_language': 'Хорошо',
					  'error': 'Произошла ошибка. Попробуйте ещё раз',
					  'choose_level': 'Выберите уровень сложности слов',
					  'wrong_word': 'Выберите один из вариантов и попробуй снова',
					  'mix_question': 'Перемешать текст?',
					  'yes': 'Да',
					  'no': 'Нет',
					  'send_scenario': 'Скиньте сам текст',
					  'text_without_words': 'Вы скинули текст без слов'})


@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(selective=True)
	btn1 = types.KeyboardButton('Русский')
	btn2 = types.KeyboardButton('English')
	markup.add(btn1, btn2)
	bot.send_message(message.chat.id, "Choose language", reply_markup=markup)
	bot.register_next_step_handler(message, choose_language)
	return


@bot.message_handler(func=lambda message: True)
def send_all(message):
	pass


def choose_language(message):
	global user
	chat_id = message.chat.id
	try:
		if message.text == 'Русский':
			slovar = {'choose_language': 'Хорошо',
					  'error': 'Произошла ошибка. Попробуйте ещё раз',
					  'choose_level': 'Выберите уровень сложности слов',
					  'wrong_word': 'Выберите один из вариантов и попробуй снова',
					  'mix_question': 'Перемешать текст?',
					  'yes': 'Да',
					  'no': 'Нет',
					  'send_scenario': 'Скиньте сам текст',
					  'text_without_words': 'Вы скинули текст без слов',
					  'start_again': 'Начинаем звново'}

			user = User(slovar)
			bot.send_message(chat_id, user.slovar['choose_language'])
		elif message.text == 'English':
			slovar = {'choose_language': 'Good',
					  'error': 'An error has occurred. Try again',
					  'choose_level': 'Choose the level of word difficulty',
					  'wrong_word': 'Choose one of the options and try again',
					  'mix_question': 'Shuffle text?',
					  'yes': 'Yes',
					  'no': 'No',
					  'send_scenario': 'Send the text',
					  'text_without_words': 'You send the text without words',
					  'start_again': 'Starting again'
					  }
			user = User(slovar)
			bot.send_message(chat_id, user.slovar['choose_language'])
		else:
			raise WrongWord
	except WrongWord:
		bot.send_message(chat_id, 'Submit one of two options. Try again')
		bot.register_next_step_handler(message, choose_language)
		return
	except Exception:
		bot.send_message(chat_id, 'An error has occurred. Try again')
		bot.register_next_step_handler(message, choose_language)
		return
	else:
		markup = types.ReplyKeyboardMarkup(selective=True)
		btn1 = types.KeyboardButton('A1')
		btn2 = types.KeyboardButton('A2')
		btn3 = types.KeyboardButton('B1')
		btn4 = types.KeyboardButton('B2')
		btn5 = types.KeyboardButton('C1')
		btn6 = types.KeyboardButton('C2')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
		bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=markup)
		bot.register_next_step_handler(message, choose_level)
		return


def choose_level(message):
	global user
	chat_id = message.chat.id
	try:
		if message.text not in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
			raise WrongWord
	except WrongWord:
		bot.send_message(chat_id, user.slovar['wrong_word'])
		bot.register_next_step_handler(message, choose_level)
		return
	except Exception:
		bot.send_message(chat_id, user.slovar['error'])
		bot.register_next_step_handler(message, choose_level)
		return
	else:
		user.level = message.text
		markup = types.ReplyKeyboardMarkup(selective=True)
		btn1 = types.KeyboardButton(user.slovar['yes'])
		btn2 = types.KeyboardButton(user.slovar['no'])
		markup.add(btn1, btn2)
		bot.send_message(message.chat.id, user.slovar['mix_question'], reply_markup=markup)
		bot.register_next_step_handler(message, mix_question)
		return


def mix_question(message):
	global user
	chat_id = message.chat.id
	try:
		if message.text not in ['Да', 'Yes', 'No', 'Нет']:
			raise WrongWord
	except WrongWord:
		bot.send_message(chat_id, user.slovar['wrong_word'])
		bot.register_next_step_handler(message, mix_question)
		return
	except Exception:
		bot.send_message(chat_id, user.slovar['error'])
		bot.register_next_step_handler(message, mix_question)
		return
	else:
		if message.text in ['Yes', 'Да']:
			user.mix = True
		else:
			user.mix = False
		# bot.send_message(chat_id, f'level: {user.level}, mix: {user.mix}')
		markup = types.ReplyKeyboardRemove(selective=True)
		bot.send_message(message.chat.id, user.slovar['send_scenario'], reply_markup=markup)
		bot.register_next_step_handler(message, main_process)
		return


def main_process(message):
	global user
	chat_id = message.chat.id
	try:
		base_text = message.text.lower()
		final_text = ''
		for symbol in base_text:
			if symbol in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '.lower():
				final_text += symbol
		if final_text.strip() == '':
			raise TextWithoutWords
	except TextWithoutWords:
		bot.send_message(chat_id, user.slovar['text_without_words'])
		bot.register_next_step_handler(message, choose_level)
		markup = types.ReplyKeyboardMarkup(selective=True)
		btn1 = types.KeyboardButton('A1')
		btn2 = types.KeyboardButton('A2')
		btn3 = types.KeyboardButton('B1')
		btn4 = types.KeyboardButton('B2')
		btn5 = types.KeyboardButton('C1')
		btn6 = types.KeyboardButton('C2')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
		bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=markup)
		bot.send_message(message.chat.id, user.slovar['start_again'])
		bot.register_next_step_handler(message, choose_level)
		return
	except Exception:
		bot.send_message(chat_id, user.slovar['error'])
		bot.register_next_step_handler(message, main_process)
		return
	else:
		bot.send_message(message.chat.id, 'ok')
	return


# -
if message.text not in ['/chanlan']:
	raise WrongWord
elif message.text == '/chanlan':
	bot.register_next_step_handler(message, choose_language)
	return












# ----------------------------------------------------------------------------------
bot.infinity_polling()

