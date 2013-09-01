# main
# Grab command line argument. Usage: R --vanilla --args inputfile="inpath" outputfile="outpath" pvaluefile="pvaluepath" < rscript path
# for use in peak-gene association
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

png(outputfile)
inp = scan(inputfile, sep="\t", list(label="",count=0))
label = sapply(inp$label,function(x) gsub("\\s", "\\\n", x)) #make those separated by space double line
ylimit = max(inp$count)*1.1
bp <- barplot(inp$count,names.arg=label,ylim=c(0,ylimit),ylab="number of peaks",cex.names=0.8,col="orange")
text(bp, inp$count + .02 * diff(par("usr")[3:4]), inp$count)
dev.off()

pvalue = chisq.test(inp$count)$p.value
pvalueInfo = paste("p-value =",toString(pvalue))
fileConn = file(pvaluefile)
writeLines(pvalueInfo,fileConn)
close(fileConn)