Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
myColors<-rainbow(length(Args)-1)
titlename<-basename(Args[2])
titlename<- unlist(strsplit(titlename,"_"))
png(paste(titlename[1],"_bigwigsummary.png",sep = ""),width = 12, height = 9, units = "in", res=400)
ma <- function(x,n=5){filter(x,rep(1/n,n), sides=2)}
le<-list()
par(cex=2)
for(i in 2:length(Args))
{
data <- as.matrix(read.table(Args[i], header=FALSE, sep ="\t"))
titlename<-basename(Args[i])
titlename<- unlist(strsplit(titlename,"_"))
le<-c(le,sub(".dat","",titlename[1]))

colsum<-colSums(data[,1:200])
print(colsum)
Density<-colsum/sum(colsum)
Density<-ma(Density,10)
binsize=10
Position=binsize*(1:length(Density))-0.5*length(Density)*binsize+0.5*binsize
if(i <=2)
{
plot(Position,Density,ylim = c(0,0.03),main="",type="l",lwd=4)
}
lines(Position,Density,ylim = c(0,0.03),col=myColors[i-1],lwd=4)
}
print(unlist(le))
legend("topright",legend=unlist(le),col=myColors , lty = 1, xjust = 1, yjust = 1,cex=0.75)
dev.off()



