rm -rf ./test/output
mkdir ./test/output
sh ./peakAnnotation.UCSC.sh ./test/ctcfpeak_ixn.bed hg19 ./test/output/
wc -l ./test/output/*.txt


#R --vanilla --args inputfile=./test/output//ctcfpeak_ixn.bed.summary outputfile=./test/output//ctcfpeak_ixn.bed.summary.png pvaluefile=./test/output//ctcfpeak_ixn.bed.summary.pvalue refpvalue=/home/genomebrowser/ChIPseqPipeline/peakAnnotation/pvalue/hg19.genomeRegion.txt < /home/genomebrowser/ChIPseqPipeline/peakAnnotation/peakDist.r
