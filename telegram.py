import csv

import telebot

# Набор констант по датасету "World University Rankings"
DATASET_FILE = "cwurData.csv"
DATASET_WORLD_RANK_FIELD = 'world_rank'
DATASET_INSTITUTUION_FIELD = 'institution'
DATASET_COUNTRY_FIELD = 'country'
DATASET_NATIONAL_RANK_FIELD = 'national_rank'
DATASET_QUALITY_OF_EDUCATION_FIELD = 'quality_of_education'
DATASET_ALUMINI_EMPLOYMENT_FIELD = 'alumni_employment'
DATASET_QUALITI_OF_FACUALUTY_FIELD = 'quality_of_faculty'
DATASET_PUBLICATIONS_FIELD = 'publications'
DATASET_INFLUENCE_FIELD = 'influence'
DATASET_CITATIONS_FIELD = 'citations'
DATASET_BROAD_IMPACT_FIELD = 'broad_impact'
DATASET_PATENTS_FIELD = 'patents'
DATASET_SCORE_FIELD = 'score'
DATASET_YEAR_FIELD = 'year'

# Инициируем бот. Необходимо указать токен телеграм бота
TELEGRAM_BOT_TOKEN = ''
telebot_ = telebot.TeleBot(TELEGRAM_BOT_TOKEN)  # Создаем объект телеграм бота


def parse_text_message(message):
	""" Обрабатывает (парсит) пользовательское сообщение из бота. Вызывает поиск по "Рейтингу университета" и по строке из сообщения

	Аргументы:
	message - строка или цифра по которой будет производится поиск

	Возвращает строку - сообщение для ответа

	"""
	telebot_.send_message(message.chat.id, '⚙️ I\'ll try to find a university by rating')
	try:
		rankNumFromMessage = int(message.text)
		universityInfo = loadUniversityFromDatasetByWorldRank(rankNumFromMessage)
		return convertUniversityInfoToMessageView(universityInfo)
	except ValueError:
		# Мы не можем быть уверены пользователь ввел цифру или строку, данный способ проверки один из самых надежных
		pass 
	telebot_.send_message(message.chat.id, '⚙️ And by the phrase')
	universitiesInfo = loadUniversitiesFromDatasetByPhrase(message.text)
	if universitiesInfo:
		if len(universitiesInfo) == 1:
			return convertUniversityInfoToMessageView(universitiesInfo[0])
		universitiesMainInfo = '\n'.join([str(x.get(DATASET_WORLD_RANK_FIELD) + '. ' + x.get(DATASET_INSTITUTUION_FIELD)) for x in universitiesInfo])
		return f'⚙️ I found some univers:\n{universitiesMainInfo} \n\n😷 You can enter the number of the world ranking or specify the request'
	return ''


def searchRowsFromDatasetByField(field, value):
	""" Производит поиск всех записей в датасете по указанному значению
	
	Аргументы:
	field -- Поле колонки датасета
	value -- Значение колонки

	Возвращает массив словарей из всех совпадений

	"""
	foundRows = []
	with open(DATASET_FILE, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if not row.get(field):
				continue

			lowerUserValue = str(value).lower()
			lowerRowValue = row.get(field).lower()

			if lowerRowValue.startswith(lowerUserValue) or lowerUserValue in lowerRowValue:
				foundRows.append(row)
	return foundRows


def searchRowFromDatasetByField(field, value):
	""" Производит поиск определенной записи в датасете по указанному значению
	
	Аргументы:
	field -- Поле колонки датасета
	value -- Значение колонки

	Возвращает словарь - запись из датасета

	"""
	with open(DATASET_FILE, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if row.get(field) == str(value):
				return row
	return {}


def convertUniversityInfoToMessageView(universityData):
	""" Конвертирует информацию об университете в текстовое сообщение для телеграм бота 
	
	Аргументы:
	universityData -- Словарь, содержащий информацию об университете

	Возвращает строку - сообщение для пользователя

	"""
	if not isinstance(universityData, dict):
		return ''

	message = f'That\'s all I know:'
	for key, value in universityData.items():
		if not value:
			continue
		normalizedDataField = key.capitalize()
		normalizedDataField = normalizedDataField.replace('_', ' ')
		message += f'\n - {normalizedDataField} : {value}'
	return message


def loadUniversityFromDatasetByWorldRank(worldRank):
	""" Загружает из датасета университет по мировому рейтингу - проводит поиск по названию университета

	Аргументы:
	worldRank -- цифра от 0 до 1000 - номер в рейтинге
	
	Возвращает словарь - найденный в датасете университет или пустой словарь, если университет не найден
	
	"""

	if not isinstance(worldRank, int) or worldRank < 1 or worldRank > 1000:
		return {}
	return searchRowFromDatasetByField(field=DATASET_WORLD_RANK_FIELD, value=worldRank)


def loadUniversitiesFromDatasetByPhrase(phrase):
	""" Загружает из датасета университет по ключевой фразе - проводит поиск по названию университета

	Аргументы:
	phrase -- строка по которой необходимо найти университет из рейтинга
	
	Возвращает массив словарей - найденные в датасете университеты
	
	"""
	if not isinstance(phrase, str):
		return []
	return searchRowsFromDatasetByField(field=DATASET_INSTITUTUION_FIELD, value=phrase)


@telebot_.message_handler(commands=['start'])
def sendWelcomeMessage(message):
	""" Приветствует пользователя при первом использовании бота. Фреймворк вызывает данную функцию, когда пользователь вводит '/start'
	
	Аргументы:
	message -- объект сообщения, декоратор фрейморка отправляет сообщение в данную функцию. Подробнее см. в документации
	
	"""
	telebot_.reply_to(message, "Salute! 👋🏼\nI can help you find information about the university from the top 1000 in the world")


@telebot_.message_handler(commands=['help'])
def sendHelpMessage(message):
	""" Дает справку по доступным командам бота. Фреймворк вызывает данную функцию, когда пользователь вводит '/help'
	
	Аргументы:
	message -- объект сообщения, декоратор фрейморка отправляет сообщение в данную функцию. Подробнее см. в документации
	
	"""
	telebot_.send_message(message.chat.id, f'Доступные команды:\n\n/help - справка по коммандам\n/start -  Запуск бота')


@telebot_.message_handler(func=lambda message: True)
def echoAll(message):
	""" Прослушивает все тектовые сообщения пользователя, кроме комант /start и /help
	
	Аргументы:
	message -- объект сообщения, декоратор фреймворка отправляет сообщение в данную функцию. Подробнее см. в документации
	
	"""
	if message.text:
		responseMessage = parse_text_message(message)

	if not responseMessage:
		responseMessage = f'Sorry, didn\'t get it 😥'

	telebot_.reply_to(message, responseMessage)


def startApp():
	""" Инициирует работу приложения. Запускает петлю для прослушивания сообщений """
	telebot_.infinity_polling()


if __name__ == '__main__':
	startApp()