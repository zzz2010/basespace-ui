# main
# Grab command line argument. Usage: R --vanilla --args inputfile="inpath" refpvalue="nullpvaluefile"  outputfile="outpath" pvaluefile="pvaluepath" < rscript path
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
refPdata<-read.table(refpvalue,row.names=1)
rawcountdata<-read.table(inputfile,row.names=1,sep="\t")
n<-sum(rawcountdata)

n
length(rawcountdata[,1])
pvalues<-array("0",length(rawcountdata[,1]))

for( i in 1:length(rawcountdata[,1]))
{
	name=sub(" ","_",row.names(rawcountdata)[i])
	ratio=refPdata[name,1]
	print(rawcountdata[i,1]/n)
	pvalues[i]=sprintf("pvalue:\n%.5f",1-pbinom(rawcountdata[i,1]-0.1,n,ratio))
}

pvalues

png(outputfile)
inp = scan(inputfile, sep="\t", list(label="",count=0))
label = sapply(inp$label,function(x) gsub("\\s", "\\\n", x)) #make those separated by space double line
ylimit = max(inp$count)*1.1
bp <- barplot(inp$count,names.arg=label,ylim=c(0,ylimit),ylab="number of peaks",cex.names=0.8,col=rainbow(6))
text(bp, inp$count + .02 * diff(par("usr")[3:4]), inp$count)
text(bp, ylimit/2 + .08 * diff(par("usr")[3:4]), pvalues)
dev.off()

pvalue = chisq.test(inp$count)$p.value
pvalueInfo = paste("p-value =",toString(pvalue))
fileConn = file(pvaluefile)
writeLines(pvalueInfo,fileConn)
close(fileConn)
