#!/usr/bin/python3
from telegram.ext import Updater, CommandHandler,Job
import pickle
import re
import os
import telegram
import psutil
import subprocess as sp

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

def id(bot, update):
   text="Supergroup id: "+str(update.message.chat_id)
   update.message.reply_text(text)
   update.message.reply_text("User id: "+str(update.message.from_user.id))
def runs(bot, update):
   update.message.reply_text("Yup at 100%")

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
   data='''             <b>Destroyer Server bot!</b>
                <i>About/Help DestroyerServer_bot</i>
-------------------------------------------------------
<b>Commands</b>
1)<code> /start</code>
2)<code> /about</code>
3)<code> /add x1,x2,x3....</code>
4)<code> /mult x1,x2,x3....</code>
5)<code> /sysstat</code>
6)<code> /shell anyLinuxCommand </code> 
7)<code> /memstat </code>
8)<code> /cpustat </code>
9)<code> /cpuhog </code>
Get shell? ssh bot@abhiramshibu.tk -p8000 # password respectOthers 
Checkout: <a href='https://forums.arctotal.com/'>ARC Forums</a>
-------------------------------------------------------
'''
   bot.send_message(chat_id=update.message.chat_id, text=data,parse_mode="HTML")
   f.close()
   print(update.message.from_user.username+":"+update.message.text)
def start(bot, update):
    update.message.reply_text('Use /about to know more')
    print(update.message.from_user.username+":"+update.message.text)
def hello(bot, update):
    update.message.reply_text('Hello '+update.message.from_user.first_name)
def sysstat(bot, update):
    speedtestp=os.popen("speedtest")
    cpuUse=psutil.cpu_percent(percpu=True,interval=1)
    usedMem=psutil.virtual_memory().used/1024/1024/1024
    freeMem=psutil.virtual_memory().free/1024/1024/1024
    totalMem=psutil.virtual_memory().total/1024/1024/1024
    swapFree=psutil.swap_memory().free/1024/1024/1024
    swapUse=psutil.swap_memory().used/1024/1024/1024
    swapTotal=psutil.swap_memory().total/1024/1024/1024
    msg="-------CPU------\n"
    for i in range(len(cpuUse)):
        msg+="CPU"+str(i)+":"+str(float(cpuUse[i]))+"%\n"
    msg+="------MM------\n"
    msg+="used:"+str(usedMem)+"GiB\n"
    msg+="free:"+str(freeMem)+"GiB\n"
    msg+="total:"+str(totalMem)+"GiB\n"
    msg+="------SM------\n"
    msg+="used:"+str(swapUse)+"GiB\n"
    msg+="free:"+str(swapFree)+"GiB\n"
    msg+="total:"+str(swapTotal)+"GiB\n"
    update.message.reply_text(msg)
    update.message.reply_text("Getting speedtest results")
    speedtest=speedtestp.read()
    download=speedtest.find("Download:")
    downloadEnd=speedtest.find("/s",download)
    speedtestDownload=speedtest[download:downloadEnd]
    upload=speedtest.find("Upload:")
    uploadEnd=speedtest.find("/s",upload)
    speedtestUpload=speedtest[upload:uploadEnd]
    msg="-------SpeedTest-------\n"
    msg+=speedtestDownload+"\n"
    msg+=speedtestUpload+"\n"
    update.message.reply_text(msg)
def cpustat(bot,update):
    cpuUse=psutil.cpu_percent(percpu=True,interval=1)
    msg="-------CPU------\n"
    for i in range(len(cpuUse)):
        msg+="CPU"+str(i)+":"+str(float(cpuUse[i]))+"%\n"
    update.message.reply_text(msg)
def memstat(bot,update):
    usedMem=psutil.virtual_memory().used/1024/1024/1024
    freeMem=psutil.virtual_memory().free/1024/1024/1024
    totalMem=psutil.virtual_memory().total/1024/1024/1024
    swapFree=psutil.swap_memory().free/1024/1024/1024
    swapUse=psutil.swap_memory().used/1024/1024/1024
    swapTotal=psutil.swap_memory().total/1024/1024/1024
    msg="------MM------\n"
    msg+="used:"+str(usedMem)+"GiB\n"
    msg+="free:"+str(freeMem)+"GiB\n"
    msg+="total:"+str(totalMem)+"GiB\n"
    msg+="------SM------\n"
    msg+="used:"+str(swapUse)+"GiB\n"
    msg+="free:"+str(swapFree)+"GiB\n"
    msg+="total:"+str(swapTotal)+"GiB\n"
    update.message.reply_text(msg)
def st(bot,update):
    speedtestp=os.popen("speedtest")
    update.message.reply_text("Getting speedtest results")
    speedtest=speedtestp.read()
    download=speedtest.find("Download:")
    downloadEnd=speedtest.find("/s",download)
    speedtestDownload=speedtest[download:downloadEnd]
    upload=speedtest.find("Upload:")
    uploadEnd=speedtest.find("/s",upload)
    speedtestUpload=speedtest[upload:uploadEnd]
    msg="-------SpeedTest-------\n"
    msg+=speedtestDownload+"\n"
    msg+=speedtestUpload+"\n"
    update.message.reply_text(msg)
def cpuhog(bot,update):
    command='''ps -aeo pcpu,pid,user,args | sort -k1 -r -n | head -1 | awk '''
    command+="'"+'''{ print "CpuUse:"$1; print "PID:"$2; print "User:"$3; print "Command:"$4 }'''
    command+="'"
    p=os.popen(command)
    update.message.reply_text(p.read())
def shell(bot,update):
    cwd=os.getcwd()
    os.chdir("/home/temp")
    msg=update.message.text
    msg=msg.split()
    msg.pop(0)
    msg=" ".join(msg)
    msg=msg.strip()
    if("conf.ini" in msg):
        update.message.reply_text("Nice try :-)")
    else:
        if(os.path.exists("/tmp/bot")):
            f=open("/tmp/bot/runnable.sh","w")
        else:
            os.mkdir("/tmp/bot")
            f=open("/tmp/bot/runnable.sh","w")
        f.write("#!/usr/bin/env zsh\n")
        os.system("chmod +x /tmp/bot/runnable.sh")
        f.write(msg+"\n")
        f.close()
        msg="sudo -u bot /tmp/bot/runnable.sh"
        p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True);
        i=0
        while(p.poll()==None):
            time.sleep(1)
            i+=1
            if(i==5):
                break
        if(i==5):
            data="Timeout killed\n"
            p.kill()
            data+=p.stdout.read().decode("utf-8")
            stderrData=p.stderr.read().decode("utf-8");
            if(stderrData):
                data+="Errors where detected while executing!"+"\n"
                data+=stderrData
        else:
            data=p.stdout.read().decode("utf-8")
            stderrData=p.stderr.read().decode("utf-8");
            if(stderrData):
                data+="Errors where detected while executing!"+"\n"
                data+=stderrData
        #update.message.reply_text(msg)
        update.message.reply_text(data)
    os.chdir(cwd)
try: 
   key=open("conf.ini",'r').read().strip()
except: 
   print("Error occured, try running setup.py")
   exit()
   

updater = Updater(key)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('id', id))
updater.dispatcher.add_handler(CommandHandler('runs', runs))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('about', about))
updater.dispatcher.add_handler(CommandHandler('add', add))
updater.dispatcher.add_handler(CommandHandler('mult', mult))
updater.dispatcher.add_handler(CommandHandler('div', div))
updater.dispatcher.add_handler(CommandHandler('sysstat', sysstat))
updater.dispatcher.add_handler(CommandHandler('cpustat', cpustat))
updater.dispatcher.add_handler(CommandHandler('memstat', memstat))
updater.dispatcher.add_handler(CommandHandler('speedtest', st))
updater.dispatcher.add_handler(CommandHandler('cpuhog', cpuhog))
updater.dispatcher.add_handler(CommandHandler('shell', shell))
updater.start_polling()
#updater.idle()


