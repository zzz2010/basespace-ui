import sys
import os
#settings
rootdir=os.getenv('rootdir')
from common import *

pomoda=format("{rootdir}/PROG/pomoda/pomoda64",locals())
pomoclust=format("{rootdir}/PROG/pomoda/pomoclust64",locals())
extractfas=format("python {rootdir}/PROG/extractfas.py",locals())
pomoscan=format("python {rootdir}/PROG/pomoscan/zzpomoscan.py",locals())
genlogo=format("python {rootdir}/PROG/genlogo/genlogo_multi_cache.py",locals())
STAMP=format("{rootdir}/PROG/STAMP/STAMPzzz",locals())
STAMP_Score_Dist=format("{rootdir}/PROG/STAMP/ScoreDists/TransfacRand_SSD_SWU.scores",locals())

args=getargs()
configfile=args['configfile'][0]
args=readconfig(configfile,args)

pwmfile=args['pwmfile'][0]
outputdir=args['outputdir'][0]
command=format("{genlogo} -pwmfile {pwmfile} -prefix {outputdir}/",locals())
if ossystem(command):
	raise Exception("genlogo failed")

command=format("{pomoscan} -configfile {configfile}",locals())
if ossystem(command):
	raise Exception("pomoscan failed")

#ossystem("cp {src}/version {outputdir}".format(src=os.path.abspath(os.path.dirname(pomoscan)),outputdir=outputdir))
ossystem("cp {src}/version {outputdir}".format(src=os.path.abspath(sys.path[0]),outputdir=outputdir))
