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

for i in range(0,len(ENCpeaks)):
	peakfile=ENCpeaks[i].replace(commonPrefix,"").replace(commonSuffix,"")
	peakcount=len(open(ENCpeaks[i],'r').readlines())
	print peakfile+"\t"+str(peakcount)
