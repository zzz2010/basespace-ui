import getopt
import os
import sys


optlist, args = getopt.getopt(sys.argv[1:], 'a:b:')


input1=args[0]
input2=args[1]


#print input1
#print input2

cols1=optlist[0][1].split(',')
cols2=optlist[1][1].split(',')

maplines=open(input1,'r').readlines()
linemap=dict()
lineNo=0
for line in maplines:
	comps=line.strip().split()
	keystr=""
	for col in cols1:
		keystr+=comps[int(col)-1]
	if not linemap.has_key(keystr):
		linemap[keystr]=str(lineNo)
	else:
		linemap[keystr]+="\t"+str(lineNo)
	lineNo+=1



for line in open(input2,'r').readlines():
        comps=line.strip().split()
        keystr=""
        for col in cols2:
		keystr+=comps[int(col)-1]
		if linemap.has_key(keystr):
			line_no=linemap[keystr].split()
			for nostr in line_no:
				if nostr!="":
					print maplines[int(nostr)].strip()+"\t"+line.strip()			





