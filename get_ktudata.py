import os
os.system("curl https://ktu.edu.in/eu/core/announcements.htm -o /tmp/announcements.htm")
f=open("/tmp/announcements.htm")
fr=open("/tmp/announcements.htm")
os.remove("/tmp/announcements.htm")

z=fr.read()
l=z.split("\n")

q=[]
for i in range(len(l)):
     if "<!-- <a target=" in l[i]:
            q.append(i)


rest=[]
k=[]
for i in range(len(q)):
    rest=[]
    if(i==len(q)-1):
        break
    for j in range(q[i],q[i+1]):
        rest.append(l[j])
    k.append(rest)

def getlist(string):
    a=[]
    for i in range(len(q)):
        a.append([])

    for i in range(len(k)):
        for j in range(len(k[i])):
            if string in k[i][j]:
                 a[i].append(k[i][j])
    return a
            

time=getlist('<label class="news-date">')

for i in range(len(time)):
    for j in range(len(time[i])):
        #print(str(i)+"."+"]n"+link[i][j])
        #link[i][j]=(link[i][j][link[i][j].find('<a href'):])
        time[i][j]=(time[i][j][time[i][j].find('-date">')+7:time[i][j].find('</label>')][:10])




link=getlist('<a href=')
#link[0][0][link[0][0].find('<b>'):link[0][0].find('</b>')]
for i in range(len(link)):
    for j in range(len(link[i])):
        #print(str(i)+"."+"]n"+link[i][j])
        link[i][j]=(link[i][j][link[i][j].find('<a href'):])


#class announcements:
 #   def __init__(self):
  #      self.title=''
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
f1=open("/tmp/ktudata_title.bin","wb")
pickle.dump(l_title,f1)
f2=open("/tmp/ktudata_desc.bin","wb")
pickle.dump(l_desc,f2)
f3=open("/tmp/ktudata_link.bin","wb")
pickle.dump(link[:10],f3)
f4=open("/tmp/ktudata_time.bin","wb")
pickle.dump(time[:10],f4)

f1.close()
f2.close()
f3.close()
f4.close()