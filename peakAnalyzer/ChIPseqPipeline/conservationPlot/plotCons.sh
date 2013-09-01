peakfile=$1
phastDir=$2
outdir=$3

WorkDir=`dirname "$0"`
bedfile1=$outdir/bed4000bp
bedfile2=$outdir/bed400bp

$WorkDir/../ZZZ/centerBed $peakfile|awk '{OFS="\t"; if($2>2000){print $1,$2-2000,$3+2000}}' > $bedfile1
$WorkDir/../ZZZ/centerBed $peakfile|awk '{OFS="\t"; if($2>200){print $1,$2-200,$3+200}}' > $bedfile2


outprefix1=$outdir/`basename $bedfile1`
cut -f1  $peakfile|sort -u | xargs -n 1 sh -c ' grep "$3" "$1" > "$2"."$3" ' move  $bedfile1 $outprefix1 

outprefix2=$outdir/`basename $bedfile2`
cut -f1  $peakfile|sort -u | xargs -n 1 sh -c ' grep "$3" "$1" > "$2"."$3" ' move  $bedfile2 $outprefix2

outprefix=$outdir/`basename $peakfile`

rm $outprefix.*.cons.txt

for chrfl in $outprefix1.chr*
do
	chrom=${chrfl##$outprefix1.}
	$WorkDir/./bigWigSummaryBatch $phastDir/$chrom.phastCons*.bigWig $chrfl 40 |sed '/.\{40,\}/!d' >> $outprefix.4000.cons.txt

done

R $outprefix.4000.cons.txt 100 --no-save < $WorkDir/plotDensity.r

for chrfl in $outprefix2.chr*
do
        chrom=${chrfl##$outprefix2.}
        $WorkDir/./bigWigSummaryBatch $phastDir/$chrom.phastCons*.bigWig $chrfl 40 |sed '/.\{40,\}/!d' >> $outprefix.400.cons.txt

done

R $outprefix.400.cons.txt 10 --no-save < $WorkDir/plotDensity.r

#python ./getphastcon.py $outprefix $phastDir $outdir 4000 40

#python ./getphastcon.py $outprefix $phastDir $outdir 400 40


rm $outprefix1.chr*

rm $outprefix2.chr*
