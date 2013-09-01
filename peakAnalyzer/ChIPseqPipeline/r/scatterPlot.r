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
png(outputfile, res=85)
xlabel = paste(label[1],'peak intensity',sep=' ')
ylabel = paste(label[2],'peak intensity',sep=' ')
nlabel = paste(label[1],'n',label[2],sep=' ')

layout(matrix(1:2, nrow = 1, byrow = TRUE), width=rep(c(3,1),1))			#To separate the legend from the plot
par(xpd=TRUE, oma=c(0,0,0,2))												#Have a margin on the right side

plot(data[,1], data[,2], xlab=xlabel, ylab=ylabel)
mtext(nlabel)
commonData <- data[(data[,1]>0)&(data[,2]>0),]
x <- commonData[,1]
y <- commonData[,2]
lm1 <- lm(y ~ x)
z = predict(lm(y ~ x))
lines(z~x,lwd=2,col="red")

par(mfg=c(1,2))																#move to the right column

r = sprintf("r=%.3f", cor(x,y))
#x_coor = (max(x)-min(x))*2/3 + min(x)
#z_coor = (max(z)-min(z))*2/3 + min(z)
#z_coor1 = z_coor - 25/100*z_coor
#text(x_coor,z_coor1,r,cex=0.5,col="red")
#z_coor2 = z_coor - 40/100*z_coor
#nlabel = paste(label[1],'n',label[2],sep=' ')
#text(x_coor,z_coor2,nlabel,cex=0.5,col="red") 

figDimension = par("usr")
x_coor1 = (figDimension[2] - figDimension[1])/2 + figDimension[1]
y_coor1 = (figDimension[4] - figDimension[3])/2 + figDimension[3]
text(x_coor1,y_coor1,r,cex=2.0,col="red")
x_coor2 = 0.2*(figDimension[2] - figDimension[1]) + figDimension[1]
y_coor2 = 0.4*(figDimension[4] - figDimension[3]) + figDimension[3]
#text(x_coor2,y_coor2,nlabel,cex=0.6,col="red") 

dev.off()
