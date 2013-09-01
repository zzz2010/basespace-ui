import os,sys
from math import *
def erfcc(x):
	z = abs(x)
	t = 1. / (1. + 0.5*z)
	r = t * exp(-z*z-1.26551223+t*(1.00002368+t*(.37409196+t*(.09678418+t*(-.18628806+t*(.27886807+t*(-1.13520398+t*(1.48851587+t*(-.82215223+t*.17087277)))))))))
	if (x >= 0.):
		return r
	else:
		return 2. - r

def ncdf(x):
	return 1. - 0.5*erfcc(x/(2**0.5))




bedfile=sys.argv[1]

bgscorefile=sys.argv[2]

lines=open(bgscorefile,'r').readlines()

Ex=0
Ex2=0
for line in lines:
	temp=float(line.strip())
	Ex+=temp
	Ex2+=temp*temp



Ex=Ex/len(lines)
Ex2=Ex2/len(lines)
std=sqrt(Ex2-Ex*Ex)

lines=open(bedfile,'r').readlines()

for line in lines:
	comps=line.strip().split()
	score=float(comps[len(comps)-1])
	zscore=(score-Ex)/std
	pvalue=1-ncdf(zscore)
	print line.strip()+"\t"+str(pvalue)
	























