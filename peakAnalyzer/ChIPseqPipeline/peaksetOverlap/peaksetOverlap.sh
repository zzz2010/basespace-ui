peaksetPattern=$1
outdir=$2
WorkDir=`dirname "$0"`

python $WorkDir/PeaksetCount.py "$peaksetPattern" > $outdir/peakcount.txt
python $WorkDir/overlapPeakset.py "$peaksetPattern" > $outdir/peakset_overlap.txt
#python $WorkDir/overlapPeakset_plus.py "$peaksetPattern" 5  $outdir
R $outdir/peakset_overlap.txt $outdir/peakcount.txt --no-save < $WorkDir/plotOverlapHeatMap.R


