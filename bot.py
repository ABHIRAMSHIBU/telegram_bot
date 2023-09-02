#!/usr/bin/python3
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler,Job, Filters, MessageHandler, run_async, CallbackContext
import pickle
import re
import os
import psutil
import subprocess as sp
import base64
import time
import sys
from threading import Thread
from conf import *
from random import randint
#GLOBAL VARIABLES
betaMode=False
UNAUTH=[] # Unauthorized user
ATT=False
speedTestFlag=False
app = Application()

#END GLOBAL VARIABLES

#USER SHELL ASSOCIATION CLASS AND FUNCTIONS
class shellUser:
    def __init__(self,f):
        self.filePath=f
        self.db={}
        self.error=0
        if(os.path.exists(f)):
            try:
                f=open(f,"rb")
                self.db=pickle.load(f)
                f.close()
            except:
                self.error=1 #Problem with shell userbindings, loaded blank
                self.db={}
    def save(self,userid,unixname):
        self.db[userid]=unixname
        try:
            f=open(self.filePath,"wb")
            pickle.dump(self.db,f)
        except:
            self.error=2 #Problem with file write or serializing
    def load(self,userid):
        return self.db[userid]
    def rtError(self):
        if(self.error==0):
            return None
        elif(self.error==1):
            return "Problem with shell userbindings, loaded blank"
        elif(self.error==2):
            return "Problem with file write or serializing"
    #if(superuser==str(update.message.from_user.id)):
shelluser = shellUser("unixToTGID.dat")
def setuser(update: Update, context: CallbackContext):
    bot = context.bot
    if(superuser==str(update.message.from_user.id)):
        if(update.message.reply_to_message):
            id=update.message.reply_to_message.from_user.id
            unixName=update.message.text.replace("/setuser","").strip()
            if(unixName==""):
                update.message.reply_text(randomize(["UNIX name not given",
                                                     "/setuser <name> # <name> was not given"]))
            else:
                if(" " in unixName):
                    update.message.reply_text(randomize(["Unix name cannot contain space",
                                                         "Given name is not a valid identifier"]))
                else:
                    shelluser.save(id,unixName)
                    update.message.reply_text(randomize(["OK",
                                                         "Gotcha!",
                                                         "Aye Aye Captain"]))
        else:
            update.message.reply_text(randomize(["Dear SuperUser-\nYou may have not tagged a user.\nThank You\nYour friendy neighborhood PhenixBot",
                                                 "Please tag a message",
                                                 "Sorry but you clearly needs to tag something"]))
    else:
        update.message.reply_text(randomize(["Sometimes you may need some sort of \"god\" to get things done",
                                             "Permission denied, now show a cool UI",
                                             "Access DENIED!"]))
def getuser(update: Update, context: CallbackContext):
    bot = context.bot
    try:
        if(update.message.reply_to_message):
            msg="Username = "+str(shelluser.load(update.message.reply_to_message.from_user.id))
            update.message.reply_text(msg)
        else:
            update.message.reply_text("No tagged message to look for")
    except:
        update.message("No unix username for the tagged account!")
#END USER SHELL ASSOCIATION CLASS AND FUNCTIONS

#USER DB FUNCTIONS
def openDB():
    userDB=""
    if(os.path.exists(BASEPATH+"userdb.db")):
        f=open(BASEPATH+"userdb.db","rb")
        userDB=pickle.load(f)
    else:
        userDB={}
    return userDB
userDB=openDB()
def saveDB():
    f=open(BASEPATH+"userdb.db","wb")
    pickle.dump(userDB,f)
    f.close()
def addUserDB(message):
    save=False
    if(not (message.from_user.id in userDB.keys()) ):
        userDB[message.from_user.id]=[]
        save=True
    if(not (message.chat_id in userDB[message.from_user.id])):
        userDB[message.from_user.id].append(message.chat_id)
        save=True
    if(save):
        saveDB()
superuser=open("superuser","r").read().split("\n")[0].strip() #Get super user
#END USERDB FUNCTIONS

#HTML STRIPPERS IDK WHY THE HELL IT EXISTS IN MY CODE
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
#END HTML STRIPPER

# RANDOMIZERS
def randomize(l):
    n=len(l)
    i=randint(0,n-1)
    return l[i]
# END RANDOMIZER

# NOTES BACKEND
class Notes:
    def __init__(self,basepath):
        self.basepath=basepath
        if(not os.path.exists(basepath)):
            os.mkdir(basepath)
        pass
        self.error=False
    def remove(self,group,name):
        self.error=False
        reply=""
        path=self.basepath+"/"+str(group)
        if(os.path.exists(path+"/"+str(name))):
            os.system("rm "+path+"/"+str(name))
            reply="Remove success"
        else:
            reply="Northing to remove"
        return reply
    def add(self,group,name,data,user=""):
        self.error=False
        reply=""
        path=self.basepath+"/"+str(group)
        if( not os.path.exists(path)):
            os.mkdir(path)
        if(os.path.exists(path+"/"+str(name))):
            reply="Entry already exists, use /notes overwrite <name> <data>"
        else:
            f=open(path+"/"+str(name),"wb")
            f1=open("/tmp/test1","w")
            f1.write(data)
            f1.close()
            f.write(data.encode())
            f.write(b"\n")
            f.write(str(user).encode())
            f.close()
            reply="Success!"
        return reply
    def overwrite(self,group,name,data,user=""):
        self.error=False
        reply=""
        path=self.basepath+"/"+str(group)
        f=open(path+"/"+str(name),"wb")
        f.write(base64.encodebytes(data.encode()))
        f.write(str(user).encode())
        f.close()
        reply="Success!"
        return reply
    def read(self,group,name):
        self.error=False
        reply=""
        path=self.basepath+"/"+str(group)
        try:
            f=open(path+"/"+str(name),"rb")
        except FileNotFoundError:
            self.error=True
            return "Note don't exist"
        data=f.read()
        data=data.decode().split("\n")
        data="\n".join(data[:-1])
        reply=data
        return reply
    def listNotes(self,group):
        path=self.basepath+"/"+str(group)
        out="Notes don't exist for this group"
        self.error=True
        if(os.path.exists(path)):
            l=os.listdir(path)
            out1="\n".join(l)
            if(out1.strip("\n")!=""):
                out=out1
                self.error=False
        return out
notes=Notes("notes")
#END NOTES BACKEND

#NOTES FRONT END
def clear(update: Update, context: CallbackContext):
    bot = context.bot
    name=update.message.text.replace("/clear","").strip()
    groupid=str(update.message.chat_id)   
    reply=notes.remove(groupid,name)
    update.message.reply_text(reply)
def save(update: Update, context: CallbackContext):
    bot = context.bot
    if(update.message.reply_to_message):
        userid=update.message.from_user.id
        data=update.message.reply_to_message.text
        name=update.message.text.replace("/save","").strip()
        groupid=str(update.message.chat_id)
        reply=notes.add(groupid,name,data,userid)
        update.message.reply_text(reply)
    else:
        update.message.reply_text(randomize(["Please tag a message!",
                                             "Did you forget to tag?",
                                             "Knock Knock who is there?.. No one"]))
def noteshandle(update: Update, context: CallbackContext):
    bot = context.bot
    try:
        input=update.message.text
        input=input.replace("/notes","")
        input=input.strip()
        space1=input.find(" ")
        space2=input.find(" ",space1+1)
        cmd=""
        if(space1==-1):
            cmd=input
            if(cmd==""):
                cmd="list"
        else:
            cmd=input[:space1]
        if(cmd=="add" or cmd=="overwrite"):
            if(space2==-1):
                update.message.reply_text("Syntax incorrect, please retry with proper syntax!\n/notes add/overwrite name message")
                return
            name=input[space1+1:space2].strip()
            data=input[space2+1:]
            groupid=str(update.message.chat_id)
            userid=update.message.from_user.id
            reply=""
            if(cmd=="add"):
                reply=notes.add(groupid,name,data,userid)
            elif(cmd=="overwrite"):
                reply=notes.overwrite(groupid,name,data,userid)
            update.message.reply_text(reply)
        elif(cmd=="remove" or cmd=="read"):
            if(space1==-1):
                update.message.reply_text("Syntax incorrect, please retry with proper syntax!\n/notes remove/read name")
                return
            name=input[space1+1:]
            groupid=str(update.message.chat_id)
            if(cmd=="remove"):
                update.message.reply_text(notes.remove(groupid,name))
            else:
                chat=update.message.chat_id
                bot.send_message(chat,notes.read(groupid,name))
        elif(cmd=="list"):
            groupid=str(update.message.chat_id)
            data=notes.listNotes(groupid)
            update.message.reply_text(data)
        else:
            update.message.reply_text('''Sorry unknown command, supported commands
1) add
2) remove
3) overwrite
4) list
5) help''')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        update.message.reply_text(str(e)+" "+str(exc_tb.tb_lineno))
#END NOTES FRONT END

def quota(update: Update, context: CallbackContext):
    bot = context.bot
    msg=update.message.text.replace("/quota","").strip()
    data=""
    if(msg==""):
        id=update.message.from_user.id
        username=shelluser.load(id)
        if(username!=None):
            msg=username
        else:
            update.message.reply_text("User not found, Sorry!")
            return
    msg="quota -u "+msg
    p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
    i=0
    while(p.poll()==None):
        time.sleep(1)
        i+=1
        if(superuser==str(update.message.from_user.id)):
            if(i==60):
                break
        else:
            if(i==5):
                break
    if(i==5):
        data="Timeout killed\n"
        p.kill()
        data+=p.stdout.read().decode("utf-8")
        stderrData=p.stderr.read().decode("utf-8")
        if(stderrData):
            data+="Errors where detected while executing!"+"\n"
            data+=stderrData
    else:
        data=p.stdout.read().decode("utf-8")
        stderrData=p.stderr.read().decode("utf-8")
        if(stderrData):
            data+="Errors where detected while executing!"+"\n"
            data+=stderrData
    update.message.reply_text(data)
def deleteMsg(update: Update, context: CallbackContext):
    bot = context.bot
    text=""
    msg=update.message.text
    chat=update.message.chat_id
    if(superuser==str(update.message.from_user.id)):
        msgId=update.message.reply_to_message.message_id
        chtId=update.message.reply_to_message.chat_id
        bot.delete_message(chtId,msgId)
        update.message.delete()
        text="Message Deleted"
    else:
        text="Unauthorized"
    if("r" in msg):
        bot.send_message(chat,text)
def kick(update: Update, context: CallbackContext):
    bot = context.bot
    text=""
    chat=update.message.chat_id
    for i in bot.get_chat_administrators(chat):
        if(i.user.id ==update.message.from_user.id):
            bot.kick_chat_member(update.message.chat_id,update.message.reply_to_message.from_user.id)
            text="User kicked"
            break
        else:
            text="Unauthorized"
    update.message.reply_text(text)
def unkick(update: Update, context: CallbackContext):
    bot = context.bot
    text=""
    chat=update.message.chat_id
    for i in bot.get_chat_administrators(chat):
        if(i.user.id ==update.message.from_user.id):
            bot.unban_chat_member(update.message.chat_id,update.message.reply_to_message.from_user.id)
            text="User unkicked"
            break
        else:
            text="Unauthorized"
    update.message.reply_text(text)
def whoami(update: Update, context: CallbackContext):
    bot = context.bot
    text="You are "+str(update.message.from_user.full_name)+"\n"
    if(superuser==str(update.message.from_user.id)):
        text+="You are a superuser."+"\n"
    text+="Your user name "+str(update.message.from_user.username)+"\n"
    text+="Your telegram user id "+str(update.message.from_user.name)+"\n"
    text+="Your user id "+str(update.message.from_user.id)+"\n"
    if(update.message.from_user.id==update.message.chat_id):
        text+="This a personal message"
    else:
        text+="This is a group with group id "+str(update.message.chat_id)
    update.message.reply_text(text)
def whoareyou(update: Update, context: CallbackContext):
    bot = context.bot
    text=""
    if(update.message.reply_to_message is not None):
        text="You are "+str(update.message.reply_to_message.from_user.full_name)+"\n"
        if(superuser==str(update.message.reply_to_message.from_user.id)):
            text+="You are a superuser."+"\n"
        text+="Your user name "+str(update.message.reply_to_message.from_user.username)+"\n"
        text+="Your telegram user id "+str(update.message.reply_to_message.from_user.name)+"\n"
        text+="Your user id "+str(update.message.reply_to_message.from_user.id)+"\n"
        if(update.message.from_user.id==update.message.reply_to_message.chat_id):
            text+="This a personal message"
        else:
            text+="This is a group with group id "+str(update.message.reply_to_message.chat_id)
    else:
        text="Did you mean /whoami ? or please tag a message"
    update.message.reply_text(text)
def id(update: Update, context: CallbackContext):
   bot = context.bot
   if(superuser==str(update.message.from_user.id)):
        update.message.reply_text("You are superuser.")
   text="Supergroup id: "+str(update.message.chat_id)
   update.message.reply_text(text)
   update.message.reply_text("User id: "+str(update.message.from_user.id))
   f=open("/tmp/megDUMP","wb")
   pickle.dump(update.message,f)
def beta(update: Update, context: CallbackContext):
    bot = context.bot
    global betaMode
    if(superuser==str(update.message.from_user.id)):
        if(betaMode==True or os.path.exists(BASEPATH+"beta")):
            os.system("rm /opt/DestroyerBot/beta")
            update.message.reply_text("Disabling BETA")
            update.message.reply_text("See you again "+str(update.message.from_user.full_name)+", Bye..")
            betaMode=False
        else:
            os.system("touch /opt/DestroyerBot/beta")
            update.message.reply_text("Enabling BETA")
            update.message.reply_text("Welcome Back "+str(update.message.from_user.full_name)+", How may I help you.")
            betaMode=True
    else:
        update.message.reply_text("Sorry, You are Unauthorized to E/D BETA")
def runs(update: Update, context: CallbackContext):
   bot = context.bot
   update.message.reply_text("Yes bot is running with python "+sys.version.split(" ")[0]+"\nBot Version:"+str(VERSION))

def mult(update: Update, context: CallbackContext):
   bot = context.bot
   print(update.message.from_user.username+":"+update.message.text)
   message=update.message.text
   list=message.strip("/mult").strip().split(",")
   multi=1.0
   for i in list :
        multi*=float(i)
   update.message.reply_text("Answer is :"+str(multi))
def div(update: Update, context: CallbackContext):
   bot = context.bot
   print(update.message.from_user.username+":"+update.message.text)
   update.message.reply_text("Answer is, im not capable yet!")
def add(update: Update, context: CallbackContext):
   bot = context.bot
   print(update.message.from_user.username+":"+update.message.text)
   message=update.message.text
   list=message.strip("/add").strip().split(",")
   sum=0.0
   for i in list :
        sum+=float(i)
   update.message.reply_text("Sum is :"+str(sum))
def about(update: Update, context: CallbackContext):
   bot = context.bot 
   data='''             <b>Phenix Server bot!</b>
                <i>About/Help PhenixServer_bot</i>
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
10)<code> /whomai </code>
11)<code> /del or /delete </code>
12)<code> /whoareyou </code>
<b> BETA </b>
1) Beta what can you do?
Checkout: <a href='https://tuxforums.com/'>TUX Forums</a>
-------------------------------------------------------
'''
   bot.send_message(chat_id=update.message.chat_id, text=data,parse_mode="HTML")
   print(update.message.from_user.username+":"+update.message.text)
def start(update: Update, context: CallbackContext):
    bot = context.bot
    update.message.reply_text('Use /about to know more')
    print(update.message.from_user.username+":"+update.message.text)
def hello(update: Update, context: CallbackContext):
    bot = context.bot
    update.message.reply_text('Hello '+update.message.from_user.first_name)
def sysstat(update: Update, context: CallbackContext):
    bot = context.bot
    speedtestp=os.popen("python -m speedtest")
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
def cpustat(update: Update, context: CallbackContext):
    bot = context.bot
    cpuUse=psutil.cpu_percent(percpu=True,interval=1)
    msg="-------CPU------\n"
    for i in range(len(cpuUse)):
        msg+="CPU"+str(i)+":"+str(float(cpuUse[i]))+"%\n"
    update.message.reply_text(msg)
def memstat(update: Update, context: CallbackContext):
    bot = context.bot
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
@run_async
def st(update: Update, context: CallbackContext):
    bot = context.bot
    speedtestp=os.popen("python -m speedtest")
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
def cpuhog(update: Update, context: CallbackContext):
    bot = context.bot
    command='''ps -aeo pcpu,pid,user,args | sort -k1 -r -n | head -1 | awk '''
    command+="'"+'''{ print "CpuUse:"$1; print "PID:"$2; print "User:"$3; print "Command:"$4 }'''
    command+="'"
    p=os.popen(command)
    data=p.read()
    update.message.reply_text(data)
    return data
def fixPerm(update: Update, context: CallbackContext):
    bot = context.bot
    cwd=os.getcwd()
    os.chdir("/home/temp")
    msg="sudo chmod -R g+rwxs /mnt/build/sharedroms"
    if(os.path.exists("/tmp/bot")):
        f=open("/tmp/bot/runnable.sh","w")
    else:
        os.mkdir("/tmp/bot")
        f=open("/tmp/bot/runnable.sh","w")
    f.write("#!/usr/bin/env zsh\n")
    os.system("chmod +x /tmp/bot/runnable.sh")
    f.write(msg+"\n")
    f.close()
    msg="sudo -u abhiram /tmp/bot/runnable.sh"
    p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
    i=0
    while(p.poll()==None):
        time.sleep(1)
        i+=1
        if(i==120):
            break
    if(i==120):
        data="Timeout killed\n"
        p.kill()
        data+=p.stdout.read().decode("utf-8")
        stderrData=p.stderr.read().decode("utf-8")
        if(stderrData):
            data+="Errors where detected while executing!"+"\n"
            data+=stderrData
    else:
        data=p.stdout.read().decode("utf-8")
        stderrData=p.stderr.read().decode("utf-8")
        if(stderrData):
            data+="Errors where detected while executing!"+"\n"
            data+=stderrData
    #update.message.reply_text(msg)
    update.message.reply_text("Permission changed\nFollowing output obtained\n"+data)
    os.chdir(cwd)
@run_async
def shell(update: Update, context: CallbackContext):
    trust=False
    bot = context.bot
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
        f.write("cd ~\n")
        os.system("chmod +x /tmp/bot/runnable.sh")
        f.write(msg+"\n")
        f.close()
        if(update.message.from_user.id in shelluser.db.keys()):
            user=shelluser.load(update.message.from_user.id)
            msg="sudo -u "+user+" /tmp/bot/runnable.sh"
            trust=True
        else:
           text="User :"+str(update.message.from_user.name)+" ran : "+msg+" userid :"+str(update.message.from_user.id)
           bot.send_message(chat_id=int(superuser),text=text)
           msg="sudo -u bot /tmp/bot/runnable.sh"
        p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
        i=0
        while(p.poll()==None):
            time.sleep(1)
            i+=1
            if(superuser==str(update.message.from_user.id)):
                if(i==60):
                    break
            else:
                if(i==5 and (not trust)):
                    break
        if(i==5 and (not trust)):
            data="Timeout killed\n"
            p.kill()
            data+=p.stdout.read().decode("utf-8")
            stderrData=p.stderr.read().decode("utf-8")
            if(stderrData):
                data+="Errors where detected while executing!"+"\n"
                data+=stderrData
        else:
            data=p.stdout.read().decode("utf-8")
            stderrData=p.stderr.read().decode("utf-8")
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
def allHandle(update: Update, context: CallbackContext):
    bot = context.bot
    global speedTestFlag
    global ATT
    global UNAUTH
    global betaMode
    try:
        msg=update.message.text
        if(msg==None):
            return
        if(msg[0]=='#'):
            groupid=str(update.message.chat_id)
            msg=msg.replace("#","")
            data=notes.read(groupid,msg)
            if(notes.error==False):
                if("beta" == data[0:4].lower()):
                    msg=data
                else:
                    update.message.reply_text(data)
        if(update.message.from_user.id in UNAUTH):
            if("i am a human" in msg.lower()):
                UNAUTH.remove(update.message.from_user.id)
            else:
                update.message.delete()
        if(len(update.message.new_chat_members) != 0):
            update.message.reply_text("Hey there welcome!")
            if(ATT==True):
                bot.send_message(update.message.chat_id, "Please reply with message 'I am a human' to continue")
                UNAUTH.append(update.message.new_chat_members[0].id)
                
        #bot.send_message(int(superuser),"Test "+str(msg))
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        bot.send_message(int(superuser),"Error "+str(e)+" Line "+str(exc_tb.tb_lineno))
    try:
        addUserDB(update.message)
        if(betaMode==True or os.path.exists(BASEPATH+"beta")):
            try:
                msg=msg.lower()
            except:
                return
            betaMode=True
            if(msg == "beta" or msg == "hey" or msg == "ssal"):
                update.message.reply_text(randomize(["BETA at your service, how may I help you.","Yes, I am here.","Hola, senor.","Howdy!, How may I help.","What's up human, I am ready to help."]))
            elif("beta" == msg[0:4]):
                msg=msg[4:].strip()
                if(("what" in msg or "which" in msg) and "you" in msg and ("commands" in msg or "do")):
                    text=""
                    text+=randomize(["Hey, I can do these\n","Not much yet but here is a list\n","Interesting, Hmm.. What can I DO?\nMay be this list may enlighten you!\n"])
                    text+='''1) Beta what is system status / Beta status report, adding please would be sweet
2) Beta what can you do? / Beta what the commands?
3) Beta scan open ports, again please will be nicer
4) Beta any ongoing builds? / Beta anyone building?
5) Beta what is the server temperature? / Beta what is the temperture of your head?
6) Beta is firefox running? / Beta is <command> running?
7) Beta tell me today's date / Beta date now,  Please will be nice
8) Beta tell me the time now / Beta what is the time?
Super USER alert (for security sake) by the gatekeeper @abhiramshibu
 Beta start vnc server
 Beta kill vnc server
 Beta enable ATT / Beta enable captcha
                    '''
                    update.message.reply_text(text)
                elif("memory" in msg and ("report" in msg or "status" in msg or "usage" in msg or "free" in msg or "utilization" in msg)):
                    memstat(update, context)
                elif("cpu" in msg and ("report" in msg or "status" in msg or "usage" in msg or "utilization" in msg)):
                    cpustat(update, context)
                elif(("using" in msg or "hog" in msg or "bottlekneck" in msg) and "cpu" in msg):
                    data=cpuhog(update, context)
                    if("who" in msg):
                        update.message.reply_text(data.split("\n")[2].replace("User:",""))
                    elif("what" in msg):
                        update.message.reply_text(data.split("\n")[3].replace("Command:","")+" "+data.split("\n")[1].replace("PID:",""))
                elif(("server" in msg or "system" in msg or "report" in msg) and "status" in msg):
                    update.message.reply_text("Getting information")
                    cpustat(update, context)
                    memstat(update, context)
                    update.message.reply_text("Do you want speedtest results?")
                    speedTestFlag=True
                elif("scan" in msg and ("local" in msg or "open" in msg) and "port" in msg):
                    speedTestFlag=False
                    update.message.reply_text("Getting nmap results")
                    if(os.path.exists("/tmp/bot")):
                        f=open("/tmp/bot/runnable.sh","w")
                    else:
                        os.mkdir("/tmp/bot")
                        f=open("/tmp/bot/runnable.sh","w")
                    f.write("#!/usr/bin/env zsh\n")
                    os.system("chmod +x /tmp/bot/runnable.sh")
                    f.write("nmap localhost"+"\n")
                    f.close()
                    msg="sudo -u abhiram /tmp/bot/runnable.sh"
                    p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
                    while(p.poll()==None):
                        time.sleep(1)
                    data=p.stdout.read().decode("utf-8")
                    update.message.reply_text(data)
                elif("start" in msg and "vnc" in msg):
                    if(superuser==str(update.message.from_user.id)):
                        speedTestFlag=False
                        update.message.reply_text("Starting X11VNC")
                        if(os.path.exists("/tmp/bot")):
                            f=open("/tmp/bot/runnable.sh","w")
                        else:
                            os.mkdir("/tmp/bot")
                            f=open("/tmp/bot/runnable.sh","w")
                        f.write("#!/usr/bin/env zsh\n")
                        os.system("chmod +x /tmp/bot/runnable.sh")
                        f.write("x11vnc -auth guess -repeat -forever -rfbauth /home/abhiram/.vnc/passwd"+"\n")
                        f.close()
                        msg="sudo -u abhiram /tmp/bot/runnable.sh"
                        p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
                        time.sleep(1)
                        data=p.stdout.readline().decode()
                        update.message.reply_text(data)
                    else:
                        update.message.reply_text("Sorry this command is reserved for Abhiram Shibu")
                elif("kill" in msg and "vnc" in msg):
                    if(superuser==str(update.message.from_user.id)):
                        speedTestFlag=False
                        update.message.reply_text("Killing all vnc")
                        if(os.path.exists("/tmp/bot")):
                            f=open("/tmp/bot/runnable.sh","w")
                        else:
                            os.mkdir("/tmp/bot")
                            f=open("/tmp/bot/runnable.sh","w")
                        f.write("#!/usr/bin/env zsh\n")
                        os.system("chmod +x /tmp/bot/runnable.sh")
                        f.write("pkill x11vnc"+"\n")
                        f.close()
                        msg="sudo -u abhiram /tmp/bot/runnable.sh"
                        p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
                        while(p.poll()==None):
                            time.sleep(1)
                        data=p.stdout.read().decode("utf-8")
                        update.message.reply_text(data)
                    else:
                        update.message.reply_text("Sorry this command is reserved for Abhiram Shibu")
                elif(("ongoing" in msg or "current" in msg or "any" in msg) and "build" in msg):
                    speedTestFlag=False
                    if(os.path.exists("/tmp/bot")):
                        f=open("/tmp/bot/runnable.sh","w")
                    else:
                        os.mkdir("/tmp/bot")
                        f=open("/tmp/bot/runnable.sh","w")
                    f.write("#!/usr/bin/env zsh\n")
                    os.system("chmod +x /tmp/bot/runnable.sh")
                    f.write("ps ax | grep -v grep | grep 'make' "+"\n")
                    f.close()
                    msg="sudo -u abhiram /tmp/bot/runnable.sh"
                    p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
                    while(p.poll()==None):
                        time.sleep(1)
                    data=p.stdout.read().decode()
                    if(data!=""):
                        update.message.reply_text("Yes")
                    else:
                        update.message.reply_text("No")
                elif(("server" in msg or "system" in msg or "head" in msg or "brain" in msg) and "temp" in msg):
                    speedTestFlag=False
                    update.message.reply_text("Getting temperature information")
                    if(os.path.exists("/tmp/bot")):
                        f=open("/tmp/bot/runnable.sh","w")
                    else:
                        os.mkdir("/tmp/bot")
                        f=open("/tmp/bot/runnable.sh","w")
                    f.write("#!/usr/bin/env zsh\n")
                    os.system("chmod +x /tmp/bot/runnable.sh")
                    f.write("sensors | grep Package"+"\n")
                    f.close()
                    msg="sudo -u abhiram /tmp/bot/runnable.sh"
                    p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
                    while(p.poll()==None):
                        time.sleep(1)
                    data=p.stdout.read().decode("utf-8")
                    update.message.reply_text(data)
                elif("is" in msg and "running" in msg):
                    try:
                        speedTestFlag=False
                        index=msg.find("is")
                        index2=msg.find(" ",index+3)
                        process=msg[index+3:index2]
                        if(os.path.exists("/tmp/bot")):
                            f=open("/tmp/bot/runnable.sh","w")
                        else:
                            os.mkdir("/tmp/bot")
                            f=open("/tmp/bot/runnable.sh","w")
                        f.write("#!/usr/bin/env zsh\n")
                        os.system("chmod +x /tmp/bot/runnable.sh")
                        f.write("ps ax | grep -v grep | grep '"+process+"' "+"\n")
                        f.close()
                        msg="sudo -u abhiram /tmp/bot/runnable.sh"
                        p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
                        while(p.poll()==None):
                            time.sleep(1)
                        data=p.stdout.read().decode()
                        if(data!=""):
                            update.message.reply_text("Yes")
                        else:
                            update.message.reply_text("No")
                    except:
                        update.message.reply_text("Sorry critical error detected.")
                elif("date" in msg and ("what" in msg or "tell" in msg or "today" in msg or "now" in msg)):
                    speedTestFlag=False
                    if(os.path.exists("/tmp/bot")):
                        f=open("/tmp/bot/runnable.sh","w")
                    else:
                        os.mkdir("/tmp/bot")
                        f=open("/tmp/bot/runnable.sh","w")
                    f.write("#!/usr/bin/env zsh\n")
                    os.system("chmod +x /tmp/bot/runnable.sh")
                    f.write("date"+"\n")
                    f.close()
                    msg="sudo -u abhiram /tmp/bot/runnable.sh"
                    p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
                    while(p.poll()==None):
                        time.sleep(1)
                    data=p.stdout.read().decode("utf-8")
                    update.message.reply_text(data)
                elif("time" in msg and ("what" in msg or "tell" in msg or "today" in msg or "now" in msg)):
                    speedTestFlag=False
                    if(os.path.exists("/tmp/bot")):
                        f=open("/tmp/bot/runnable.sh","w")
                    else:
                        os.mkdir("/tmp/bot")
                        f=open("/tmp/bot/runnable.sh","w")
                    f.write("#!/usr/bin/env zsh\n")
                    os.system("chmod +x /tmp/bot/runnable.sh")
                    f.write("date +%I:%M:%S%P"+"\n")
                    f.close()
                    msg="sudo -u abhiram /tmp/bot/runnable.sh"
                    p=sp.Popen(msg,stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.PIPE,shell=True)
                    while(p.poll()==None):
                        time.sleep(1)
                    data=p.stdout.read().decode("utf-8")
                    update.message.reply_text(data)
                elif(("captcha" in msg or "verify" in msg or "att" in msg) and ("enable" in msg or "disable" in msg)):
                    if(superuser==str(update.message.from_user.id)):
                        if("enable" in msg):
                            if(ATT==True):
                                update.message.reply_text("Automated Turing Test(ATT) is already Enabled")
                            else:
                                ATT=True
                                update.message.reply_text("Automated Turing Test(ATT) Enabled")
                        elif("disable" in msg):
                            if(ATT==True):
                                update.message.reply_text("Automated Turing Test(ATT) Disabled")
                                ATT=False
                            else:
                                update.message.reply_text("Automated Turing Test(ATT) is already Disabled")
                    else:
                        update.message.reply_text("Sorry this command is reserved for Super User")
                        
            elif(msg=="yes" or msg=="yeah" or msg=="yup"):
                if(speedTestFlag==True):
                    st(update, context)
                    speedTestFlag=False
            elif(msg=="no" or msg=="never" or msg=="nop"):
                if(speedTestFlag==True):
                    update.message.reply_text("Ok, as you wish.")
                    speedTestFlag=False
            elif("thank" in msg.lower() or "good" in msg.lower()):
                try:
                    if(update.message.reply_to_message.from_user.id==733977759):
                        update.message.reply_text(randomize(["You are welcome","Glad I can help","☺"]))
                except:
                    pass
    except Exception as e:
        update.message.reply_text(str(e))
bot=telegram.Bot(key)
groupSend=False
def enableGroupSend():
    global groupSend
    time.sleep(10)
    bot.send_message(superuser,"Enabled Group Send")
    groupSend=True
def apcUPS():
    f=None
    if(os.path.exists(APCLOG)):
        f = sp.Popen(['tail','-F',APCLOG],stdout=sp.PIPE,stderr=sp.PIPE)
        bot.send_message(superuser,"File Opened")
    if(f):
        while True:
            line = f.stdout.readline().decode()
            bot.send_message(superuser,line)
            if(groupSend):
                bot.send_message(MAINGROUP,line)
apclogd=Thread(target=apcUPS)
apclogd.start()
groupSendd=Thread(target=enableGroupSend)
groupSendd.start()
updater = Updater(key)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('id', id))
updater.dispatcher.add_handler(CommandHandler('BETA', beta))
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
updater.dispatcher.add_handler(CommandHandler('fixPerm', fixPerm))
updater.dispatcher.add_handler(CommandHandler('fixperm', fixPerm))
updater.dispatcher.add_handler(CommandHandler('whoami', whoami))
updater.dispatcher.add_handler(CommandHandler('del', deleteMsg))
updater.dispatcher.add_handler(CommandHandler('delete', deleteMsg))
updater.dispatcher.add_handler(CommandHandler('kick', kick))
updater.dispatcher.add_handler(CommandHandler('unkick', unkick))
updater.dispatcher.add_handler(CommandHandler('whoareyou', whoareyou))
updater.dispatcher.add_handler(CommandHandler('notes', noteshandle))
updater.dispatcher.add_handler(CommandHandler('save', save))
updater.dispatcher.add_handler(CommandHandler('clear', clear))
updater.dispatcher.add_handler(CommandHandler('setuser', setuser))
updater.dispatcher.add_handler(CommandHandler('getuser', getuser))
updater.dispatcher.add_handler(CommandHandler('quota', quota))
unknown_handler = MessageHandler(Filters.text, allHandle)
updater.dispatcher.add_handler(unknown_handler)
updater.start_polling()
#updater.idle()
