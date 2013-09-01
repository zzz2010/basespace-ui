#$1 is CCAT output .peak format
peakfile=$1.tmp
win=20000
cut -f1,2,3 $1 > $peakfile
genefile="./hg19gene.bed"
windowBed -w $win -a $peakfile -b $genefile > $peakfile.$win.tmp
closestBed -a $peakfile -b $genefile -t first -d > $peakfile.close.tmp

python multijoin.py -a 1,2,3 -b 1,3,4 $peakfile.$win.tmp $1 > $peakfile.$win.tmp1
python multijoin.py -a 4,5,6 -b 1,2,3  $peakfile.$win.tmp1 $genefile.sorted > $peakfile.$win.tmp2
cut -f 8- $peakfile.$win.tmp2  |sort -k 7 |uniq > $1.$win.gene



paste $peakfile.close.tmp $1 > $peakfile.close.tmp1
python multijoin.py -a 4,5,6 -b 1,2,3  $peakfile.close.tmp1 $genefile.sorted > $peakfile.close.tmp2
cut -f 9- $peakfile.close.tmp2 |sort -k 7 |uniq > $1.close.gene



   
