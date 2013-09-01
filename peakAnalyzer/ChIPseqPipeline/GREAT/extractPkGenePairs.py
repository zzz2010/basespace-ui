import os
import sys
import sets

pkgenefile=sys.argv[1]
outfile=sys.argv[2]
tmp=open(pkgenefile, 'r')
	
pkgenedict=dict()
for line in tmp.readlines():
	line=line.strip()
	strarr=line.split("\t")
	peaks=strarr[0].split(',')
	genes=strarr[1].split(',')	
	for g in genes:
		g=g.strip()
		if g not in pkgenedict:
			pkgenedict[g]=set(peaks)
		else:
			pkgenedict[g].update(peaks)

out=open(outfile, 'a')
out.write("Genes\tChr\tStart\tEnd\n")
strout=''
for k in sorted(pkgenedict.keys()):
	glist=pkgenedict[k]

	pklist=list()  #create peak lists for each gene
	for e in glist:
		pk=list()  #create idv peak list of attributes
		pkStr= e.split(":")
		chrNo=pkStr[0]
		pk.append(int(chrNo[3:]))  #chr no
		loc=pkStr[1].split("-")
		pk.append(int(loc[0]))  #start
		pk.append(int(loc[1]))  #end
		
		# add individual pks to peaklist
		pklist.append(pk)

	sortedlist= sorted(pklist,key=lambda x:(x[0],x[1]))
	
	pkstr=str(k)
	for regions in sortedlist:
		for r in regions:
			pkstr+='\t'+ str(r)
		pkstr+='\n'
	out.write(pkstr)
out.close()
