import os
import sys
import glob

toolpath=sys.path[0]
denovDir=sys.argv[1]
outdir=sys.argv[2]
pwmfiles=glob.glob(denovDir+"*_sorted.pwm")
pwmlist=list()
outf=open(outdir+"/motifDB",'w')
for pwmfl in pwmfiles:
	lines=open(pwmfl,'r').readlines()
	PWMcount=0
	for line in lines:
		outf.write(line)
		if "DE" in line:
			comps=line.strip().split()
			pwmlist.append(comps[1])
		if "XX" in line:
			PWMcount+=1

		if PWMcount > 1:
			break

outf.write(open(toolpath+"/mixDB.pwm",'r').read())
outf.close()

outf=open(outdir+"/motifgroup",'w')
for pwm in pwmlist:
	outf.write(pwm+"\tDeNovo\n")
outf.write(open(toolpath+"/motifgroup",'r').read())
outf.close()
