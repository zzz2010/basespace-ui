Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]

nFiles=(length(Args)-1)/2

ctrl_id=3

myColors<-rainbow(nFiles-1)
myColors[1]="black"
myColors[2]="blue"
myColors[length(myColors)]="red"
linetype=1:length(myColors)
linetype[1]=9
linetype[9]=1

myColors[1]="black"
myColors[2]="brown"
myColors[3]=654
myColors[4]="darkgreen"
myColors[length(myColors)]="red"
linetype=1:length(myColors)
linetype[1]=9
linetype[2]=1
linetype[9]=1


titlename<-basename(Args[2])
titlename<- unlist(strsplit(titlename,"_around_"))
png(paste(dirname(Args[2]),paste(titlename[2],"_tagmulti.png",sep = ""),sep="/"),width = 12, height = 9, units = "in", res=400)
ma <- function(x,n=5){filter(x,rep(1/n,n))}
le<-list()
par(cex=2)
Args[2]
nRows<-ncol(as.matrix(read.table(Args[2], header=FALSE, sep ="\t",strip.white = TRUE)))
combinedData <- array(0, c(nRows,nFiles))


#change ctrl_fl to the last one
ctrlFl=Args[ctrl_id]
for(i in 2:(nFiles+1))
{
if(i>ctrl_id)
{
	Args[i-1]=Args[i]
}
}
Args[nFiles+1]=ctrlFl
for(i in 2:(nFiles+1))
{
data <- as.matrix(read.table(Args[i], header=FALSE, sep ="\t",strip.white = TRUE))
titlename<-basename(Args[i])
titlename<- unlist(strsplit(titlename,"_around_"))
if(i<nFiles+1)
{
le<-c(le,sub(".bed","",titlename[1]))
}
input_average <- apply(data, 2, sum)/as.numeric(Args[nFiles+i])
Density<-ma(input_average,5)
combinedData[,i-1] <- Density
}
for(i in 1:nFiles-1)
{
    for(j in 1:length(combinedData[,i]))
    {
    	combinedData[j,i]<-combinedData[j,i]/combinedData[j,nFiles]
    }
}


index <- c(10:(nRows-10))
maxy <- log( max(combinedData[index,-nFiles]))
miny<- log( min(combinedData[index,-nFiles]))
maxy
for(i in 2:(nFiles))
{
binsize=10

Position=binsize*(1:length(Density))-0.5*length(Density)*binsize+0.5*binsize
if(i <=2)
{

plot(Position,log(combinedData[,i-1]),ylim = c(miny,maxy),main="",ylab="Log ChIP Enrichment",type="l",lwd=3,lty=linetype[i-1])
}
else
{
lines(Position,log(combinedData[,i-1]),ylim = c(miny,maxy),col=myColors[i-1],lwd=3,lty=linetype[i-1])
}

}
print(unlist(le))
legend("topleft",legend=unlist(le),col=myColors , lwd=3, lty=linetype, xjust = 1, yjust = 1,cex=0.4)
dev.off()



