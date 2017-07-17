#!/usr/bin/python3
from telegram.ext import Updater, CommandHandler
def about(bot, update):
   f=open("about.txt",'r');
   bot.send_message(chat_id=update.message.chat_id, text=f.read())
   f.close()
   print(update.message.from_user.username+":"+update.message.text)

def start(bot, update):
    update.message.reply_text('Use /about to know more')
    print(update.message.from_user.username+":"+update.message.text)

def hello(bot, update):
    update.message.reply_text('Hello '+update.message.from_user.first_name)

updater = Updater(open("conf.ini",'r').read().strip())

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.start_polling()
updater.idle()

