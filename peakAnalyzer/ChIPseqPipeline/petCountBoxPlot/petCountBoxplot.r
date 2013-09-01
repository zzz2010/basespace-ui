commandArgs()

for (e in commandArgs()) {
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

library(UsingR)

inter <- as.matrix(read.table(interFile))
noInter <- as.matrix(read.table(noInterFile))
fileName <- sprintf("boxplot.%s.png", outputPrefix);
png(fileName)
boxplot(list(noInter=noInter, inter=inter), notch=TRUE,col="brown")
dev.off()

x <- c(inter,noInter)
q92 <- quantile(x, 0.92)


fileName <- sprintf("boxplot.%s.fineScale.png", outputPrefix);
png(fileName)
boxplot(list(noInter=noInter, inter=inter), notch=TRUE,col="brown", ylim=c(0,q92))
dev.off()

#fileName <- sprintf("violinplot.%s.fineScale.png", outputPrefix);
#png(fileName)
#simple.violinplot(list(noInter=noInter, inter=inter), notch=TRUE,col="brown", ylim=c(0,q92))
#dev.off()


