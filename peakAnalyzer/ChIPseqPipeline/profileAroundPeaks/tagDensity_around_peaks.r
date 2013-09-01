distances <- seq(-1000,1000-10,10)+5
nRows <- length(distances)
combinedData <- array(0, c(nRows,3))

input <- as.matrix(read.table("input_tag.aroundPeaks.profile.xls"))
input_average <- apply(input, 2, mean)  / (22732086/1000000) # normalize the total reads to reads per 1M reads
input_average_smoothed <- filter(input_average, rep(1/10,10))
combinedData[,1] <- input_average_smoothed

untreated <- as.matrix(read.table("untreated_tag.aroundPeaks.profile.xls"))
untreated_average <- apply(untreated, 2, mean)  / (37161786/1000000) # normalize the total reads to reads per 1M reads
untreated_average_smoothed <- filter(untreated_average, rep(1/10,10))
combinedData[,2] <- untreated_average_smoothed

treated <- as.matrix(read.table("treated_tag.aroundPeaks.profile.xls"))
treated_average <- apply(treated, 2, mean) / (29769084/1000000) # normalize the total reads to reads per 1M reads
treated_average_smoothed <- filter(treated_average, rep(1/10,10))
combinedData[,3] <- treated_average_smoothed

index <- c(10:(nRows-10))
maxY <- max(combinedData[index,])
maxY

pdf("TagDensity.pdf",height=6,width=6)
plot(distances[index],combinedData[index,1],type="l",col = c(1), lwd=2, main="",xlab="",ylab="", ylim=c(0,max(combinedData[index,])))
lines(distances[index], combinedData[index,2], col=c(3), lwd=2)
lines(distances[index], combinedData[index,3], col=c(2), lwd=2)
legend("topright",c("input", "untreated", "treated"),lty=c(1,1,1),col=c(1,3,2))
dev.off()

