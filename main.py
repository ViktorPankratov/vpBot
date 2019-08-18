import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from weather import Weather
from translator import Translator

TOKEN = '676056615:AAFSxnrwZ1-2ZLgTj1Y2s0K4quMZabhxAnk'
WEATHER_APP_KEY = 'c1b4f3df7e0e3fd445d4f8ed0b590d5e'
YANDEX_API_KEY = 'trnsl.1.1.20190818T184330Z.5bf78df0e0844603.2bc3a37ba31aac853258c90fa800377242449bd6'

bot = telebot.TeleBot(TOKEN)

translator_text = 'translate'
weather_text = 'weather'
button_translator = KeyboardButton('/' + translator_text)
button_weather = KeyboardButton('/' + weather_text)

option_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
option_keyboard.add(button_translator, button_weather)

option_message = {button_weather.text: 'Введи название города',
                  button_translator.text: 'Напиши слово или фразу для перевода'}
current_option = ''


@bot.message_handler(commands=['start'])
def process_start_command(message: Message):
    bot.send_message(message.chat.id, 'Привет! 👋', reply_markup=option_keyboard)


@bot.message_handler(commands=[weather_text, translator_text])
def set_current_option(message: Message):
    global current_option
    current_option = message.text
    bot.send_message(message.chat.id, option_message[current_option])


@bot.message_handler(func=lambda message: True)
def runner(message: Message):
    if current_option == button_weather.text:
        send_weather(message)
    elif current_option == button_translator.text:
        translate(message)


def send_weather(message):
    weather = Weather(WEATHER_APP_KEY, message.text, 'ru')
    if not weather.get_weather():
        bot.send_message(message.chat.id, 'Упс, что-то пошло не так!')
    else:
        current, forecast = weather.get_weather()
        result = get_weather_message(current) + get_weather_message(forecast)
        bot.send_message(message.chat.id, result, parse_mode='Markdown')


def get_weather_message(weather):
    celcius_icon = '\u2103'
    weather_message = '*{}*: {}{}, {}{}\n'.format(weather['label'], int(weather['temperature']), celcius_icon,
                                                  weather['weather'], weather['icon'])
    return weather_message


def translate(message):
    t = Translator(message.text, YANDEX_API_KEY)
    if t.get_language() == 'en':
        result = t.get_translation('ru')
    else:
        result = t.get_translation('en')
    bot.send_message(message.chat.id, result)


bot.polling()
