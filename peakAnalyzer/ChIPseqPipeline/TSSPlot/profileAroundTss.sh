peakdata=$1
tagdata=$2
outdir=$3

java -cp ../LGL/LGL.jar LGL.shortReads.ProfileRegion2 $tagdata $peakdata  profile_10bp_500bins.txt  $outdir/tagaround`basename $peakdata`.aroundPeaks



