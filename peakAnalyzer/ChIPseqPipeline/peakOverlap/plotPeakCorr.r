Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
myColors<-rainbow(4)
combinedData<-as.matrix(read.table(Args[2], header=FALSE, sep ="\t"))
linetype <- c(1:length(myColors))
titlename<-basename(Args[2])
titlename<- unlist(strsplit(titlename,"__"))
titlename[2]<-sub(".txt","",titlename[2])
png(paste(Args[2],".png",sep = ""),width = 12, height = 9, units = "in", res=100)
le<-c(paste(titlename[1],"unique"),paste(titlename[1],"peak_intersect"),paste(titlename[2],"peak_intersect"),paste(titlename[2],"unique"))

maxy <- max(combinedData)
binsize=100/length(combinedData[1,])
Position=binsize*(1:length(combinedData[1,]))+0.5*binsize
for(i in 1:4)
{
if(i <=1)
{
plot(Position,combinedData[i,],ylim = c(0,maxy),main="",ylab="Mean Tag Count",xlab="Quantile",type="l",lwd=2,col=myColors[i],lty=linetype[i])
}
lines(Position,combinedData[i,],ylim = c(0,maxy),col=myColors[i],lwd=2,lty=linetype[i])
}
print(unlist(le))
legend("topright",legend=unlist(le),col=myColors , lty = linetype, xjust = 1, yjust = 1)
dev.off()

