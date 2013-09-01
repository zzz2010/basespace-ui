Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
data <- as.matrix(read.table(Args[2], header=TRUE, sep ="\t"))
ma <- function(x,n=5){filter(x,rep(1/n,n))}
nRows=nrow(data)
myColors<-rainbow(nRows)
myColors[length(myColors)]='black'
linetype <- c(1:length(myColors))
titlename<-"Peak Distribution Around TSS (transcript direction)"
le<-rownames(data)
Position=sub(".","-",sub("X","",colnames(data)),fixed=TRUE)
Position=as.numeric(Position)
for(i in 1: nRows)
{
	data[i,]<-data[i,]/sum(data[i,])
}
index <- c(10:(nRows-10))
maxy <- max(data)*0.8
maxy

png(paste(Args[2],"_tss.png",sep=""),width = 16, height = 9, units="in", res=200)

for(i in 1:nRows)
{
if(i <=1)
{
plot(Position,ma(data[i,]),ylim = c(0,maxy),main="",ylab="Density",type="l",lwd=3,col=myColors[i],lty=linetype[i],cex.lab=1.5)
}else{
lines(Position,ma(data[i,]),ylim = c(0,maxy),col=myColors[i],lwd=3,lty=linetype[i])
}
}

print(unlist(le))
legend("topright",legend=unlist(le),col=myColors , lty = linetype, xjust = 1, yjust = 1,lwd=3,cex = 1.5)
title(titlename,cex.lab=1.75)
dev.off()


