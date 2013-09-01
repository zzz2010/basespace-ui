Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
data <- as.matrix(read.table(Args[2], header=TRUE, sep ="\t"))

nRows=nrow(data)
nCols=ncol(data)
myColors<-rainbow(nRows)
linetype <- c(1:length(myColors))
titlename<-"Other Peaks against Peak Score Distribution"
le<-rownames(data)
Position=sub("X","",colnames(data))
Position=as.numeric(Position)
selrow<-rep(0,nRows)
ncol2<-nCols/2
for(i in 1: nRows)
{
x=sum(data[i,1:ncol2])
n=sum(data[i,])
pvalue=prop.test(x,n)$p.value
if(pvalue<0.05)
{
	selrow[i]<-i
}
}
print(le[selrow])
maxy <- max(data)
maxy
csum<-colSums(data[selrow,])
print(nrow(data[selrow,]))
rsum<-rowSums(data)
noiselevel<-as.numeric(Args[3]) #nRows*min(rsum)/length(csum)
noiselevel2<-noiselevel-(sum(rsum)-sum(csum))/nCols
minPval=0.5
minIndex=0
maxFC=1
minFDR=0
confidence=1-0.05/length(csum)
noiselevel2
for(i in 1:(length(csum)-1))
{
x=sum(csum[1:i])
n=sum(csum)
p=i/length(csum)
FC=(n-x)*p/(x*(1-p))
FDR=noiselevel2/x
print(FDR)
pvalue=prop.test(x,n,p=p,alternative="less",conf.level=confidence)$conf.int[2]
if(FDR >0.5)
{
  maxFC=FC
  minFDR=FDR
  minIndex=i
  minPval=pvalue
}
}
png(paste(Args[2],"_peakcorr.png",sep=""),width = 1600, height = 1200,  res=200)
mat<-matrix(1:2,nrow=1)
#layout(mat,widths = rep(c(4,1),1))
#par(xpd=TRUE,oma=c(0,0,0,0),mar=c(4,4,2,0))
for(i in 1:nRows)
{
data[i,]<-cumsum(rev(data[i,]))
}
maxy <- max(data)

for(i in 1:nRows)
{
if(i <=1)
{
plot(Position,data[i,],ylim = c(0,maxy),main="",xlab="Peak Rank",ylab="Overlap Count",type="l",lwd=2,col=myColors[i],lty=linetype[i])
}
lines(Position,data[i,],ylim = c(0,maxy),col=myColors[i],lwd=2,lty=linetype[i])
}
if(minIndex>0)
{
yy=0:maxy
points(rep(Position[minIndex],length(yy)), yy, type="l",lty=2, col="black")
text(Position[minIndex],y=yy[length(yy)/2],labels=paste("x=",Position[minIndex]))
}
points(Position,rep(noiselevel/nRows,length(Position)), type="l",lty=2, col="black")
text(Position[length(Position)/2],y=noiselevel/nRows,labels=paste("noiselevel=",noiselevel))

legend("topleft",legend=unlist(le),horiz=F,col=myColors , lty = linetype, xjust = 1, yjust = 1)
title(titlename)
Args[2]
minPval
minFDR
maxFC
noiselevel
print(unlist(le))
#par(mfg=c(1,2))
#par(oma=c(0,0,0,0),mar=c(0,0,0,0))
dev.off()


