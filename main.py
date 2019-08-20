import telebot
from telebot.types import Message, ReplyKeyboardMarkup
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

option_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
option_keyboard.add(text.button_translator, text.button_weather)


@bot.message_handler(commands=['start'])
def process_start_command(message: Message):
    bot.send_message(message.chat.id, text.button_translatorhe,
                     reply_markup=option_keyboard)


@bot.message_handler(commands=['weather'])
def set_current_option(message: Message):
    bot.send_message(message.chat.id, text.button_weather)
    bot.register_next_step_handler(message, send_weather)


@bot.message_handler(commands=['translate'])
def set_current_option(message: Message):
    bot.send_message(message.chat.id, text.button_translator)
    bot.register_next_step_handler(message, translate)


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
    t = Translator(YANDEX_API_KEY)
    if t.get_language(message.text) == 'en':
        result = t.get_translation(message.text, 'ru')
    else:
        result = t.get_translation(message.text, 'en')
    bot.send_message(message.chat.id, result)


bot.polling()
