Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
myColors<-rainbow(length(Args)-1)
linetype <- c(1:length(myColors)) 
outdir<-dirname(Args[2])
titlename<-basename(Args[2])
titlename<- unlist(strsplit(titlename,"__"))

myColors[2]='blue'
myColors[3]='yellow'
myColors[4]='green'
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
data<-(1+data)/(1+rowSums(data))
Density<-apply(data,2,mean)

combinedData[,i-1] <- Density/sum(Density)
}

index <- c(10:(nRows-10))
maxy <- max(combinedData[index,])
maxy
miny=min(combinedData) #0
binsize=20
Position=binsize*(1:length(Density))-0.5*length(Density)*binsize+0.5*binsize
for(i in 2:length(Args))
{
if(i <=2)
{
plot(Position,combinedData[,i-1],ylim = c(miny,maxy),main="",ylab="Density",type="l",lwd=4,col=myColors[i-1],lty=linetype[i-1],cex=2)
}
lines(Position,combinedData[,i-1],ylim = c(miny,maxy),col=myColors[i-1],lwd=4,lty=linetype[i-1],cex=2)
}
print(unlist(le))
legend("topright",legend=unlist(le),col=myColors , lwd = 4, lty = linetype,cex=2, xjust = 1, yjust = 1)
dev.off()



