import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from config import Config
from main_strings import MainStrings
from weather import Weather
from translator import Translator

config = Config()
TOKEN = config.telebot_token
WEATHER_APP_KEY = config.weather_app_key
YANDEX_API_KEY = config.yandex_api_key

bot = telebot.TeleBot(TOKEN)

text = MainStrings()
translator_text = text.translator
weather_text = text.weather
button_translator = KeyboardButton('/' + translator_text)
button_weather = KeyboardButton('/' + weather_text)

option_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
option_keyboard.add(button_translator, button_weather)

option_message = {button_weather.text: text.button_weather,
                  button_translator.text: text.button_translator}
current_option = ''


@bot.message_handler(commands=['start'])
def process_start_command(message: Message):
    bot.send_message(message.chat.id, text.button_translatorhe,
                     reply_markup=option_keyboard)


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
        bot.send_message(message.chat.id, text.oops)
    else:
        current, forecast = weather.get_weather()
        result = get_weather_message(current) + get_weather_message(forecast)
        bot.send_message(message.chat.id, result, parse_mode='Markdown')


def get_weather_message(weather):
    celcius_icon = '\u2103'
    weather_message = '*{label}*: {temp}{unit_symbol}, {desc}{icon}\n'.format(
        label=weather['label'],
        temp=int(weather['temperature']),
        unit_symbol=celcius_icon,
        desc=weather['weather'],
        icon=weather['icon'])
    return weather_message


def translate(message):
    t = Translator(message.text, YANDEX_API_KEY)
    if t.get_language() == 'en':
        result = t.get_translation('ru')
    else:
        result = t.get_translation('en')
    bot.send_message(message.chat.id, result)


bot.polling()
