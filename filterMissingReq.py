#!/usr/bin/python

import re
import os
import sys


fh1=open(sys.argv[1],'r')
fhlog=open(sys.argv[2],'w')
timediff=int(sys.argv[3])
all=int(sys.argv[4])


##############################
# based on output from:
# tshark.exe -t "a" -r .\seventh.pcapng | Out-File -Encoding UTF8 Z:\windows\seventh
# 
# wrong:
# query A solr-02.smk.dk
# query AAAA solr-02.smk.dk
#
# rigth:
# query A solr-02.smk.dk
# query response A 172.20.1.9
#
#
#
##############################

myReg=re.compile('(\d+)\s(\d+):(\d+):([0-9.]+) .*query 0x([a-z0-9]+)\s+A\s')
myReg2=re.compile('(\d+)\s(\d+):(\d+):([0-9.]+) .*query response\s+0x([a-z0-9]+)\s+A\s')
searchlines = fh1.readlines()
resDict={}
warnDict={}
tempLine = ''
tmpKey = ''
prevLine = searchlines.pop(0)

for sline in searchlines:
  sline = sline.rstrip()
  #pdb.set_trace()
  m2=myReg.search(sline)
  m=myReg2.search(sline)
  if m2:
    prevLine=sline
    prevKey=m2.group(5)
    prevsec=m2.group(3)
    #print "First: " + m2.group(2) + ":" + m2.group(3) + ":" + m2.group(4) + "->" + m2.group(5)
    #print "Key: " + prevKey
  if m:
    #print "SEC: " + m.group(2) + ":" + m.group(3) + ":" + m.group(4) + "->" + m.group(5)
    if m.group(5) == prevKey:
      nowsec=int(m.group(3)) + 0
      diff=nowsec - int(prevsec)
      resDict[prevKey]=[diff,sline]
      prevLine=sline
      prevKey=m.group(5)
      if diff >= timediff:
        warnDict[prevKey]=[diff,prevLine,sline]

if all != 0:
  for key in resDict.iterkeys():
    print key + " " + str(resDict[key])

for key in warnDict.iterkeys():
  print "WARN: " + key + " " + str(warnDict[key])

fh1.close()
fhlog.close()
