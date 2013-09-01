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

#def.par <- par(no.readonly = TRUE)

plotLabel = scan(inputfile, what="char", nlines = 1, sep="\t")
graphLabel = scan(inputfile, what="char", skip=1, nlines=1)
inp = scan(inputfile, skip=2, list(one=0, two=0, three=0, four=0, five=0, six=0, seven=0, eight=0, nine=0, ten=0, eleven=0, twelve=0, thirteen=0))
input = cbind(inp$two,inp$three,inp$four,inp$five,inp$six,inp$seven,inp$eight,inp$nine,inp$ten,inp$eleven,inp$twelve,inp$thirteen)

png(outputfile,width=700,height=480)

layout(matrix(1:2, nrow = 1, byrow = TRUE), width=rep(c(3,1),1))			#To separate the legend from the plot
#layout.show(2)
par(xpd=TRUE, oma=c(0,0,0,2))												#Have a margin on the right side
barplot(t(input),xlab=plotLabel[1],ylab=plotLabel[2],names.arg=inp$one,col=topo.colors(13))
par(mfg=c(1,2))																#move to the right column
legend("center", graphLabel, cex=0.8, fill=topo.colors(13), inset=0.01, title="mismatch from")

dev.off()

#par(def.par)

