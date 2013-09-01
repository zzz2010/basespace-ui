import os
import sys

rootdir=os.getenv('rootdir')

from common import *
extractfas=format("python {rootdir}/PROG/extractfas.py",locals())
try:
	peakfile=sys.argv[1]
	peakwidth=sys.argv[2]
	genomedir=sys.argv[3]
	outputdir="."
	if len(sys.argv)>4:
		outputdir=sys.argv[4]
	
	ossystem(extractfas+" -genomedir "+genomedir+" -peakfile "+peakfile+" -w "+peakwidth+" > "+outputdir+"/posfa.fa")
	outBG=open(outputdir+"/bg.peak",'w')
	lines=open(peakfile,"r").readlines()
	bias=int(float(peakwidth))*3
	bias=1000
	for line in lines:
		comps=line.strip().split()
		if len(comps)==0:
			continue
		chrom=comps[0]
		leftbg=list()
		rightbg=list()
		leftbg.append(chrom)
		rightbg.append(chrom)
		for el in comps[1:3]:
			left1=int(float(el))-bias
			if(left1>0):
				leftbg.append(str(left1))
			right1=int(float(el))+bias
			rightbg.append(str(right1))
		if(len(leftbg)==len(rightbg)):
			outBG.write("\t".join(leftbg)+"\n")
		outBG.write("\t".join(rightbg)+"\n")

	outBG.close()
	ossystem(extractfas+" -genomedir "+genomedir+" -peakfile "+outputdir+"/bg.peak"+" -w "+peakwidth+" > "+outputdir+"/negfa.fa")
except Exception,e:
	print("generate2FA peakfile peakwidth genomedir <outputdir>")
	print e
