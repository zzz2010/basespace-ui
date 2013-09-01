import os, sys
import subprocess

def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
	raise IOError(err)
    return int(result.strip().split()[0])

toolpath=sys.path[0]+"/"

peakdata=sys.argv[1]
outdir=sys.argv[2]


flagset=set()

lines=open(peakdata,'r').readlines()
lid=0
for line in lines:
	comps=line.strip().split()
	if comps[len(comps)-1]=='-':
		flagset.add(lid)
	lid=lid+1

tagcountlist=list()
xlslist=list()
for tagdata in sys.argv[3:]:
	peakname=os.path.basename(peakdata)+".5k"
	tagname=os.path.basename(tagdata)
	outfl=outdir+"/"+tagname+"_around_"+peakname+".aroundPeaks.profile.xls"
	xlslist.append(outfl)
	cmd="java -cp "+toolpath+"../LGL/LGL.jar LGL.shortReads.ProfileRegion2 "+tagdata+" "+peakdata+"  "+toolpath+"./profile_10bp_500bins.txt "+outdir+"/"+tagname+"_around_"+peakname+".aroundPeaks"
	if len(xlslist)< len(sys.argv)-4:
		cmd+=" "
#	os.system(cmd)
#	lines=open(outfl,"r").readlines()
	tagcountlist.append(file_len(tagdata))
#	outf=open(outfl,"w")
#	
#	for lid in range(0,len(lines)):
#		outstr=lines[lid]
#		if lid in flagset:
#			comps=lines[lid].strip().split()
#			comps.reverse()
#			outstr="\t".join(comps)+"\t\n"
#		outf.write(outstr)
#print tagcountlist
normstr=""
for tcnt in tagcountlist:
	normstr+=" "+str(float(tcnt)/1000000)
cmd="R "+" ".join(xlslist)+normstr+" --no-save < ./plotTagDensity_multi.R"
os.system(cmd)

print cmd
#os.system("rm "+outdir+"/*.xls")
os.system("rm "+outdir+"/*.SVG")

