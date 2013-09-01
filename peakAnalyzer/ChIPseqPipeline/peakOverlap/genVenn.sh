first=`basename ${1%%.*}`
second=`basename ${2%%.*}`

WorkDir=`dirname "$0"`
outdir=$3

java -cp $WorkDir/../LGL/LGL.jar LGL.overlap.HitConciseOverlap  $1  $2  500  $outdir/$first.peak.annotatedwith.$second.txt
java -cp $WorkDir/../LGL/LGL.jar LGL.overlap.HitConciseOverlap  $2  $1  500  $outdir/$second.peak.annotatedwith.$first.txt

peakIntenFl=$outdir/${first}_${second}.txt
echo -e "$first\t$second" > $peakIntenFl # change this to change labels for the rest of the plots
tr ';,' '\t\t' < $outdir/$first.peak.annotatedwith.$second.txt | awk '{if(NF>4){print $3"\t"$7}else{print $3"\t0"}}' >> $peakIntenFl
grep No <$outdir/$second.peak.annotatedwith.$first.txt | awk '{print 0"\t"$3}' >> $peakIntenFl
## plot Venn
R  $peakIntenFl --vanilla < $WorkDir/plotVenn2C.r



rm $outdir/$second.peak.annotatedwith.$first.txt
rm $outdir/$first.peak.annotatedwith.$second.txt
#rm $peakIntenFl
