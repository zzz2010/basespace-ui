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

outdir2=$outdir/plus
mkdir $outdir2
peakIntenFl2=$outdir2/${first}__${second}.txt
python $WorkDir/vennTagcount_hist.py $1 $2 $peakIntenFl > $peakIntenFl2  

R  $peakIntenFl2 --vanilla < $WorkDir/plotPeakCorr.r

peakIntenFl3=$outdir2/${first}__${second}.scatter
echo -e "$first\t$second" > $peakIntenFl3
sh $WorkDir/scatter.sh $1 $2 6 200 >> $peakIntenFl3
R  --vanilla --args inputfile="$peakIntenFl3" outputfile="${peakIntenFl3}.png" < $WorkDir/scatterPlot.r

#rm $outdir/$second.peak.annotatedwith.$first.txt
#rm $outdir/$first.peak.annotatedwith.$second.txt
#rm $peakIntenFl
