import googletrans
import telebot
from telebot import types
from random import shuffle
import datetime as dt
import config

bot = telebot.TeleBot("5693296256:AAFQsYHKkbIKMhpKF8mYbTvL09hjpyt0Uyc")
translator = googletrans.Translator()

class WrongWord(Exception):
	pass


class TextWithoutWords(Exception):
	pass


class NoWordsInText(Exception):
	pass


class User:
	def __init__(self, level='A1', mix=True, chanlan=True):
		self.slovar = {'choose_language': 'Select interface language\nВыберите язык интерфейса',
					   'error': 'An error has occurred. Try again\nПроизошла ошибка. Попробуйте ещё раз',
					   'wrong_word': 'Select one of the options and try again\nВыберите один из вариантов и попробуйте снова',
					   'change_language': 'If you want to change the interface language, send /chanlan\nЕсли хотите изменить язык интерфейса, отправьте /chanlan'}
		self.level = level
		self.mix = mix
		self.chanlan = chanlan
		markup = types.ReplyKeyboardMarkup(selective=True)
		btn1 = types.KeyboardButton('A1')
		btn2 = types.KeyboardButton('A2')
		btn3 = types.KeyboardButton('B1')
		btn4 = types.KeyboardButton('B2')
		btn5 = types.KeyboardButton('C1')
		btn6 = types.KeyboardButton('C2')
		markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
		self.markup_level = markup
		markup = types.ReplyKeyboardMarkup(selective=True)
		btn1 = types.KeyboardButton('Русский')
		btn2 = types.KeyboardButton('English')
		markup.add(btn1, btn2)
		self.markup_language = markup


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
	user = User()
	f = open('users.txt', mode='r', encoding='utf8')
	text = f.read().split('\n').copy()
	file = open('users.txt', mode='w', encoding='utf8')
	f.close()
	user_id = message.from_user.id
	user_name = message.from_user.first_name
	if text == ['']:
		text = [f'{user_name}:{user_id}', '1']
	elif f'{user_name}:{user_id}' not in text[-2]:
		text[-2] += f', {user_name}:{user_id}'
		text[-1] = str(int(text[-1]) + 1)
	file.write('\n'.join(text))
	file.close()
	bot.send_message(message.chat.id, user.slovar['choose_language'], reply_markup=user.markup_language)
	bot.register_next_step_handler(message, choose_language, user)
	return


@bot.message_handler(func=lambda message: True)
def send_all(message):
	if message != '/start':
		bot.send_message(message.chat.id, 'Send /start\nНапишите /start')


def choose_language(message, user):
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
					  'choose_language': 'Выберите язык интерфейса',
					  'text_has_no_words': 'После чистки слов не осталось',
					  'help': 'Этот бот пригодится когда вам нужно заранее перевести сложные слова из текста на английском. Он удалит из текста все простые слова и отправит только сложные'
							  'и переведёт их если вам нужно.'
							  'Этим можно воспользоваться например перед просмотром фильма(В интернете можно найти сценарии к каждому фильму где есть все диалоги фильма). '
							  'Вам не придётся останавливать фильм на каждом новом слове, а спокойно смотреть так как вы уже будете знать перевод всех сложных слов. '
							  'Вы можете выбрать уровень сложности слов которые вам нужно удалить(A1 или  B2 и другие), '
							  'а также можно приказать боту перемешать текст или нет.\nЕсли хотите изменить язык интерфейса, отправьте /chanlan\n'
							  'Если у вас есть идеи по улучшению бота, нашли баг или хотите предложить аватарку для бота пишите ему : @Musa_Dulmiev',
					  'change_language': 'If you want to change the interface language, send /chanlan\nЕсли хотите изменить язык интерфейса, отправьте /chanlan',
					  'choose_language_to_translate': 'Выбери язык на который будут переводиться слова'}

			user.slovar = slovar
			user.ui_language = 'ru'
			user.slovar_of_short_languages = config.dict_of_short_languages_ru
			bot.send_message(chat_id, user.slovar['ok'])
			if user.chanlan:
				bot.send_message(message.chat.id, user.slovar['change_language'])
				user.chanlan = False
		elif message.text == 'English':
			slovar = {'ok': 'Well',
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
					  'choose_language': 'Select interface language',
					  'text_has_no_words': 'No words left after cleaning',
					  'help': "This bot is useful when you need to translate difficult words from an English text in advance."
							  " It will remove all simple words from the text and send only complex ones."
							  " This can be used, for example, before watching a movie (on the Internet you can find scripts for each movie where there are all the dialogues of the movie). "
							  "You don't have to stop the movie at every new word, but watch calmly as you will already know the translation of all difficult words. "
							  "You can choose the level of difficulty of the words you need to remove (A1 or B2 and others), and you can also order the bot to shuffle the text or not.\n"
							  "If you want to change the interface language, send /chanlan\n"
							  "If you have ideas for improving the bot, found a bug or want to suggest an avatar for the bot, write to him: @Musa_Dulmiev",
					  'change_language': 'If you want to change the interface language, send /chanlan\nЕсли хотите изменить язык интерфейса, отправьте /chanlan',
					  'choose_language_to_translate': 'Choose the language into which the words will be translated'}
			user.slovar = slovar
			user.ui_language = 'en'
			user.slovar_of_short_languages = config.dict_of_short_languages_eng
			bot.send_message(chat_id, user.slovar['ok'])
			if user.chanlan:
				bot.send_message(message.chat.id, user.slovar['change_language'])
				user.chanlan = False
		elif message.text == '/start':
			bot.register_next_step_handler(message, choose_language, user)
			return
		else:
			raise WrongWord
	except WrongWord:
		bot.send_message(chat_id, user.slovar['wrong_word'])
		bot.register_next_step_handler(message, choose_language, user)
		return
	except Exception:
		bot.send_message(chat_id, user.slovar['error'])
		bot.register_next_step_handler(message, choose_language, user)
		return
	else:
		markup = types.ReplyKeyboardMarkup(selective=True)
		langs = sorted(translator.translate(', '.join(googletrans.LANGUAGES.values()),
											src='en', dest=user.ui_language).text.split(', '))
		if user.ui_language == 'ru':
			langs[-1] = 'японский'
		user.sp_of_langs = langs
		for name in langs:
			btn = types.KeyboardButton(name.capitalize())
			markup.add(btn)
		bot.send_message(message.chat.id, user.slovar['choose_language_to_translate'], reply_markup=markup)
		bot.register_next_step_handler(message, choose_language_to_translate, user)
		return


def choose_language_to_translate(message, user):
	chat_id = message.chat.id
	try:
		if message.text.lower() not in user.sp_of_langs and message.text not in ['/chanlan',
																							 '/help',
																							 '/get_users',
																							 '/get_every_day',
																							 '/get_today',
																							 '/get_yesterday',
																							 '/start']:
			raise WrongWord
		elif message.text == '/chanlan':
			bot.send_message(message.chat.id, 'Select interface language\nВыберите язык интерфейса', reply_markup=user.markup_language)
			bot.register_next_step_handler(message, choose_language, user)
			return
		elif message.text == '/help':
			bot.send_message(message.chat.id, user.slovar['help'])
			bot.send_message(message.chat.id, user.slovar['start_again'])
			bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=user.markup_level)
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/get_users':
			users(chat_id)
			bot.send_message(message.chat.id, user.slovar['choose_level'])
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/get_every_day':
			get_statistics_for_every_day(chat_id)
			bot.send_message(message.chat.id, user.slovar['choose_level'])
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/get_today':
			get_today_statistics(chat_id)
			bot.send_message(message.chat.id, user.slovar['choose_level'])
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/get_yesterday':
			get_yesterday_statistics(chat_id)
			bot.send_message(message.chat.id, user.slovar['choose_level'])
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/start':
			bot.send_message(message.chat.id, user.slovar['choose_language'], reply_markup=user.markup_language)
			bot.register_next_step_handler(message, choose_language, user)
			return
	except WrongWord:
		bot.send_message(chat_id, user.slovar['wrong_word'])
		bot.register_next_step_handler(message, choose_language_to_translate, user)
		return
	except Exception:
		bot.send_message(chat_id, user.slovar['error'])
		bot.register_next_step_handler(message, choose_language_to_translate, user)
		return
	else:
		user.language_to_translate = user.slovar_of_short_languages[message.text.lower()]
		bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=user.markup_level)
		bot.register_next_step_handler(message, choose_level, user)
		return


def choose_level(message, user):
	print(user.language_to_translate)
	chat_id = message.chat.id
	try:
		if message.text not in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'] and message.text not in ['/chanlan',
																							 '/help',
																							 '/get_users',
																							 '/get_every_day',
																							 '/get_today',
																							 '/get_yesterday',
																							 '/start']:
			raise WrongWord
		elif message.text == '/chanlan':
			bot.send_message(message.chat.id, 'Select interface language\nВыберите язык интерфейса', reply_markup=user.markup_language)
			bot.register_next_step_handler(message, choose_language, user)
			return
		elif message.text == '/help':
			bot.send_message(message.chat.id, user.slovar['help'])
			bot.send_message(message.chat.id, user.slovar['start_again'])
			bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=user.markup_level)
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/get_users':
			users(chat_id)
			bot.send_message(message.chat.id, user.slovar['choose_level'])
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/get_every_day':
			get_statistics_for_every_day(chat_id)
			bot.send_message(message.chat.id, user.slovar['choose_level'])
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/get_today':
			get_today_statistics(chat_id)
			bot.send_message(message.chat.id, user.slovar['choose_level'])
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/get_yesterday':
			get_yesterday_statistics(chat_id)
			bot.send_message(message.chat.id, user.slovar['choose_level'])
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/start':
			bot.send_message(message.chat.id, user.slovar['choose_language'], reply_markup=user.markup_language)
			bot.register_next_step_handler(message, choose_language, user)
			return
		user.level = message.text
	except WrongWord:
		bot.send_message(chat_id, user.slovar['wrong_word'])
		bot.register_next_step_handler(message, choose_level, user)
		return
	except Exception:
		bot.send_message(chat_id, user.slovar['error'])
		bot.register_next_step_handler(message, choose_level, user)
		return
	else:
		user.level = message.text
		markup = types.ReplyKeyboardMarkup(selective=True)
		btn1 = types.KeyboardButton(user.slovar['yes'])
		btn2 = types.KeyboardButton(user.slovar['no'])
		markup.add(btn1, btn2)
		bot.send_message(message.chat.id, user.slovar['mix_question'], reply_markup=markup)
		bot.register_next_step_handler(message, mix_question, user)
		return


def mix_question(message, user):
	chat_id = message.chat.id
	try:
		if message.text not in ['Да', 'Yes', 'No', 'Нет'] and message.text not in ['/chanlan', '/help', '/start']:
			raise WrongWord
		elif message.text == '/chanlan':
			bot.send_message(message.chat.id, 'Select interface language\nВыберите язык интерфейса', reply_markup=user.markup_language)
			bot.register_next_step_handler(message, choose_language, user)
			return
		elif message.text == '/help':
			bot.send_message(message.chat.id, user.slovar['help'])
			bot.send_message(message.chat.id, user.slovar['start_again'])
			bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=user.markup_level)
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/start':
			bot.send_message(message.chat.id, user.slovar['choose_language'], reply_markup=user.markup_language)
			bot.register_next_step_handler(message, choose_language, user)
			return
	except WrongWord:
		bot.send_message(chat_id, user.slovar['wrong_word'])
		bot.register_next_step_handler(message, mix_question, user)
		return
	except Exception:
		bot.send_message(chat_id, user.slovar['error'])
		bot.register_next_step_handler(message, mix_question, user)
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
		bot.register_next_step_handler(message, main_process, user, markup)
		return


def main_process(message, user, markup):
	new_date = False
	chat_id = message.chat.id
	try:
		file = open('statistics_for_every_day.txt', mode='r', encoding='utf8')
		date = file.read().split('\n')
		date = date[-3][:-1].split()
		yesterday = dt.date(int(date[0]), int(date[1]), int(date[2]))
		today = dt.datetime.now().date()
		file.close()
		if today > yesterday:
			new_date = True
		file.close()
		if new_date:
			file = open('statistics_for_every_day.txt', mode='a', encoding='utf8')
			file.write(f'\n{today.year} {today.month} {today.day}:\n')
			file.write(f'{message.from_user.id}\n')
			file.write('1')
			file.close()
		if not new_date:
			file = open('statistics_for_every_day.txt', mode='r', encoding='utf8')
			text = file.read().split('\n')
			if str(message.from_user.id) not in text[-2].split(', '):
				text[-2] += f', {message.from_user.id}'
				count = str(int(text[-1]) + 1)
				text[-1] = count
				file.close()
				file = open('statistics_for_every_day.txt', mode='w', encoding='utf8')
				file.write('\n'.join(text))
			file.close()
		if message.text == user.slovar['start_again_button']:
			bot.send_message(message.chat.id, user.slovar['start_again'])
			bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=user.markup_level)
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/chanlan':
			bot.send_message(message.chat.id, 'Select interface language\nВыберите язык интерфейса', reply_markup=user.markup_language)
			bot.register_next_step_handler(message, choose_language, user)
			return
		elif message.text == '/help':
			bot.send_message(message.chat.id, user.slovar['help'])
			bot.send_message(message.chat.id, user.slovar['start_again'])
			bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=user.markup_level)
			bot.register_next_step_handler(message, choose_level, user)
			return
		elif message.text == '/start':
			bot.send_message(message.chat.id, user.slovar['choose_language'], reply_markup=user.markup_language)
			bot.register_next_step_handler(message, choose_language, user)
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
		if not final_text:
			raise NoWordsInText
		if user.mix:
			shuffle(final_text)
		final_text = ' '.join(final_text)
	except TextWithoutWords:
		bot.send_message(chat_id, user.slovar['text_without_words'])
		bot.send_message(message.chat.id, user.slovar['start_again'])
		bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=user.markup_level)
		bot.register_next_step_handler(message, choose_level, user)
		return
	except NoWordsInText:
		bot.send_message(chat_id, user.slovar['text_has_no_words'])
		bot.send_message(message.chat.id, user.slovar['start_again'])
		bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=user.markup_level)
		bot.register_next_step_handler(message, choose_level, user)
		return
	except Exception:
		bot.send_message(chat_id, user.slovar['error'])
		bot.register_next_step_handler(message, mix_question, user)
		return
	else:
		bot.send_message(message.chat.id, final_text)
		bot.send_message(message.chat.id, user.slovar['start_again'])
		bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=user.markup_level)
		bot.register_next_step_handler(message, choose_level, user)
	return


def start_again(message, user):
	if message.text == user.slovar['start_again_button']:
		bot.send_message(message.chat.id, user.slovar['start_again'])
		bot.send_message(message.chat.id, user.slovar['choose_level'], reply_markup=user.markup_level)
		bot.register_next_step_handler(message, choose_level, user)
	else:
		bot.register_next_step_handler(message, start_again, user)


def users(chat_id):
	file = open('users.txt', mode='r', encoding='utf8')
	text = file.read()
	file.close()
	bot.send_message(chat_id, text)
	return


def get_statistics_for_every_day(chat_id):
	file = open('statistics_for_every_day.txt', mode='r', encoding='utf8')
	text = file.read()
	file.close()
	bot.send_message(chat_id, text)
	return


def get_today_statistics(chat_id):
	file = open('statistics_for_every_day.txt', mode='r', encoding='utf8')
	text = file.read().split('\n')
	file.close()
	text = '\n'.join(text[-3:])
	bot.send_message(chat_id, text)
	return


def get_yesterday_statistics(chat_id):
	file = open('statistics_for_every_day.txt', mode='r', encoding='utf8')
	text = file.read().split('\n')
	file.close()
	text = '\n'.join(text[-6:-3])
	bot.send_message(chat_id, text)
	return

# ----------------------------------------------------------------------------------
bot.infinity_polling()