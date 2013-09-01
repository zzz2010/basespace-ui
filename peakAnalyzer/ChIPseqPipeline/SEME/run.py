import sys
import os
#settings
#rootdir=os.getenv('rootdir')

from common import *
#toolpath=sys.path[0]
rootdir="/home/sokemay/ChIPseqPipeline/webseqtools2"
toolpath=rootdir+"/TASKS/SEME"
SEME=format("time java -d64 -Djava.awt.headless=true -XX:-UseParallelGC -server -Xmx4g -jar {toolpath}/SEME1.0.jar ",locals())
JEval=format("time java -d64 -Djava.awt.headless=true -Xmx2g -jar {toolpath}/JEvaluator.jar -match {toolpath}/../metaNovo/mixDB.pwm ",locals())
extractfas=format("python {rootdir}/PROG/extractfas.py",locals())
pomoscan=format("python {rootdir}/PROG/pomoscan/zzpomoscan.py",locals())
genlogo=format("python {rootdir}/PROG/genlogo/genlogo_multi_cache.py",locals())
STAMP=format("{rootdir}/PROG/STAMP/STAMPzzz",locals())
STAMP_Score_Dist=format("{rootdir}/PROG/STAMP/ScoreDists/TransfacRand_SSD_SWU.scores",locals())

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")


ossystem("pwd") 
peakfile=sys.argv[1]
genomedir=sys.argv[2]
outputdir=sys.argv[3]
seqlen=2*200
fastafile=outputdir+"/fastafile.fa"
No_of_Motif=5
Min_Support=0.05
Seed_Length=5
Max_Motif_Len=20
flag=" "
if str2bool("true"):
	flag+="-mask "
if str2bool("false"):
	flag+="-strand "
topN=10000

if Seed_Length<0 or Seed_Length>7:
	Seed_Length=5

if Min_Support<0 or Min_Support>1:
	Min_Support=0.05

if seqlen>1000:
	print "co-motif distance is too long: "+str(seqlen)
	seqlen=1000
if Max_Motif_Len>30:
	print "maximum motif length is too long: "+str(Max_Motif_Len)
	Max_Motif_Len=30

command="python "+toolpath+"/generate2FA.py "+peakfile+" "+str(seqlen)+" "+genomedir+" "+outputdir
posfa=outputdir+"/posfa.fa"
negfa=outputdir+"/negfa.fa"
if ossystem(command):
	raise Exception(command+"\nfailed")
#command=format("{extractfas} -genomedir {genomedir} -peakfile {peakfile} -w {seqlen} > {fastafile}.all",locals())
#if ossystem(command):
#	raise Exception("Extract sequence failed")
#if topN>0:
#	topNtimes2=topN*2
#	command=format("head -{topNtimes2} {fastafile}.all > {fastafile}",locals())
#	if ossystem(command):
#		raise Exception(command+"\nfailed")
#else:
#	command=format("cp {fastafile}.all {fastafile}",locals())
#	if ossystem(command):
#		raise Exception(command+"\nfailed")

command=format("{SEME} {flag} -i {posfa} -c {negfa} -prefix {outputdir} -n {No_of_Motif} -supp {Min_Support}  -seedlen {Seed_Length} -maxlen {Max_Motif_Len}  ",locals())
if ossystem(command):
	raise Exception("denovo failed")


pwmfile=format("{outputdir}/SEME_clust.pwm",locals())
#command=format("{pomoscan} -pwmfile {pwmfile} -fastafile {posfa} -outputdir {outputdir}",locals())
#if ossystem(command):
#	raise Exception("scan denovo failed")

command=format("{genlogo} -pwmfile {pwmfile} -prefix {outputdir}/",locals())
if ossystem(command):
	raise Exception("genlogo failed")

resultfile = format("{outputdir}/SEME_clust.pwm",locals())
command=format("{JEval} -prefix {outputdir} -i {posfa} -c {negfa} -pwm {resultfile} -roc ",locals())

if ossystem(command):
	raise Exception("JEval failed")
ossystem("rm -f {outputdir}/*.fa")
ossystem("rm -f {outputdir}/*.pos")
