#!/usr/bin/python3
import pickle
import os
try:
	if os.path.exists("index.rss"):
		print("index.rss found, deleting")
		os.system("rm index.rss")
	os.system("wget https://forums.arctotal.com/forums/-/index.rss")
	f=open("index.rss","r")
	data=f.read()
except:
	print("Some error occured!")
	print("Exiting!")
	exit()
lis=[]
z=-1
while(1):
    z=data.find("<item>",z+1)
    if(z==-1):
        break
    lis.append(z)
start=lis
lis=[]
while(1):
    z=data.find("</item>",z+1)
    if(z==-1):
        break
    lis.append(z)
end=lis
lis=[]
title=[]
link=[]
desc=[]
for i in range(len(end)):
    lis.append("")
    title.append("")
    link.append("")
    desc.append("")
for i in range(len(end)):
    for j in range(start[i],end[i],1):
        lis[i]=lis[i]+data[j]
for i in range(len(lis)):
    lis[i]=lis[i].strip("<item>\n").strip()
    loc=lis[i].find("</title>")
    for j in range(0,loc):
        title[i]=title[i]+lis[i][j]
    title[i]=title[i].strip("<title>")
    loc=lis[i].find("<link>")
    loce=lis[i].find("</link>")
    for j in range(loc,loce):
        link[i]=link[i]+lis[i][j]
    link[i]=link[i].strip("<link>")
    loc=lis[i].find("<content:encoded>")
    loce=lis[i].find("</content:encoded>")
    for j in range(loc,loce):
        desc[i]=desc[i]+lis[i][j]
    desc[i]=desc[i].strip("<content:encoded>").strip("![CDATA[").strip("]]")

import sys
ftitle=sys.argv[1]
flink=sys.argv[2]
fdesc=sys.argv[3]
file_title=open(ftitle,"wb")
file_link=open(flink,"wb")
file_desc=open(fdesc,"wb")
pickle.dump(title,file_title)
pickle.dump(link,file_link)
pickle.dump(desc,file_desc)
file_title.close()
file_link.close()
file_desc.close()
os.system("rm index.rss")

