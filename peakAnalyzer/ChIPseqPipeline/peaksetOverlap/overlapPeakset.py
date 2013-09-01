import os
import sys
import glob
import commands
import math
import StringOps

#globstr="/home/chipseq/public_html/encode_chipseq/hg19/*.narrowPeak"
globstr=sys.argv[1]

ENCpeaks=glob.glob(globstr)
commonPrefix=os.path.commonprefix(ENCpeaks)
commonSuffix=StringOps.CommonSuffixString(ENCpeaks)

peakNames=list()
headerstr=""
for i in range(0,len(ENCpeaks)):
	peakfile=ENCpeaks[i].replace(commonPrefix,"").replace(commonSuffix,"")
	peakNames.append(peakfile)
	if i==0:
		headerstr=peakfile
	else:
		headerstr+="\t"+peakfile

print headerstr

for i in range(0,len(ENCpeaks)):
	mainpeak=ENCpeaks[i]
	outstr=peakNames[i]
	for j in range(0,len(ENCpeaks)):
		encpeak=ENCpeaks[j]
		main_N2=1
		maxrate=0
		cmd="windowBed -u -w 500 -a "+mainpeak+" -b "+encpeak
		(status,output)=commands.getstatusoutput(cmd)
		if status==0:
			main_N2=len(output.split("\n"))
		outstr+="\t"+str(main_N2)
	print outstr
