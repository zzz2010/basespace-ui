peakdata=$1
tagdata=$2
outdir=$3

java -cp ../LGL/LGL.jar LGL.shortReads.ProfileRegion2 $tagdata $peakdata  ./profileConfig_10bp_1Kbins.txt $outdir/tagaround`basename $peakdata`.aroundPeaks



