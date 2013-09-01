import sys
import os
from glob import *
rootdir=os.getenv("rootdir")
genomedir=os.getenv("genomedir")
from common import *

filterpwm=format("python {rootdir}/PROG/filterpwm.py",locals())

args=getargs()
inputdir=args['inputfilesdir'][0]
configfile=args['configfile'][0]
inputs=dict()
for f in glob(inputdir+"/*"):
	inputs[getfilename(f)]=open(f).read()

config=dict()
config['peakfile']=[inputdir+"/peakfile"]
config['genomedir']=[genomedir+"/"+inputs["genome"]]
config['w']=[int(inputs["Max_Comotif_Dist"])]
config['FP']=[float(inputs["FP"])]
config['outputdir']=["output"]
motifdatabase=inputdir+"/motifdatabase"
motifselect=inputdir+"/motifselect"
ossystem(format("{filterpwm} -pwmfile {motifdatabase} -motifselect {motifselect} > input/pwmfile",locals()));
config['pwmfile']=["input/pwmfile"]
writeconfig(configfile,config)
