# main
# Grab command line argument. Usage: R --vanilla --args inputfile="inpath" outputfile="outpath" logoutputfile="logoutpath" title="title"< rscript path
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

x <- as.matrix(read.table(inputfile))
hist_x <- hist(x,breaks=c(seq(0,10000,100),2000000), plot=FALSE, right = FALSE) 

png(logoutputfile)
logtitle = paste("log view of",title,sep=" ")
plot(hist_x$breaks[1:100]+1, pmax(hist_x$counts[1:100],1), log="xy", xlim=c(1,10000), xlab="peak distance", ylab="frequency of peak distance", main=logtitle)
dev.off()

png(outputfile)
plot(hist_x$breaks[1:100], hist_x$counts[1:100], xlim=c(0,10000), xlab="peak distance", ylab="frequency of peak distance", main=title)
dev.off()