#!/usr/bin/python3
from telegram.ext import Updater, CommandHandler
import pickle

class item:    #creating the class
   def __init__(self):
    self.title=""
    self.pubdate=""
    self.link=""
    self.guid=""
    self.author=""
    self.creator=""
    self.content=""
    self.comment=""
    
    self.h_title=""
    self.h_pubdate=""
    self.h_link=""
    self.h_guid=""
    self.h_author=""
    self.h_creator=""
    self.h_content=""
    self.h_comment=""

f=open("arcdata", "rb")
l= pickle.load(f)
st=""
for i in range(len(l)):
        st+=l[i].title+"\n\n"+l[i].content


print(st)




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

	
def feeds(bot, update):
    f=open("arcdata", "rb")
    li_inst= pickle.load(f)
    l=li_inst
    s=""
    for i in range(len(l)):
        s+=l[i].title+"\n\n"

    bot.send_message(chat_id=update.message.chat_id, text=st)
    print(s)
    print(update.message.from_user.username+":"+update.message.text)

def disp(bot,update):
	bot.send_message(chat_id=update.message.chat_id, text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', parse_mode='XML')



    



updater = Updater(open("conf.ini",'r').read().strip())

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(CommandHandler('feeds', feeds))
updater.dispatcher.add_handler(CommandHandler('disp', disp))

updater.start_polling()
updater.idle()

