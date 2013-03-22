Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
outdir<-Args[2]
unmap<-as.numeric(Args[3])
multimap<-as.numeric(Args[4])
uniq<-as.numeric(Args[5])

png(paste(outdir,"reads_distribution.png",sep=""), width=600)
slices<-c(unmap,uniq, multimap)
lab<-c("Non-Mapped", "Unique","Multi-Map")
pct <- round(slices/sum(slices)*100, digits=2)
lab<-paste(lab,pct)
lab <- paste(lab,"%",sep="")
pie(slices,labels=lab,main="Distribution of Reads")

dev.off()
