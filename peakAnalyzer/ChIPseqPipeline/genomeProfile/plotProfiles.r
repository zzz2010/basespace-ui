Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
data <- as.matrix(read.table(Args[2], header=TRUE, sep ="\t"))


chroms <- as.matrix(read.table(Args[3]))

nChroms <- length(chroms)
myColors <- rainbow(nChroms)

maxX <- 0
maxY <- 0

for (i in 1:nChroms) {
	indexes <- (data[,2]==chroms[i])
    x <- as.numeric(data[indexes,3])
	y <- as.numeric(data[indexes,5])
	if(maxX < max(x)) {
		maxX <- max(x)
	}
	if(maxY < max(y)) {
		maxY <- max(y)
	}
}

#png("profileGenome.input.png", width = 5, height = 9, units = "in", res=300)
png(paste(Args[2],".unifinedScale.png",sep = ""), width = 8, height = 10, units = "in", res=300)

layout(matrix(c(1:nChroms), nChroms, 1, byrow = TRUE))
for (i in 1:nChroms) {
	indexes <- (data[,2]==chroms[i])
    x <- as.numeric(data[indexes,3])
	y <- as.numeric(data[indexes,5])

	par(mar=c(1,2,1,1))
	## the same scale in y-axis
	plot(x, y, type="h", xaxt="n", bty="n", yaxt="n", xlim=c(1, maxX+1), ylim=c(0,maxY), col=myColors[i])
	title(main=chroms[i])
}
dev.off()

png(paste(Args[2],".differentScale.png",sep = ""), width = 8, height = 10, units = "in", res=300)
layout(matrix(c(1:nChroms), nChroms, 1, byrow = TRUE))
for (i in 1:nChroms) {
	if(i==23 || i==25)
		next	
	indexes <- (data[,2]==chroms[i])
    x <- as.numeric(data[indexes,3])
	y <- as.numeric(data[indexes,5])
	maxY=max(y)
	par(mar=c(1,2,1,1))
	## different scales in y-axis
	plot(x[y>=0.05], y[y>=0.05], type="h", xaxt="n", lwd=2, bty="n", yaxt="n",ylim=c(0,maxY), xlim=c(1, maxX+1), col="red")#myColors[i])
	 lines(x[y<0.05], y[y<0.05], xaxt="n", bty="n", yaxt="n", ylim=c(0,maxY),xlim=c(1, maxX+1), col="black")
	title(main=chroms[i])
}
dev.off()

