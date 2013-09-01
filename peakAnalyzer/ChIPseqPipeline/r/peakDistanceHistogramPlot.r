# main
# Grab command line argument. Usage: R --vanilla --args inputfile="inpath" outputfile="outpath" limit="value1" bin="value2" title="title"< rscript path
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
limitnum = as.integer(limit)
x <- x[x>-limitnum & x<limitnum]
binnum = as.integer(bin)
titlerange = paste(limit,"bp range",title,sep=" ")
png(outputfile)
hist(x,breaks=seq(-limitnum,limitnum, binnum), xlab="Distance between peaks", ylab="Frequency of peak distance", main=titlerange)
dev.off()
