data <- c(as.matrix(read.table("sampleData.txt")))
ratio <- c(as.numeric(as.matrix(read.table("hg19.genomeRegion.txt"))[,2]))
ratio <- ratio /sum(ratio)
#chisq.test(data, p=ratio)$p.value

n<-sum(data)
pvalues<-array(0,length(ratio))
for (i in 1:length(ratio))
{
pvalues[i]=pbinom(data[i],n,ratio[i])
}

