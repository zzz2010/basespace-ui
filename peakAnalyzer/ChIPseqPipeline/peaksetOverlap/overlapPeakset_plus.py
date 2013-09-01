import os
import sys
import glob
import commands
import math
import StringOps
import random
import bisect
import math

#globstr="/home/chipseq/public_html/encode_chipseq/hg19/*.narrowPeak"
globstr=sys.argv[1]
scorecol=int(sys.argv[2])
outdir=sys.argv[3]


toolpath=sys.path[0]
outf1=open(outdir+"/peakset_overlap.txt",'w')
ENCpeaks=glob.glob(globstr)
#print ENCpeaks
commonPrefix=os.path.commonprefix(ENCpeaks)
commonSuffix=StringOps.CommonSuffixString(ENCpeaks)

peakCount=dict()
numBreak=20
peakScores=dict()
peakBreaks=dict()
peakNames=list()
headerstr=""
peakBrPos=dict()
totalpeakCount=0
tmpkey=str(random.randrange(10000000))
tempBGpeaks=list()
tempBGprefix="/tmp/"+tmpkey+"BG.peak"

for i in range(0,len(ENCpeaks)):
	peakfile=ENCpeaks[i].replace(commonPrefix,"").replace(commonSuffix,"")
	print peakfile
	peakNames.append(peakfile)
	if i==0:
		headerstr=peakfile
	else:
		headerstr+="\t"+peakfile
	lines=open(ENCpeaks[i],'r').readlines()
	peakScores[peakfile]=list()
	for line in lines:
		print line
		comps=line.strip().split()
		peakScores[peakfile].append(float(comps[scorecol-1]))
	peakScores[peakfile].sort()
	peakCount[peakfile]=len(peakScores[peakfile])
	peakBreaks[peakfile]=list()
	totalpeakCount+=len(peakScores[peakfile])
	os.system("python "+toolpath+"/makeflankBG.py "+ENCpeaks[i]+" > "+tempBGprefix+"_"+peakfile)
	tempBGpeaks.append(tempBGprefix+"_"+peakfile)
	for ii in range(1,numBreak+1):
		peakBreaks[peakfile].append(peakScores[peakfile][int(math.ceil(ii*float(len(peakScores[peakfile]))/numBreak))-1])
	peakBreaks[peakfile]=list(set(peakBreaks[peakfile]))
	peakBreaks[peakfile].sort()
	peakBrPos[peakfile]=list()
	for pb in peakBreaks[peakfile]:
		peakBrPos[peakfile].append(bisect.bisect_left(peakScores[peakfile],pb))
print peakNames


outf1.write(headerstr+"\n")

peakBGcount=dict()
for i in range(0,len(ENCpeaks)):
	mainpeak=ENCpeaks[i]
	outstr=peakNames[i]
	mainpeak_name=ENCpeaks[i].replace(commonPrefix,"").replace(commonSuffix,"")
	for j in range(0,len(ENCpeaks)):
		encpeak=ENCpeaks[j]
		encpeak_name=ENCpeaks[j].replace(commonPrefix,"").replace(commonSuffix,"")
		main_N2=1
		outfile="/tmp/"+tmpkey+mainpeak_name+"__"+encpeak_name
		maxrate=0
		cmd="windowBed -u -w 500 -a "+mainpeak+" -b "+encpeak+" > "+outfile
		os.system(cmd)
		lines=open(outfile,'r').readlines()
		main_N2=len(lines)
		outstr+="\t"+str(main_N2)
		os.system("windowBed -u -w 500 -a "+tempBGpeaks[i]+" -b "+ENCpeaks[j]+" >> "+tempBGpeaks[i]+".overlap")
	peakBGcount[mainpeak_name]=len(open(tempBGpeaks[i]+".overlap",'r').readlines())
	outf1.write(outstr+"\n")
outf1.close()


for peak in peakNames:
	outf2=open(outdir+"/"+peak+"_profile.txt",'w')
	profile=outdir+"/"+peak+"_profile.txt"	
	header="\t".join(map(str,peakBrPos[peak]))
	outf2.write(header+"\n")
	for peak2 in peakNames:
		if peak == peak2:
			continue
		histo=[0]*(len(peakBreaks[peak]))
		olfile="/tmp/"+tmpkey+peak+"__"+peak2
		lines=open(olfile,'r').readlines()
		for line in lines:
			comps=line.strip().split()
			score=float(comps[scorecol-1])
			insert_point = bisect.bisect_left(peakBreaks[peak], score)
			histo[insert_point]+=1
		outstr=peak2+"\t"
		outstr+="\t".join(map(str,histo))
		outf2.write(outstr+"\n")
	outf2.close()
	noiselevel=float(peakBGcount[peak])/len(peakBreaks[peak])
	os.system("R "+profile+" "+str(noiselevel)+" --no-save < "+toolpath+"/plotPeakCorr.R")

os.system("rm /tmp/"+tmpkey+"*")
