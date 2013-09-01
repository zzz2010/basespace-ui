# main
# Grab command line argument. Usage: R --vanilla --args commonPeakIntensities="commonPath" uniquePeakIntensities="uniquePath" firstLegend="legend1" secondLegend="legend2" beanPlotFile="outpath" < rscript path
for (e in commandArgs(trailingOnly=TRUE)) {
  ta = strsplit(e,"=",fixed=TRUE)
  if(! is.na(ta[[1]][2])) {
    temp = ta[[1]][2]
    if(substr(ta[[1]][1],nchar(ta[[1]][1]),nchar(ta[[1]][1])) == "I") {
      temp = as.integer(temp)
    }
    if(substr(ta[[1]][1],nchar(ta[[1]][1]),nchar(ta[[1]][1])) == "N") {
      temp = as.numeric(temp)
    }
    assign(ta[[1]][1],temp)
    cat("assigned ",ta[[1]][1]," the value of |",temp,"|\n")
  } else {
    assign(ta[[1]][1],TRUE)
    cat("assigned ",ta[[1]][1]," the value of TRUE\n")
  }
}

x <- as.matrix(read.table(commonPeakIntensities))
y <- as.matrix(read.table(uniquePeakIntensities))
library(beanplot)
png(beanPlotFile)

q1 <- quantile(x)
q2 <- quantile(y)
maxY <- max(q1[4]+(q1[4]-q1[2])*3, q2[4]+(q2[4]-q2[2])*3)
maxY <- min(maxY, max(q1[5], q2[5]))
minY <- min(q1[2]-(q1[4]-q1[2])*3, q2[2]-(q2[4]-q2[2])*3)
minY <- max(minY, min(q1[1], q2[1]))
x_filtered <- x[(x>minY)&(x<maxY)]
y_filtered <- y[(y>minY)&(y<maxY)]

beanplot(x_filtered,y_filtered,log="",ylim = c(minY,maxY),names=c("common","unique"),col="orange")
graphTitle = paste(firstLegend,"wrt",secondLegend,sep=" ")
title(main=graphTitle,ylab="peak intensity")
dev.off()
