Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
outdir<-Args[2]
result<-Args[3]

peaks<-read.table(result)
pkmat<-as.matrix(peaks[-1,])	
colnames(pkmat)<-as.matrix(peaks[1,])

#num peaks
npeaks<-nrow(pkmat)

#basic stats for length, tags and fold enrichment
length<-as.numeric(pkmat[,"length"])
tags<-as.numeric(pkmat[,"tags"])
fe<-as.numeric(pkmat[,"fold_enrichment"])
p<-as.numeric(pkmat[,"-10*log10(pvalue)"])
tmplist<-list(l=length,t=tags,f=fe)

minlist<-c()
maxlist<-c()
sdlist<-c()
meanlist<-c()

for(i in c('l','t','f')){
minlist<-c(minlist,min(tmplist[[i]]))
maxlist<-c(maxlist,max(tmplist[[i]]))
meanlist<-c(meanlist,mean(tmplist[[i]]))
sdlist<-c(sdlist,sd(tmplist[[i]]))
}
statsCols<-rbind(minlist,maxlist,meanlist,sdlist)
statsCols<-round(statsCols,2)
rownames(statsCols)<-c("Min","Max","Mean","Standard Deviation")

fethr<-c()
feRange<-c(10,20,50)
for(i in feRange){
	fethr<-c(fethr, length(which(fe>i)))
}
names(fethr)<-paste(">",feRange, sep='')

pthr<-c()
pRange<-c(50,100,200)
for(i in pRange){
	pthr<-c(pthr, length(which(p>i)))
}
names(pthr)<-paste(">",pRange, sep='')

#write result to tmp files
write(npeaks,paste(outdir,'stats.tmp',sep=''))
write.table(statsCols,paste(outdir,'stats.tmp',sep=''),sep='\t', col.names=F, append=T)
write.table(t(as.matrix(fethr)),paste(outdir,'feStats.tmp',sep=''), sep="\t",col.names=T)
write.table(t(as.matrix(pthr)),paste(outdir,'pvalStats.tmp',sep=''), sep="\t",col.names=T)