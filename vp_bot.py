import telebot
from telebot.types import Message
from telebot import apihelper

TOKEN = '676056615:AAFSxnrwZ1-2ZLgTj1Y2s0K4quMZabhxAnk'
# PROXY = 'socks5://telegram:telegram@qcpfo.tgproxy.me:1080'


# apihelper.proxy = {'https', PROXY}
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def upper(message: Message):
    bot.send_message(message.chat.id, message.text.upper())

bot.polling()
