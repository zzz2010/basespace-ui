import os, sys


toolpath=sys.path[0]+"/"

peakdata=sys.argv[1]
outdir=sys.argv[2]

tagcountlist=list()
xlslist=list()
for tagdata in sys.argv[3:]:
	peakname=os.path.basename(peakdata)+".5k"
	tagname=os.path.basename(tagdata)
	outfl=outdir+"/"+tagname+"_around_"+peakname+".aroundPeaks.profile.xls"
	xlslist.append(outfl)
	cmd="java -cp "+toolpath+"../LGL/LGL.jar LGL.shortReads.ProfileRegion2 "+tagdata+" "+peakdata+"  "+toolpath+"./profile_10bp_1Kbins.txt "+outdir+"/"+tagname+"_around_"+peakname+".aroundPeaks"
	if len(xlslist)< len(sys.argv)-4:
		cmd+=" &"
	os.system(cmd)
	tagcountlist.append(len(open(tagdata,"r").readlines()))

print tagcountlist
normstr=""
for tcnt in tagcountlist:
	normstr+=" "+str(float(tcnt)/1000000)
cmd="R "+" ".join(xlslist)+normstr+" --no-save < /data5/zhizhuo/hTERT/CHH_new/FDR02/plotTagDensity_multi.R"
os.system(cmd)
print cmd
#os.system("rm "+outdir+"/*.xls")
os.system("rm "+outdir+"/*.SVG")

