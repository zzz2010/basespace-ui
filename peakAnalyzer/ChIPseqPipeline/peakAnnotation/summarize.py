import os,glob, subprocess, re, zipfile, sys

toolpath=sys.path[0]

libname=sys.argv[1]
genome=sys.argv[2]
outdir=sys.argv[3]
#file1=glob.glob(outdir+"/*.distal-promoter.txt")[0]

#libname=os.path.basename(file1).replace(".distal-promoter.txt","")
keyOrderL = ['distal promoter', 'promoter', 'exon', 'intron', '3-prime', 'inter-genic']
peakDistFile=outdir+"/"+libname+".summary"
out=open(peakDistFile,'w')
for key in keyOrderL:
	key2=key.replace(" ","-")
	count=len(open(outdir+"/"+libname+"."+key2+".txt").readlines())
	out.write(key+"\t"+str(count)+"\n")

out.close()
imageFile=peakDistFile+".png"
pvalueFile=peakDistFile+".pvalue"
cmd='R --vanilla --args inputfile=' + peakDistFile + ' outputfile=' + imageFile + ' pvaluefile=' + pvalueFile +' refpvalue='+toolpath+'/pvalue/'+genome+'.genomeRegion.txt < '+toolpath+'/peakDist.r'
print cmd
os.system(cmd) 
