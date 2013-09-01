Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
data <- as.matrix(read.table(Args[2], header=FALSE, sep ="\t"))

Density<-apply(data,2,mean)
Density
png(paste(Args[2],".cons.png",sep = ""))
binsize=as.numeric(Args[3])
Position=binsize*(1:length(Density))-0.5*length(Density)*binsize+0.5*binsize
par(cex=1.2)
plot(Position,Density,main="Average phastCons around the center of peaks",type="l", ylab="PhastCons Score",lwd=4 )
dev.off()

