#!/usr/bin/python3
import pickle
fin=open("announcement_data.bin","ab")
fout=open("announcement_data.bin","rb")
import os


class announcement():
    def __init__(self,title='',desc='',img=''):
        self.title=title
        self.desc=desc
        self.img=img
        
    def display(self):
        return "Title: "+self.title+"\n"+"Desc: "+self.desc+"\n"+"img src: "+self.img+"\n"

l=announcement()
pickle.dump(l,fin)
        

while(True):
    fin.close()
    fout.close()
    ch=input("\n\nEnter the choice:\n\n1.See the data\n\n2.Enter new data\n\n3.Delete a data\n\n4.mark finished\n\n5.Quit\n\n")
    
    if ch==2 or ch=='2':
        pos=input("\nEnter Position\n")
        title=input("Enter the announcement title:\n")
        desc=input("Enter the description:\n")
        img=input("Enter the img source\n")
        fout=open("announcement_data.bin","rb")
        an=announcement(title,desc,img)
        l=pickle.load(fout)
        l.insert(int(pos)-1,an)
        fin=open("announcement_data.bin","wb")
        pickle.dump(l,fin)

    if ch==1 or ch=='1':
        fout=open("announcement_data.bin","rb")
        l=pickle.load(fout)
        for i in range(len(l)):
            print("\n"+str(i+1)+"\n"+l[i].display())
   
    if ch==3 or ch=="3":
        fout=open("announcement_data.bin","rb")
        ch=input("Enter the no you want to delete\n")
        l=pickle.load(fout)
        del l[int(ch)-1]
        fin=open("announcement_data.bin","wb")
        pickle.dump(l,fin)
    


    if ch==4 or ch=="4":
        fout=open("announcement_data.bin","rb")
        ch=input("Enter the no you want to mark finished\n")
        l=pickle.load(fout)
        l[int(ch)-1].title+=u'\u274c'
        fin=open("announcement_data.bin","wb")
        pickle.dump(l,fin)

    if ch==5 or ch=="5":
        quit()
			

	
			

	


