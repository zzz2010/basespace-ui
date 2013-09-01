import os
import sys
import glob
import commands
import math

toolpath=sys.path[0]
genome=sys.argv[1]
peaklist=list()
tssbed=toolpath+"/tss/"+genome+".tss"
maxdist=10000
binN=200
binstep=maxdist*2/binN

outstr=str(-maxdist+binstep/2)
for i in range(1,binN):
	pos=i*binstep-maxdist+binstep/2
	outstr+="\t"+str(pos)

print outstr


def getdist(line):
	comps=line.strip().split()
	first=(int(comps[1])+int(comps[2]))/2
	for i in range(3,len(comps)):
		if "chr" in comps[i]:
			break
	second=(int(comps[i+1])+int(comps[i+2]))/2
	flag="+"
	if "-" in comps[i+3:]:
		flag="-"
	dist=first-second
	if flag=="-":
		dist=0-dist
	return dist

for peak in sys.argv[2:]:
	peaklist.append(peak)
		
for peak in peaklist:
	cmd="closestBed -t first -d -a "+peak+" -b "+tssbed
	count=[0]*binN
	(status,output)=commands.getstatusoutput(cmd)
	if status==0:
		lines=output.split("\n")
		for line in lines:
			if "chrM" in line:
				continue
			dist=getdist(line)
			if math.fabs(dist)<maxdist:
				binId=(dist+maxdist)/binstep
				count[binId]+=1
	peakname=os.path.basename(peak).split(".")[0]
	outstr=peakname
	for i in range(0,binN):
		outstr+="\t"+str(count[i])
	print outstr		
							
