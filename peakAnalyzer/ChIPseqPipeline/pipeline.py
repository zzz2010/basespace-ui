import os
import sys
import ConfigParser
import io
import glob
import string, threading, time

toolpath=sys.path[0]+"/"

def exec2(cmd):
	print cmd
	os.system(cmd)

def runbackground(cmdlist):
	for cmd in cmdlist:
		exec2(cmd)

def mkpath(outdir):
	if not os.path.exists(outdir):
	        os.makedirs(outdir)


taskconfigfile=sys.argv[1]

pipelineconfig=toolpath+"./pipeline.cfg"

pipeconfig = ConfigParser.ConfigParser()
pipeconfig.readfp(open(pipelineconfig))

taskconfig=ConfigParser.ConfigParser()
taskconfig.readfp(open(taskconfigfile))

inputdir=taskconfig.get("task", "dataDIR")
outdir=taskconfig.get("task", "outputDIR")
genome=taskconfig.get("task", "genome")

taskStr=""
if taskconfig.has_option("task","task"):
	taskStr=taskconfig.get("task", "task")
taskSet=set(taskStr.split(","))
if taskStr=="":
	taskSet=set()	
cmdlist=list()


if not os.path.exists(outdir):
        os.makedirs(outdir)

cmd="cp "+toolpath+"resultSummarize/*.php "+outdir+"/"
exec2(cmd)
exec2("cp "+taskconfigfile+" "+outdir+"/")
##############prepare standard peak summit bed files#################

peakdir=outdir+"/peakfiles/"
if not os.path.exists(peakdir):
        os.makedirs(peakdir)

for lib in os.listdir(inputdir):
	libdir=inputdir+"/"+lib
	if os.path.isdir(libdir):
		exec2("sh "+toolpath+"./preprocessing/preprocess.sh "+libdir+" "+taskconfig.get("task", "CCAT_FC")+" "+taskconfig.get("task", "MACS_FC")+" "+peakdir)
outf=open(peakdir+"/peakcount.html",'w')
peaklist=glob.glob(peakdir+"/*_*.bed")
fullpeaklist=glob.glob(peakdir+"/fullpeak/*_*.bed")

for peak in peaklist:
	count=len(open(peak,'r').readlines())
	peakname=os.path.basename(peak).split(".")[0]
	outf.write(peakname+":"+str(count)+"<br>\n")

outf.close()
##################peak gene association####################
outdir2=outdir+"/peakgeneAssociate/"
mkpath(outdir2)
for peak in fullpeaklist:
	cmd="sh "+toolpath+"./peakgeneAssociate/peakgeneAnnot.sh "+peak+" "+genome+" "+outdir2
	if len(taskSet)==0 or "peakgeneAssociate" in taskSet :
		exec2(cmd)
##############Denovo Motif#################
for peak in peaklist:
	peakname=os.path.basename(peak).split(".")[0]
	outdir2=outdir+"/denovoMotif/"+peakname+"/"
	mkpath(outdir2)
	cmd="sh "+toolpath+"./DenovoMotif/runMetaNovo.sh "+peak+" "+pipeconfig.get("path","GenomeDIR")+"/"+genome+"/ "+pipeconfig.get("path","WebseqtoolDIR")+" "+outdir2+" > "+outdir2+"/log.txt 2>&1"
	cmdlist.append(cmd)


#use background job queue
t=threading.Thread(target=runbackground, args=(cmdlist,))
if len(taskSet)==0 or "denovoMotif" in taskSet :
	t.start()

##############Tag around peak#################
taglist=glob.glob(inputdir+"/*/MAIN/*.tags.unique")
peaklist=glob.glob(peakdir+"/*_*.bed")
profileAroundPeaks_Dir=outdir+"/profileAroundPeaks/"
mkpath(profileAroundPeaks_Dir)
refpeaklist=list()
if taskconfig.has_option("task","refpeak"):
	refpeakstr=taskconfig.get("task","refpeak").strip().split(",")
	for rpeak in refpeakstr:
		refpeaklist.append(inputdir+"/"+rpeak)
print refpeaklist
peaklist2=peaklist+refpeaklist
if len(taskSet)==0 or "profileAroundPeaks" in taskSet :
	for peak in peaklist2:
		cmd="python "+toolpath+"./profileAroundPeaks/profileAroundPeaks_multiTag.py "+peak+" "+profileAroundPeaks_Dir+" "+" ".join(taglist)
		exec2(cmd)
		cmd2="python "+toolpath+"./profileAroundPeaks/profile5k.py "+peak+" "+profileAroundPeaks_Dir+" "+" ".join(taglist)
		exec2(cmd2)
##############peak gene Annotation#################
outdir2=outdir+"/peakAnnotation/"
mkpath(outdir2)
for peak in peaklist2:
	cmd="sh "+toolpath+"./peakAnnotation/peakAnnotation.UCSC.sh "+peak+" "+genome+" "+outdir2
	if len(taskSet)==0 or "peakAnnotation" in taskSet :
		exec2(cmd+" &")


###################repeat analysis######################
outdir2=outdir+"/repeatAnalysis/"
mkpath(outdir2)
for peak in peaklist2:
        cmd="sh "+toolpath+"./repeatAnalysis/overlaprepeat.sh "+peak+" "+genome+" "+outdir2
        if len(taskSet)==0 or "repeatAnalysis" in taskSet :
		exec2(cmd)


####################TSS Plot#######################
outdir2=outdir+"/TSSPlot/"
mkpath(outdir2)
cmd="python "+toolpath+"./TSSPlot/TssDistTable.py "+genome
for peak in peaklist2:
        cmd+=" "+peak
if len(taskSet)==0 or "TSSPlot" in taskSet :
	exec2(cmd+" > "+outdir2+"/peak_tssplot.txt")
	exec2("R "+outdir2+"/peak_tssplot.txt  --no-save "+" < "+toolpath+"./TSSPlot/plotTss.R &")



##############Conservation Plot#################
outdir2=outdir+"/conservationPlot/"
mkpath(outdir2)
for peak in peaklist2:
	cmd="sh "+toolpath+"./conservationPlot/plotCons.sh "+peak+" "+pipeconfig.get("path","phastconsDIR")+"/"+genome+" "+outdir2
	if len(taskSet)==0 or "conservationPlot" in taskSet :
		exec2(cmd+" &")

##############Genome Profile Plot#################
outdir2=outdir+"/genomeProfile/"
mkpath(outdir2)
for peak in peaklist2:
	cmd="sh "+toolpath+"./genomeProfile/profileGenome.sh "+peak+" "+genome+" "+outdir2
	if len(taskSet)==0 or "genomeProfile" in taskSet :
		exec2(cmd) 

##############Venn Diagram Plot#################
outdir2=outdir+"/peakOverlap/"
mkpath(outdir2)
for i in range(0,len(peaklist2)-1):
	peak1=peaklist2[i]
	for j in range(i+1,len(peaklist2)):
		peak2=peaklist2[j]
		cmd="sh "+toolpath+"./peakOverlap/genVenn_plus.sh "+peak1+" "+peak2+" "+outdir2
		if len(taskSet)==0 or "peakOverlap" in taskSet :
			exec2(cmd+" &")

################Input Peak Set Overlap HeatMap Plot##################
outdir2=outdir+"/peaksetOverlap/"
mkpath(outdir2)
for peak in peaklist2:
	outpeak=outdir2+os.path.basename(peak)+".bed"
	os.system("cp "+peak+" "+outpeak)
cmd="sh "+toolpath+"./peaksetOverlap/peaksetOverlap.sh '"+outdir2+"/*.bed"+"' "+outdir2
if len(taskSet)==0 or "peaksetOverlap" in taskSet :
	exec2(cmd)

##############ENCODE peak overlap Plot#################
outdir2=outdir+"/peaksetSummary/"
mkpath(outdir2)
for peak in peaklist2:
	cmd="sh "+toolpath+"./peaksetSummary/peaksetSummary.sh "+peak+" '"+pipeconfig.get("path","ENCODEchipseqDIR")+"/"+genome+"/*.narrowPeak' "+outdir2
	if len(taskSet)==0 or "peaksetSummary" in taskSet :
		exec2(cmd+" &")

##############histone Plot #################
outdir2=outdir+"/histonePlot/"
mkpath(outdir2)
cellline1=taskconfig.get("task","cellline")
cellline2=taskconfig.get("task","alternative_cellline")
histoneDir=pipeconfig.get("path","ENCODEhistoneDIR")+"/"+genome+"/"
cellline_used=cellline1
#check for cell line data
if len(glob.glob(histoneDir+"*"+cellline1+"*.bigWig"))>0:
	cellline_used=cellline1
elif len(glob.glob(histoneDir+"*"+cellline2+"*.bigWig"))>0:
	cellline_used=cellline2
else:
	cellline_used="none"
if "none" not in cellline_used:
	#check data generator: broad
	datastr="".join(glob.glob(histoneDir+"*"+cellline_used+"*.bigWig"))
	if "BroadHistone" in datastr:
		cellline_used="BroadHistone"+cellline_used
	elif "SydhHistone" in datastr:
		cellline_used="SydhHistone"+cellline_used
	elif "UwHistone" in datastr:
		cellline_used="UwHistone"+cellline_used

	for peak in peaklist2:
		cmd="python "+toolpath+"./histonePlot/plotHistoneDist.py "+peak+" "+cellline_used+" "+histoneDir+" "+outdir2
		if len(taskSet)==0 or "histonePlot" in taskSet :
			exec2(cmd)

###########################GO analysis##############################	
outdir2=outdir+"/GREAT/"
mkpath(outdir2)
for peak in peaklist2:
	bed3peak=outdir2+os.path.basename(peak)
	os.system("cut -f 1-3 "+peak+" > "+bed3peak)
	cmd="python "+toolpath+"./GREAT/runGREAT.py "+bed3peak+" "+genome+" "+outdir2
	if len(taskSet)==0 or "GREAT" in taskSet :
		exec2(cmd+" &")

###########################CENTDIST############################## 
for peak in peaklist2:
        peakname=os.path.basename(peak).split(".")[0]
        outdir2=outdir+"/CENTDIST/"+peakname+"/"
	mkpath(outdir2)
	denovoDir=outdir+"/denovoMotif/"+peakname+"/"
	cmd1="python "+toolpath+"/CENTDIST/combineDeNovo.py "+denovoDir+" "+outdir2
	cmd="sh "+toolpath+"/CENTDIST/runCENTDIST.sh "+peak+" "+pipeconfig.get("path","GenomeDIR")+"/"+genome+"/ "+outdir2+"/motifDB "+pipeconfig.get("path","WebseqtoolDIR")+" "+outdir2
	if len(taskSet)==0 or "CENTDIST" in taskSet :
		exec2(cmd1)
		exec2(cmd)
if len(taskSet)==0 or "denovoMotif" in taskSet :	
	t.join()
