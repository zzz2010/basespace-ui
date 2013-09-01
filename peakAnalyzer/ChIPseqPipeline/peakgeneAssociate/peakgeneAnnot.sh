#$1 is bed output .peak format
genome=$2
outdir=$3
win=20000
WorkDir=`dirname "$0"`
x=`basename $1`
prefix=$outdir/$x
peakfile=$prefix.tmp

cut -f1,2,3 $1 > $peakfile
genefile="${WorkDir}/gene/${genome}gene.bed"
cut -f1,2,3 $genefile |windowBed -w $win -a $peakfile -b stdin > $peakfile.$win.tmp
cut -f1,2,3 $genefile|closestBed -a $peakfile -b stdin -t first -d > $peakfile.close.tmp

python ${WorkDir}/multijoin.py -a 1,2,3 -b 1,2,3 $peakfile.$win.tmp $1 > $peakfile.$win.tmp1
python ${WorkDir}/multijoin.py -a 4,5,6 -b 1,2,3  $peakfile.$win.tmp1 $genefile > $peakfile.$win.tmp2


#exons region
closestBed -a $peakfile.$win.tmp2 -b ${WorkDir}/gene/UCSC_${genome}_exons* -d -t first > $peakfile.$win.tmp3
awk '{OFS="\t";if($NF==0){print "1"}else{print "0"}}' $peakfile.$win.tmp3 > $peakfile.$win.tmp4

paste $peakfile.$win.tmp2 $peakfile.$win.tmp4 > $peakfile.$win.tmp5



echo "peak	summit	summit+1	start	end	tagcount	(CCAT)ctrltag/(MACS)logpvalue	FC	FDR	Gene	left	right	strand	Name	Id" > $prefix.$win.gene
cut -f 7- $peakfile.$win.tmp5  |sort -k 7 |uniq >> $prefix.$win.gene

python ${WorkDir}/postprocess.py $prefix.$win.gene > $prefix.$win.gene.tsv

perl ${WorkDir}/tsv2html.pl $prefix.$win.gene.tsv >$prefix.$win.gene.tsv.html

paste $peakfile.close.tmp $1 > $peakfile.close.tmp1
python ${WorkDir}/multijoin.py -a 4,5,6 -b 1,2,3  $peakfile.close.tmp1 $genefile |sort -u -k1,2 > $peakfile.close.tmp2

#exons region
closestBed -a $peakfile.close.tmp2 -b ${WorkDir}/gene/UCSC_${genome}_exons* -d -t first > $peakfile.close.tmp3
awk '{OFS="\t";if($NF==0){print "1"}else{print "0"}}' $peakfile.close.tmp3 > $peakfile.close.tmp4

paste $peakfile.close.tmp2 $peakfile.close.tmp4 > $peakfile.close.tmp5

echo "peak	summit	summit+1	start	end	tagcount	(CCAT)ctrltag/(MACS)logpvalue	FC	FDR	Gene	left	right	strand	Name	Id	is_exon" > $prefix.close.gene
cut -f 8- $peakfile.close.tmp5 |sort -k 7 |uniq >> $prefix.close.gene

python ${WorkDir}/postprocess.py  $prefix.close.gene > $prefix.close.gene.tsv

perl ${WorkDir}/tsv2html.pl $prefix.close.gene.tsv > $prefix.close.gene.tsv.html

rm $prefix*.tmp*
   
