'''
Created on Mar 28, 2013

@author: soke may
'''
import os
import glob
import sys

outdir=sys.argv[1]
peaklist=glob.glob(outdir+"/*summits.bed") 

for f in peaklist:
    tmp=f+".tmp"
    os.system("mv " + f + " " + tmp)
    cmd="sort -k 5 -nr "+ tmp + " > " + f
    os.system(cmd)
    os.system("rm " +tmp)
     
