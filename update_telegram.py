#!/usr/bin/python3
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
		a.append("\n"+str(i+1)+". "+l[i]+"\n")
	for i in l:
		bot.send_message(chat_id=update.message.chat_id, text=i)

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
		a.append("\n"+str(i+1)+". "+l[i]+"\n")
	for i in l:
		bot.send_message(chat_id=update.message.chat_id, text=i)
			


def newdata(pos,an):
	#pos=input("\nEnter Position\n")
	#an=input("Enter the announcement\n")
	fout=open("announcement_data.bin","rb")
	l=pickle.load(fout)
	l.insert(int(pos)-1,an)
	fin=open("announcement_data.bin","wb")
	pickle.dump(l,fin)
			
def deldata(pos):
	fout=open("announcement_data.bin","rb")
	#pos=input("Enter the no you want to delete\n")
	l=pickle.load(fout)
	del l[int(pos)-1]
	fin=open("announcement_data.bin","wb")
	pickle.dump(l,fin)

def mark_finished(pos):
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
			


def newdata(pos,an):
	#pos=input("\nEnter Position\n")
	#an=input("Enter the announcement\n")
	fout=open("announcement_data.bin","rb")
	l=pickle.load(fout)
	l.insert(int(pos)-1,an)
	fin=open("announcement_data.bin","wb")
	pickle.dump(l,fin)
			
def deldata(pos):
	fout=open("announcement_data.bin","rb")
	#pos=input("Enter the no you want to delete\n")
	l=pickle.load(fout)
	del l[int(pos)-1]
	fin=open("announcement_data.bin","wb")
	pickle.dump(l,fin)

def mark_finished(pos):
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
	



