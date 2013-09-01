import os
import sys


peakgenefile=sys.argv[1]



def TssDistance(line):
	comps=line.strip().split()
	genecol=4
	for i in range(4,len(comps)):
		if "chr" in comps[i]:
			break
	genecol=i
	distance=0
	peak=int(comps[1])
	if comps[genecol+3]=="+":
		tss=int(comps[genecol+1])
		distance=peak-tss
	else:
		tss=int(comps[genecol+2])
		distance=tss-peak

	return distance

def INOUTGeneBody(line):
	comps=line.strip().split()
        genecol=4
        for i in range(4,len(comps)):
                if "chr" in comps[i]:
                        break
        genecol=i
        peak=int(comps[1])
	left=int(comps[genecol+1])
	right=int(comps[genecol+2])
	if peak < left or peak > right:
		return "OUT"
	else:
		return "IN"


def regionAnnote(line):
	comps=line.strip().split()
	genecol=4
	for i in range(4,len(comps)):
		if "chr" in comps[i]:
			break
	genecol=i
	peak=int(comps[1])
	left=int(comps[genecol+1])
	right=int(comps[genecol+2])
	strand=comps[genecol+3]
	if (abs(left-peak)<2500 and strand == "+" ) or (abs(right-peak)<2500 and strand == "-"):
		return "proximal_promoter"
	elif ( peak < left and left-peak<2500 and strand == "-" ) or ( right < peak and peak-right<2500 and strand == "+" ):
		return "3_prime"
	elif ((left-peak)>2500 and (left-peak)<20000 and strand == "+" ) or ((peak-right)>2500 and (peak-right)<20000 and strand == "-"):
		return "distal_promoter"
	elif peak > left and peak < right:
	                 return "Gene_Body"
	else:
		return "inter_genic"
lines=open(peakgenefile,'r').readlines()

header=lines[0].strip()

header+="\tDistance2TSS\tIN/OUTGeneBody\tGeneRegion"
print header
for line in lines[1:]:
	line=line.strip()
	if len(line)<10:
		continue
	distance=str(TssDistance(line))
	inout=INOUTGeneBody(line)
	geneRegion=regionAnnote(line)
	line+="\t"+distance+"\t"+inout+"\t"+geneRegion
	print line
	
