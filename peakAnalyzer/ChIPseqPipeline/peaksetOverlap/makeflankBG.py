import os
import sys
import random

input_bed=sys.argv[1]

shift=5000

lines=open(input_bed,'r').readlines()
random.seed(12345789)

for line in lines:
	comps=line.strip().split()
	outstr=comps[0]+"\t"
	first=int(comps[1])
	anchorlen=int(comps[2])-first
	flank=shift+anchorlen
	if random.random()<0.6 and first > flank: #shift left
		outstr+=str(first-flank)+"\t"+str(int(comps[2])-flank)
	else:
		outstr+=str(first+flank)+"\t"+str(int(comps[2])+flank)
	outstr+="\t"+comps[3]
	
	print outstr
