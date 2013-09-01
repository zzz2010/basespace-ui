Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
data <- as.matrix(read.table(Args[2], header=TRUE, sep ="\t"))
ma <- function(x,n=5){filter(x,rep(1/n,n))}
nRows=nrow(data)


myColors<-rainbow(nRows)

myColors[1]="black"
myColors[2]="brown"
myColors[3]=654
myColors[4]="darkgreen"
myColors[length(myColors)]="red"
linetype=1:length(myColors)
linetype[1]=9
linetype[2]=1
linetype[9]=1


titlename<-"Peak Distribution Around TSS (transcript direction)"
Position=sub(".","-",sub("X","",colnames(data)),fixed=TRUE)
Position=as.numeric(Position)


for(i in 1: nRows)
{
	data[i,]<-data[i,]/sum(data[i,])
}

ctrl_id=2
le<-rownames(data)


index <- c(10:(nRows-10))
maxy <- max(data)*0.8
maxy

png(paste(Args[2],"_tss.png",sep=""),width = 16, height = 9, units = "in", res=200)
ii=0
for(i in 1:nRows)
{

ii=ii+1
if(i <=1)
{
plot(Position,ma(data[i,],10),ylim = c(0,maxy),main="",ylab="Density",type="l",lwd=3,col=myColors[ii],lty=linetype[ii],cex.lab=1.5)
}else{
nr=5
if(i==5 || i==6)
{
  nr=10
}
lines(Position,ma(data[i,],nr),ylim = c(0,maxy),col=myColors[ii],lwd=3,lty=linetype[ii])
}
}

print(unlist(le))
legend("topright",legend=unlist(le),col=myColors , lty = linetype, xjust = 1, yjust = 1,lwd=3,cex = 1.5)
title(titlename,cex.lab=1.75)
dev.off()


