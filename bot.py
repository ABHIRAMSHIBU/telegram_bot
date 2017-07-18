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
try:
 f=open("arcdata", "rb")
 l= pickle.load(f)
 st=""
 for i in range(len(l)):
    st+=l[i].title+"\n\n"+l[i].content
 print(st)
except:
	print("ARC data unavailable, falling back st=NULL");
	st="NULL"
f_title=open("title.bin", "rb")
f_link=open("link.bin", "rb")
f_desc=open("desc.bin", "rb")
title=[]
link=[]
desc=[]
title=pickle.load(f_title)
link=pickle.load(f_link)
desc=pickle.load(f_desc)
def runs(bot, update):
   update.message.reply_text("not so fast...")

def mult(bot, update):
   print(update.message.from_user.username+":"+update.message.text)
   message=update.message.text
   list=message.strip("/mult").strip().split(",")
   multi=1.0
   for i in list :
        multi*=float(i)
   update.message.reply_text("Answer is :"+str(multi))
def div(bot, update):
   print(update.message.from_user.username+":"+update.message.text)
   update.message.reply_text("Answer is, im not capable yet!")
def add(bot, update):
   print(update.message.from_user.username+":"+update.message.text)
   message=update.message.text
   list=message.strip("/add").strip().split(",")
   sum=0.0
   for i in list :
        sum+=float(i)
   update.message.reply_text("Sum is :"+str(sum))
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
    f_title=open("title.bin", "rb")
    f_link=open("link.bin", "rb")
    f_desc=open("desc.bin", "rb")
    try:
        title=[]
        link=[]
        desc=[]
        title=pickle.load(f_title)
        link=pickle.load(f_link)
        desc=pickle.load(f_desc)
    except:
        print("Error")
        title=['Fetch ERROR!']
        link=['Fetch ERROR!']
        desc=['Fetch ERROR!']
    for i in range(len(title)):
        text="<b>"+title[i]+"</b>"+"\n"+"link :"+link[i]+"\n"+desc[i].replace("<br>","\n").replace("<br />","\n").replace("I&#039;","I")[:50]+"..."
        print(text)
        bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode="HTML")
    print(update.message.from_user.username+":"+update.message.text)
def disp(bot,update):
	bot.send_message(chat_id=update.message.chat_id, text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', parse_mode='XML')
try: 
   key=open("conf.ini",'r').read().strip()
except: 
   print("Error occured, try running setup.py")
   exit()
updater = Updater(key)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('runs', runs))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(CommandHandler('add', add))
updater.dispatcher.add_handler(CommandHandler('mult', mult))
updater.dispatcher.add_handler(CommandHandler('div', div))
updater.dispatcher.add_handler(CommandHandler('feeds', feeds))
updater.dispatcher.add_handler(CommandHandler('disp', disp))
updater.start_polling()
#updater.idle()

