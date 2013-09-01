Args<-commandArgs()[grep("^--",commandArgs(),invert=T)]
data <- as.matrix(read.table(Args[2], header=FALSE, sep ="\t"))

colsum<-colSums(data)
png(paste(Args[2],".density.png",sep = ""))
plot(1:length(colsum),colsum,main=Args[2],type="l")
dev.off()

