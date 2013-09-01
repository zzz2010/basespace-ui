peakfile=$1
phastDir=$2
outdir=$3

WorkDir=`dirname "$0"`

#make background bed
awk 'BEGIN{OFS="\t"}{for(i=1;i<=10;i++){offset=1000-int(2000*rand());print $1,$2+offset,$3+offset}}' $peakfile > $outdir/bg.bed



outprefix1=$outdir/site.bed
cut -f1  $peakfile|sort -u | xargs -n 1 sh -c ' grep -w "$3" "$1" > "$2"."$3" ' move  $peakfile $outprefix1 

outprefix2=$outdir/bg.bed
cut -f1  $peakfile|sort -u | xargs -n 1 sh -c ' grep -w "$3" "$1" > "$2"."$3" ' move  $outdir/bg.bed $outprefix2

outprefix=$outdir/`basename $peakfile`

rm $outprefix.*.cons.txt

for chrfl in $outprefix1.chr*
do
	chrom=${chrfl##$outprefix1.}
	$WorkDir/./bigWigSummaryBatch $phastDir/$chrom.phastCons*.bigWig $chrfl 1  >> $outprefix1.cons.txt

done

for chrfl in $outprefix2.chr*
do
        chrom=${chrfl##$outprefix2.}
	        $WorkDir/./bigWigSummaryBatch $phastDir/$chrom.phastCons*.bigWig $chrfl 1  >> $outprefix2.cons.txt

done

paste $peakfile  $outprefix1.cons.txt >   $outprefix1.combined

python computePvalue.py $outprefix1.combined $outprefix2.cons.txt > $outprefix1.combined.pvalue 

awk '{if($NF<0.05){print $0}}' $outprefix1.combined.pvalue > $outprefix1.combined.pvalue.filtered

tail $outprefix1.combined.pvalue

rm $outprefix1.chr*

rm $outprefix2.chr*
