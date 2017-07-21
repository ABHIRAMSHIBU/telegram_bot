#!/usr/bin/python3
import os 
import subprocess
from telegram.ext import Updater, CommandHandler
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class announcement():
    def __init__(self,title='',desc='',img=''):
        self.title=title
        self.desc=desc
        self.img=img
        
    def display(self):
        return "Title: "+self.title+"\n"+"Desc: "+self.desc+"\n"+"img src: "+self.img+"\n"

import pickle
fin=open("announcement_data.bin","ab")
fout=open("announcement_data.bin","rb")
import os
l=[]
pickle.dump(l,fin)
def display():
        a=[]
        fout=open("announcement_data.bin","rb")
        l=pickle.load(fout)
        for i in range(len(l)):
            bot.send_message(chat_id=update.message.chat_id, text="\n"+str(i+1)+". "+l[i]+"\n")
def add(pos,an):
        #pos=input("\nEnter Position\n")
        #an=input("Enter the announcement\n")
        fout=open("announcement_data.bin","rb")
        l=pickle.load(fout)
        l.insert(int(pos)-1,an)
        fin=open("announcement_data.bin","wb")
        pickle.dump(l,fin)
def delete(pos):
        fout=open("announcement_data.bin","rb")
        #pos=input("Enter the no you want to delete\n")
        l=pickle.load(fout)
        del l[int(pos)-1]
        fin=open("announcement_data.bin","wb")
        pickle.dump(l,fin)
def strike(pos):
        fout=open("announcement_data.bin","rb")
        #pos=input("Enter the no you want to mark finished\n")
        l=pickle.load(fout)
        l[int(pos)-1]+=u'\u274c'
        fin=open("announcement_data.bin","wb")
        pickle.dump(l,fin)
def findspace(a):
        s=[]
        for i in range(len(a)):
            if a[i]	==' ':
                s.append(i)
        return s
import pickle
def start(bot, update):
        update.message.reply_text('Use /about to know more')
        print(update.message.from_user.username+":"+update.message.text)

def hello(bot, update):
        update.message.reply_text('Hello '+update.message.from_user.username)

def about(bot,update):
        bot.send_message(chat_id=update.message.chat_id, text="<b>This is the announcement bot of R2 TKMCE</b>",parse_mode="HTML")
        bot.send_message(chat_id=update.message.chat_id, text="Choose /announcements to see class details\nChoose /ktu to see university announcements")
                
def announcements(bot,update):
        bot.send_message(chat_id=update.message.chat_id, text="Announcements is as follows\n")
        f=open("announcement_data.bin","rb")
        a=pickle.load(f)
        try:
            for i in range(len(a)):
                bot.send_message(chat_id=update.message.chat_id, text=str(i+1)+"."+" "+a[i].title+"\n\n"+a[i].desc)
                if(len(a[i].img) !=0):
                    bot.send_photo(chat_id=update.message.chat_id, photo=open(l[i].img, 'rb'))
        except:
                pass
def ktu(bot,update):
        os.system("rm /tmp/ktudata_title.bin /tmp/ktudata_desc.bin /tmp/ktudata_time.bin")
        bot.send_message(chat_id=update.message.chat_id, text="Acquiring Data from ktu.edu.in\nStand by .........")      
        if(os.path.exists("get_ktudata.py")):
              os.system("python get_ktudata.py")
              text="KTU Announcements is as follows\n"
              flag=1
        else:
              text="Error! Contact bot admin"
              print(bcolors.FAIL+"Fetch program deploy error"+bcolors.ENDC)
              flag=0
        if(flag):
               try:
                    link=''
                    f1=open("/tmp/ktudata_title.bin","rb")
                    f2=open("/tmp/ktudata_desc.bin","rb")
                    f3=open("/tmp/ktudata_time.bin","rb")
                    l_title=pickle.load(f1)
                    l_desc=pickle.load(f2)
                    l_time=pickle.load(f3)
                    bot.send_message(chat_id=update.message.chat_id, text=text)
                    for i in range(len(l_title)):
                        bot.send_message(chat_id=update.message.chat_id, text=str(i+1)+"."+" "+"<b>"+l_title[i]+"</b>"+"\n"+"<b>"+str(l_time[i])+"</b>"+"\n\n"+l_desc[i]+"\n\n",parse_mode="HTML")
               except:
                     text="Read error"
                     print(bcolors.FAIL+"Failed to unpickle"+bcolors.ENDC)
                     bot.send_message(chat_id=update.message.chat_id, text=text)
        else:
               bot.send_message(chat_id=update.message.chat_id, text=text)
def mirror(bot,update):
	a=update.message.text
	l=findspace(a)
	passkey=open("passkey.txt").read()
	if a[l[0]+1:l[1]]==passkey:
		bot.send_message(chat_id=update.message.chat_id, text="Your wish is my command master\n")
		exec(a[l[1]+1:])
		print("done")
	else:
		bot.send_message(chat_id=update.message.chat_id, text="Authentication failure\n")
def add(bot,update):
	#import telegram_update as u
	#a=update.message.text
	#passkey=open("passkey.txt").read()
	#l=u.findspace(a)
	#bot.send_message(chat_id=update.message.chat_id, text="you typed\n"+a)
	#bot.send_message(chat_id=update.message.chat_id, text="passkey is\n"+passkey)
	#print(a[l[0]+1:l[1]])
	bot.send_photo(chat_id=update.message.chat_id, photo=open('/home/abhijith/Desktop/tkm.jpg', 'rb'))
#    update.message.reply_text()
updater = Updater(open("conf.ini",'r').read().strip())
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('mirror', mirror))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('announcements', announcements))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(CommandHandler('ktu', ktu))
updater.dispatcher.add_handler(CommandHandler('add', add))
updater.start_polling()
#		a=up.display()
#		bot.send_message(chat_id=update.message.chat_id, text="current data\n")
#		for i in range(len(a)):
#			bot.send_message(chat_id=update.message.chat_id, text=a[i])

