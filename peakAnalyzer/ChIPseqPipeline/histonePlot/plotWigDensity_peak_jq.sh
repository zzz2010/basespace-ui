peakfile=$1
bigwigfile=$2

datapoints=25

WorkDir=`dirname "$0"`

awk '{ w=2500;m=($2+$3)/2;a=m-w;b=m+w;if(a<0){a=0;} printf("%s\t%ld\t%ld\n", $1,a,b)}' $peakfile | $WorkDir/bigWigSummaryBatch $bigwigfile stdin  $datapoints  

