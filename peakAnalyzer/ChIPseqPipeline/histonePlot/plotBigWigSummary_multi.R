Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
myColors<-rainbow(length(Args)-1)
linetype <- c(1:length(myColors)) 
outdir<-dirname(Args[2])
titlename<-basename(Args[2])
titlename<- unlist(strsplit(titlename,"__"))

nRows<-ncol(as.matrix(read.table(Args[2], header=FALSE, sep ="\t")))
combinedData <- array(0, c(nRows,length(Args)-1))

png(paste(outdir,paste(titlename[1],"_bigwigsummary.png",sep = ""),sep="/"),width = 16, height = 9, units = "in", res=200)
le<-list()
for(i in 2:length(Args))
{
data <- as.matrix(read.table(Args[i], header=FALSE, sep ="\t"))
titlename<-basename(Args[i])
titlename<- unlist(strsplit(titlename,"__"))
le<-c(le,sub(".dat","",titlename[length(titlename)]))
Density<-apply(data,2,mean)

combinedData[,i-1] <- Density/sum(Density)
}

index <- c(10:(nRows-10))
maxy <- max(combinedData[index,])
maxy

binsize=20
Position=binsize*(1:length(Density))-0.5*length(Density)*binsize+0.5*binsize
for(i in 2:length(Args))
{
if(i <=2)
{
plot(Position,combinedData[,i-1],ylim = c(0,maxy),main="",ylab="Density",type="l",lwd=2,col=myColors[i-1],lty=linetype[i-1])
}
lines(Position,combinedData[,i-1],ylim = c(0,maxy),col=myColors[i-1],lwd=2,lty=linetype[i-1])
}
print(unlist(le))
legend("topright",legend=unlist(le),col=myColors , lty = linetype, xjust = 1, yjust = 1)
dev.off()



