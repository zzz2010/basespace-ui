import os
import glob
import sys

outdir=sys.argv[1]
peaklist=glob.glob(outdir+"/*summits.bed") 

for f in peaklist:
	cmd="sort -k 5 -nr"+ f
	os.system(cmd)
	 
