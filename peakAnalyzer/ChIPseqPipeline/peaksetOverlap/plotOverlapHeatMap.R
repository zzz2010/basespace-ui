Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
overlapMatrix <- as.matrix(read.table(Args[2], header=TRUE, row.names=1))
peakcount<- as.matrix(read.table(Args[3], header=FALSE, row.names=1))

nLib=ncol(overlapMatrix)

for(i in 1:nLib)
{
	p1count=peakcount[i,1]
	for(j in i:nLib)
	{
		p2count=peakcount[j,1]
		o1=overlapMatrix[i,j]
		o2=overlapMatrix[j,i]
		overlaprate=min(o1,o2)/min(p1count,p2count)
		overlapMatrix[i,j]=overlaprate
		overlapMatrix[j,i]=overlaprate
	}

}
max(overlapMatrix)
library(gplots)
png(paste(Args[2],"_heatmap.png",sep = ""),width = 9, height = 9, units = "in", res=400)
heatmap.2(overlapMatrix, symm = TRUE,scale='none',trace="none",margins = c(10, 10))
dev.off()
