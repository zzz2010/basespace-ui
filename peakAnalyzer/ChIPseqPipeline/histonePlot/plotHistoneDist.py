# python plotHistoneDist.py CHB115_guoliang.peak Hmec
import os
import sys
import glob

peakfile1=sys.argv[1]
cellline=sys.argv[2]
histoneDir=sys.argv[3]
outdir=sys.argv[4]

toolpath=sys.path[0]+"/"

wigfiles=glob.glob(histoneDir+"/*"+cellline+"*")
peakfile=outdir+"/"+os.path.basename(peakfile1)
os.system(toolpath+"../ZZZ/centerBed "+peakfile1+" > "+peakfile)

datfiles_str=""
for wfl in wigfiles:
	histone=os.path.splitext(os.path.basename(wfl))[0]
	histone=histone.split(cellline)[1]
	datfiles_str+=peakfile+"__"+histone+".dat "
	os.system(toolpath+"./plotWigDensity_peak.sh "+peakfile+" "+wfl+" > "+peakfile+"__"+histone+".dat")

os.system("R "+datfiles_str+" --no-save --args --slave < "+toolpath+"plotBigWigSummary_multi2.R") 
#os.system("R "+datfiles_str+" --no-save --args --slave < "+toolpath+"plotGaye.R")
 
os.system("rm "+datfiles_str)
