import os
import sys
import math

def mean(numbers):
	if len(numbers) ==0:
		return 0
	return sum(numbers) / len(numbers)

def quantile(rawlist,n):
	qlist=list()
	sortedlist=sorted(rawlist, reverse=True)
	binsize=((len(sortedlist)/float(n)))
	for i in range(0,n):
		end=int((i+1)*binsize)
		start=int(i*binsize)
		if end > len(sortedlist):
			end=len(sortedlist)
		qlist.append(mean(sortedlist[start:end]))		
	return qlist
	
bed1=sys.argv[1]
bed2=sys.argv[2]
peakoverlap=sys.argv[3]

dict1=dict()
dict2=dict()

lines=open(bed1,'r').readlines()

for line in lines:
	comps=line.strip().split()
	dict1[comps[2]]=float(comps[5])

lines=open(bed2,'r').readlines()

for line in lines:
        comps=line.strip().split()
        dict2[comps[2]]=float(comps[5])

left_uniq=list()
left_right=list()
right_left=list()
right_uniq=list()

lines=open(peakoverlap,'r').readlines()

for line in lines[1:]:
        comps=line.strip().split()
        if comps[0] == "0":
		right_uniq.append(dict2[comps[1]])
	elif comps[1] == "0":
		left_uniq.append(dict1[comps[0]])
	else:
		left_right.append(dict1[comps[0]])
		right_left.append(dict2[comps[1]])

print "\t".join(map(str,quantile(left_uniq,10)))
print "\t".join(map(str,quantile(left_right,10)))
print "\t".join(map(str,quantile(right_left,10)))
print "\t".join(map(str,quantile(right_uniq,10)))

