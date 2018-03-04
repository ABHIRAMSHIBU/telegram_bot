#!/usr/bin/python3
from telegram.ext import Updater, CommandHandler,Job
import pickle
import re
import os
import telegram
import feedparser


def strip_html(string):
    return re.sub('<[^<]+?>', '', string).replace("&","")
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
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


import time
import os
import pickle


def backup(bot, update):
    update.message.reply_text("Checking userinfo.")
    if(str(update.message.from_user.id) in open("admins.db","r").read()):
        bot.send_message(chat_id=update.message.chat_id, text="Access:<b> granted</b>",parse_mode="HTML")
        bot.send_message(chat_id=update.message.chat_id, text="Backing up data and db.",parse_mode="HTML")
        os.system("python ~/backup.py")
        try:
           if('success' in open("/root/status","r").read()):
               bot.send_message(chat_id=update.message.chat_id, text="Backup Status:<b> SUCCESS</b>",parse_mode="HTML")
           else:
               bot.send_message(chat_id=update.message.chat_id, text="Backing Status:<b> FAILED!</b>.",parse_mode="HTML")
        except:
             print("Error! - No such file or dir /root/status")
             bot.send_message(chat_id=update.message.chat_id, text="Backing Status:<b> Unknown, probably failed</b>.",parse_mode="HTML")
    else:
           bot.send_message(chat_id=update.message.chat_id, text="Access:<b> denied</b>",parse_mode="HTML")
    os.system("rm /root/status")
def changeindex(fname1,fname2):
    change_index=[]
    
    l1=pickle.load(fname1)
    l2=pickle.load(fname2)
    
    
    for i in range(len(l2)):
        if l2[i] not in l1:
            change_index.append(i)
    return change_index 


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
def id(bot, update):
   text="Supergroup id: "+str(update.message.chat_id)
   update.message.reply_text(text)
   update.message.reply_text("User id: "+str(update.message.from_user.id))
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
   bot.send_message(chat_id=update.message.chat_id, text=f.read(),parse_mode="HTML")
   f.close()
   print(update.message.from_user.username+":"+update.message.text)
def start(bot, update):
    update.message.reply_text('Use /about to know more')
    print(update.message.from_user.username+":"+update.message.text)
def hello(bot, update):
    update.message.reply_text('Hello '+update.message.from_user.first_name)
def feed(bot, update):
    try:
        data=feedparser.parse("https://forums.arctotal.com/forums/-/index.rss")
        for i in data["entries"]:
            resultString=""
            try:
                resultString+="Thread from :"+i["author"]+"\n"
                resultString+="Title :"+i["title"]+"\n"
                resultString+="Link :"+i["link"]+"\n"
            except:
                print("Autor ERROR!");
            try:
                resultString+="Content :"+cleanhtml(i["content"][0]["value"])[:30]+"........"+"\n"
            except:
                print("Content error");
            try:
                bot.send_message(chat_id=update.message.chat_id, text=resultString, parse_mode="HTML")
            except:
                print("Bot error!")
    except:
        update.message.reply_text("Internal ERROR occured!")
def feeds(bot, update):
    
    try:
       os.system("python3 arc_get.py title.bin link.bin desc.bin")
       f_title=open("title.bin", "rb")
       f_link=open("link.bin", "rb")
       f_desc=open("desc.bin", "rb")
    except:
       print("Fetcher deploy failure!")
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
        text="<b>"+title[i]+"</b>"+"<a href="+'"'+link[i]+'"'+"> Link</a>\n"+cleanhtml(desc[i].replace("<br>","\n").replace("<br />","\n").replace("I&#039;","I"))[:50]+"..."
        try:
        	bot.send_message(chat_id=update.message.chat_id, text=text, parse_mode="HTML")
        	print("\n\n\nSTART"+text+"END\n\n\n")
        except:
                print("Error occured while sending below")
                print(text+"\n\n\n")
    print(update.message.from_user.username+":"+update.message.text)
    os.system("rm -rf title.bin link.bin desc.bin")
def disp(bot,update):
	bot.send_message(chat_id=update.message.chat_id, text='<b>bold</b> <i>italic</i> <a href="http://google.com">link</a>.', parse_mode='XML')



try: 
   key=open("conf.ini",'r').read().strip()
except: 
   print("Error occured, try running setup.py")
   exit()
   

updater = Updater(key)
#bot = telegram.Bot(token=key)
#chat_id = bot.get_updates()[-1].message.chat_id

#def send_changedmessage(bot,update):
 #   global changed_text
  #  bot.send_message(chat_id=update.message.chat_id, text=changed_text, parse_mode="HTML")
    
    

counter=-1
def new(bot,job):
    global counter
    if counter==-1:
        print("FIRST ITERATION")
        ftitle1=open("title1.bin","rb")
        os.system("python3 arc_get.py title2.bin link2.bin desc2.bin")
        ftitle2=open("title2.bin","rb")
        lchange=changeindex(ftitle1,ftitle2)
        title2=pickle.load(open("title2.bin","rb"))
        link2=pickle.load(open("link2.bin","rb"))
        desc2=pickle.load(open("desc2.bin","rb"))
    
        for i in range(len(title2)):
            if i in lchange:
                text="<b>"+title2[i]+"</b>"+"<a href="+'"'+link2[i]+'"'+"> Link</a>\n"+cleanhtml(desc2[i].replace("<br>","\n").replace("<br />","\n").replace("I&#039;","I"))+"..."
                
                print(text)
                bot.send_message(chat_id=open("chat_id.txt").read(), text=text, parse_mode="HTML")
        	#print("\n\n\nSTART"+text+"END\n\n\n")
                
                
                

        
    else:
        print("second iteration")
        ftitle2=open("title2.bin","rb")
        os.system("python3 arc_get.py title1.bin link1.bin desc1.bin")
        ftitle1=open("title1.bin","rb")
        lchange=changeindex(ftitle2,ftitle1)
        title1=pickle.load(open("title1.bin","rb"))
        link1=pickle.load(open("link1.bin","rb"))
        desc1=pickle.load(open("desc1.bin","rb"))
        for i in range(len(title1)):
            if i in lchange:
                text="<b>"+title1[i]+"</b>"+"<a href="+'"'+link1[i]+'"'+"> Link</a>\n"+cleanhtml(desc1[i].replace("<br>","\n").replace("<br />","\n").replace("I&#039;","I"))+"..."
                bot.send_message(chat_id=open("chat_id.txt").read(), text=text, parse_mode="HTML")
                print(text)
                #print("\n\n\nSTART"+text+"END\n\n\n")
        
    
    counter*=-1
    
job_minute = Job(new, 3600.0)
j=updater.job_queue
j.put(job_minute, next_t=0.0)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('id', id))
updater.dispatcher.add_handler(CommandHandler('runs', runs))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(CommandHandler('add', add))
updater.dispatcher.add_handler(CommandHandler('mult', mult))
updater.dispatcher.add_handler(CommandHandler('div', div))
updater.dispatcher.add_handler(CommandHandler('feeds', feeds))
updater.dispatcher.add_handler(CommandHandler('feed', feed))
updater.dispatcher.add_handler(CommandHandler('disp', disp))
updater.dispatcher.add_handler(CommandHandler('backup', backup))
updater.start_polling()
#updater.idle()


