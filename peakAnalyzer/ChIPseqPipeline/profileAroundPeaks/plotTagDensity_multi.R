Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]

nFiles=(length(Args)-1)/2
myColors<-rainbow((length(Args)-1)/2)
myColors[1]="black"
myColors[2]="blue"
myColors[length(myColors)]="red"

titlename<-basename(Args[2])
titlename<- unlist(strsplit(titlename,"_around_"))
png(paste(dirname(Args[2]),paste(titlename[2],"_tagmulti.png",sep = ""),sep="/"),width = 12, height = 9, units = "in", res=400)
ma <- function(x,n=5){filter(x,rep(1/n,n))}
le<-list()
par(cex=2)
nRows<-ncol(as.matrix(read.table(Args[2], header=FALSE, sep ="\t")))
combinedData <- array(0, c(nRows,nFiles))

for(i in 2:(nFiles+1))
{
data <- as.matrix(read.table(Args[i], header=FALSE, sep ="\t"))
titlename<-basename(Args[i])
titlename<- unlist(strsplit(titlename,"_around_"))
le<-c(le,sub(".tags.unique","",titlename[1]))
input_average <- apply(data, 2, mean)/as.numeric(Args[nFiles+i])

Density<-ma(input_average,10)
combinedData[,i-1] <- Density
}

index <- c(10:(nRows-10))
maxy <- max(combinedData[index,])
maxy
for(i in 2:(nFiles+1))
{
binsize=10
Position=binsize*(1:length(Density))-0.5*length(Density)*binsize+0.5*binsize
if(i <=2)
{

plot(Position,combinedData[,i-1],ylim = c(0,maxy),main="",ylab="Density",type="l",lwd=4)
}
lines(Position,combinedData[,i-1],ylim = c(0,maxy),col=myColors[i-1],lwd=4)
}
print(unlist(le))
legend("topright",legend=unlist(le),col=myColors , lty = 1, xjust = 1, yjust = 1,cex=0.75)
dev.off()



