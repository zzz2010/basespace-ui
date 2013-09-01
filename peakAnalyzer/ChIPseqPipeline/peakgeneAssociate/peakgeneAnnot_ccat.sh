#$1 is bed output .peak format
genome=$2
outdir=$3
win=20000
WorkDir=`dirname "$0"`
x=`basename $1`
prefix=$outdir/$x
peakfile=$prefix.tmp

cut -f1,3,4 $1 > $peakfile
genefile="${WorkDir}/gene/${genome}gene.bed"
cut -f1,2,3 $genefile |windowBed -w $win -a $peakfile -b stdin > $peakfile.$win.tmp
cut -f1,2,3 $genefile|closestBed -a $peakfile -b stdin -t first -d > $peakfile.close.tmp

python multijoin.py -a 1,2,3 -b 1,3,4 $peakfile.$win.tmp $1 > $peakfile.$win.tmp1
python multijoin.py -a 4,5,6 -b 1,2,3  $peakfile.$win.tmp1 $genefile > $peakfile.$win.tmp2
cut -f 8- $peakfile.$win.tmp2  |sort -k 7 |uniq > $prefix.$win.gene



paste $peakfile.close.tmp $1 > $peakfile.close.tmp1
python multijoin.py -a 4,5,6 -b 1,2,3  $peakfile.close.tmp1 $genefile > $peakfile.close.tmp2
cut -f 9- $peakfile.close.tmp2 |sort -k 7 |uniq > $prefix.close.gene


rm $prefix*.tmp*
   
