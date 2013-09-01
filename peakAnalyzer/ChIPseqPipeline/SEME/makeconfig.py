import sys
import os
from glob import *
rootdir=os.getenv("rootdir")
genomedir=os.getenv("genomedir")
from common import *

args=getargs()
inputdir=args['inputfilesdir'][0]
configfile=args['configfile'][0]
inputs=dict()
for f in glob(inputdir+"/*"):
	inputs[getfilename(f)]=open(f).read()

config=dict()
config['peakfile']=[inputdir+"/peakfile"]
config['genomedir']=[genomedir+"/"+inputs["genome"]]
config['Max_Comotif_Dist']=[inputs["Max_Comotif_Dist"]]
config['outputdir']=["output"]
config['No_of_Motif']=[int(inputs["No_of_Motif"])]
config['Min_Support']=[float(inputs['Min_Support'])]
config['Seed_Length']=[int(inputs['Seed_Length'])]
config['Max_Motif_Len']=[int(inputs['Max_Motif_Len'])]
if "mask" in inputs:
	config["mask"]=[True]
else:
	config["mask"]=[False]
if "strand" in inputs:
	config["strand"]=[True]
else:
	config["strand"]=[False]


writeconfig(configfile,config)
