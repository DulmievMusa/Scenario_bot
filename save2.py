import telebot
from telebot import types
from random import shuffle

bot = telebot.TeleBot("5693296256:AAFQsYHKkbIKMhpKF8mYbTvL09hjpyt0Uyc")


class WrongWord(Exception):
	pass


class TextWithoutWords(Exception):
	pass


class User:
	def __init__(self, level='A1', mix=True):
		self.slovar = {'choose_language': 'Select interface language/Выберите язык интерфейса',
					   'error': 'An error has occurred. Try again/Произошла ошибка. Попробуйте ещё раз',
					   'wrong_word': 'Select one of the options and try again/Выберите один из вариантов и попробуйте снова'}
		self.level = level
		self.mix = mix


user = User()


words_of_language = {
	'A1': ['go', 'mum', 'home'],
	'A2': [],
	'B1': [],
	'B2': [],
	'C1': [],
	'C2': [],
}


@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(selective=True)
	btn1 = types.KeyboardButton('Русский')
	btn2 = types.KeyboardButton('English')
	markup.add(btn1, btn2)
	bot.send_message(message.chat.id, user.slovar['choose_language'], reply_markup=markup)
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
			slovar = {'ok': 'Хорошо',
					  'error': 'Произошла ошибка. Попробуйте ещё раз',
					  'choose_level': 'Выберите уровень сложности слов',
					  'wrong_word': 'Выберите один из вариантов и попробуйте снова',
					  'mix_question': 'Перемешать текст?',
					  'yes': 'Да',
					  'no': 'Нет',
					  'send_scenario': 'Скиньте сам текст',
					  'text_without_words': 'Вы скинули текст без слов на английском',
					  'start_again': 'Начинаем заново',
					  'start_again_button': 'Начать заново',
					  'choose_language': 'Выберите язык интерфейса'}

			user.slovar = slovar
			bot.send_message(chat_id, user.slovar['ok'])
		elif message.text == 'English':
			slovar = {'ok': 'Good',
					  'error': 'An error has occurred. Try again',
					  'choose_level': 'Select the level of word difficulty',
					  'wrong_word': 'Select one of the options and try again',
					  'mix_question': 'Shuffle text?',
					  'yes': 'Yes',
					  'no': 'No',
					  'send_scenario': 'Send the text',
					  'text_without_words': 'You send the text without English words',
					  'start_again': 'Starting again',
					  'start_again_button': 'Start again',
					  'choose_language': 'Select interface language'}
			user.slovar = slovar
			bot.send_message(chat_id, user.slovar['ok'])
		else:
			raise WrongWord
	except WrongWord:
		bot.send_message(chat_id, user.slovar['wrong_word'])
		bot.register_next_step_handler(message, choose_language)
		return
	except Exception:
		bot.send_message(chat_id, user.slovar['error'])
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
		if message.text not in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] and message.text not in ['/chanlan', '/help']:
			raise WrongWord
		elif message.text == '/chanlan':
			markup = types.ReplyKeyboardMarkup(selective=True)
			btn1 = types.KeyboardButton('Русский')
			btn2 = types.KeyboardButton('English')
			markup.add(btn1, btn2)
			bot.send_message(message.chat.id, 'Select interface language/Выберите язык интерфейса', reply_markup=markup)
			bot.register_next_step_handler(message, choose_language)
			return
		elif message.text == '/help':
			bot.send_message(message.chat.id, "It's command help")
			return
		user.level = message.text
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
		if message.text not in ['Да', 'Yes', 'No', 'Нет'] and message.text not in ['/chanlan']:
			raise WrongWord
		elif message.text == '/chanlan':
			markup = types.ReplyKeyboardMarkup(selective=True)
			btn1 = types.KeyboardButton('Русский')
			btn2 = types.KeyboardButton('English')
			markup.add(btn1, btn2)
			bot.send_message(message.chat.id, 'Select interface language/Выберите язык интерфейса', reply_markup=markup)
			bot.register_next_step_handler(message, choose_language)
			return
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
		markup = types.ReplyKeyboardMarkup(selective=True)
		btn = types.KeyboardButton(user.slovar['start_again_button'])
		markup.add(btn)
		bot.send_message(message.chat.id, user.slovar['send_scenario'], reply_markup=markup)
		bot.register_next_step_handler(message, main_process)
		return


def main_process(message):
	global user
	chat_id = message.chat.id
	try:
		if message.text == user.slovar['start_again_button']:
			markup = types.ReplyKeyboardMarkup(selective=True)
			btn1 = types.KeyboardButton('A1')
			btn2 = types.KeyboardButton('A2')
			btn3 = types.KeyboardButton('B1')
			btn4 = types.KeyboardButton('B2')
			btn5 = types.KeyboardButton('C1')
			btn6 = types.KeyboardButton('C2')
			markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
			bot.send_message(message.chat.id, user.slovar['start_again'])
			bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=markup)
			bot.register_next_step_handler(message, choose_level)
			return
		elif message.text == '/chanlan':
			markup = types.ReplyKeyboardMarkup(selective=True)
			btn1 = types.KeyboardButton('Русский')
			btn2 = types.KeyboardButton('English')
			markup.add(btn1, btn2)
			bot.send_message(message.chat.id, 'Select interface language/Выберите язык интерфейса', reply_markup=markup)
			bot.register_next_step_handler(message, choose_language)
			return
		base_text = message.text.lower()
		final_text = ''
		for symbol in base_text:
			if symbol in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '.lower():
				final_text += symbol
		if final_text.strip() == '':
			raise TextWithoutWords
		final_text = final_text.split()
		does_not_repeats = []
		for word in final_text:
			if word not in does_not_repeats:
				does_not_repeats.append(word)
		final_text = does_not_repeats.copy()
		count = 0
		for index in range(len(final_text)):
			index -= count
			if final_text[index] in words_of_language[user.level]:
				final_text.remove(final_text[index])
				count += 1
		if user.mix:
			shuffle(final_text)
		final_text = ' '.join(final_text)
	except TextWithoutWords:
		bot.send_message(chat_id, user.slovar['text_without_words'])
		markup = types.ReplyKeyboardMarkup(selective=True)
		btn1 = types.KeyboardButton('A1')
		btn2 = types.KeyboardButton('A2')
		btn3 = types.KeyboardButton('B1')
		btn4 = types.KeyboardButton('B2')
		btn5 = types.KeyboardButton('C1')
		btn6 = types.KeyboardButton('C2')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
		bot.send_message(message.chat.id, user.slovar['start_again'])
		bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=markup)
		bot.register_next_step_handler(message, choose_level)
		return
	except Exception:
		bot.send_message(chat_id, user.slovar['error'])
		bot.register_next_step_handler(message, main_process)
		return
	else:
		bot.send_message(message.chat.id, final_text)
		bot.register_next_step_handler(message, start_again)
	return


def start_again(message):
	if message.text == user.slovar['start_again_button']:
		markup = types.ReplyKeyboardMarkup(selective=True)
		btn1 = types.KeyboardButton('A1')
		btn2 = types.KeyboardButton('A2')
		btn3 = types.KeyboardButton('B1')
		btn4 = types.KeyboardButton('B2')
		btn5 = types.KeyboardButton('C1')
		btn6 = types.KeyboardButton('C2')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
		bot.send_message(message.chat.id, user.slovar['start_again'])
		bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=markup)
		bot.register_next_step_handler(message, choose_level)
	else:
		bot.register_next_step_handler(message, start_again)



# ----------------------------------------------------------------------------------
bot.infinity_polling()


