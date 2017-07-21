#!/usr/bin/python3

import pickle
import os 
os.system("python3 arc_get.py title2.bin link2.bin desc2.bin")

def changeindex(fname1,fname2):
    change_index=[]
    ftitle2=open(fname1,"rb")
    ftitle1=open(fname2,"rb")
    
    l1=pickle.load(ftitle1)
    l2=pickle.load(ftitle2)
    
    ftitle1.close()
    ftitle2.close()
    
    for i in range(len(l2)):
        if l2[i] not in l1:
            change_index.append(i)
            
    return change_index
        
    

        