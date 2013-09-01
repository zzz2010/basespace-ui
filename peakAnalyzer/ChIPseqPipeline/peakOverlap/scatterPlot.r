# main
# Grab command line argument. Usage: R --vanilla --args inputfile="inpath" outputfile="outpath" < rscript path
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

library(utils)
data <- as.matrix(read.table(inputfile, header=TRUE))
label = scan(inputfile, nlines = 1, list(first="", second=""))
png(outputfile)
xlabel = paste(label[1],'peak intensity',sep=' ')
ylabel = paste(label[2],'peak intensity',sep=' ')
plot(data[,1], data[,2], xlab=xlabel, ylab=ylabel)
#correlation = cor(data,method="pearson") #print correlation
#print(correlation)
#write(print(correlation), file="correlation coefficient.txt", ncol=2)
#write.table(cbind(rownames(correlation), correlation), "Pearson-correlation-coefficient.txt", row.names=FALSE)
commonData <- data[(data[,1]>0)&(data[,2]>0),]
x <- commonData[,1]
y <- commonData[,2]
lm1 <- lm(y ~ x)
z = predict(lm(y ~ x))
lines(z~x,lwd=2,col="red")
r = sprintf("r=%.3f", cor(x,y))
x_coor = (max(x)-min(x))*2/3 + min(x)
y_coor = (max(y)-min(y))/3 + min(y)
text(x_coor,y_coor,r,cex=2)
y_coor2 = (max(y)-min(y))/3 - min(y)
nlabel = paste(label[1],'n',label[2],sep=' ')
text(x_coor,y_coor2,nlabel,cex=1) 

dev.off()
