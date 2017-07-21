#!/usr/bin/python3

import time
import os
import pickle

def changeindex(fname1,fname2):
    flag=True
    change_index=[]
    ftitle2=open(fname1,"rb")
    ftitle1=open(fname2,"rb")
    fchangedindex=open("changeindex.bin","wb")
    
    l1=pickle.load(ftitle1)
    l2=pickle.load(ftitle2)
    
    ftitle1.close()
    ftitle2.close()
    
    for i in range(len(l2)):
        if l2[i] not in l1:
            change_index.append(i)
    if len(change_index)==0:
        flag=False
    pickle.dump(change_index,fchangedindex)
    return flag


while(True):
    os.system("python3 arc_get.py title1.bin link1.bin desc2.bin")
    changeindex("title1.bin","title2.bin")
    time.sleep(3600)
    os.system("python3 arc_get.py title2.bin link2.bin desc2.bin")
    time.sleep(3600)
    changeindex("title2.bin","title1.bin")
    
    
    
    