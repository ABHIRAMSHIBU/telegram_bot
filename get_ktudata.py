import os
os.system("wget https://ktu.edu.in/eu/core/announcements.htm")
f=open("announcements.htm")
os.remove("announcements.htm")

class announcements:
    def __init__(self):
        self.title=''
        

count=0
l_title=[]
l_desc=[]
l_data=[]
while(True):
    line=f.readline()
    if '<!-- <a target="_blank">' in line:
        l_data.append(line)
        if count>=9:
            break
        count+=1
        
def desc(p):
   return p[p.find('</b>')+5:p.find('<!-- </a> -->')]

def title(a):
	return a[a.find('<b>')+3:a.find('</b>')]


for i in range(len(l_data)):
	l_title.append(title(l_data[i]))



for i in range(len(l_data)):
    l_desc.append(desc(l_data[i]))

import pickle
f1=open("ktudata_title.bin","wb")
pickle.dump(l_title,f1)
f2=open("ktudata_desc.bin","wb")
pickle.dump(l_desc,f2)

f1.close()
f2.close()


