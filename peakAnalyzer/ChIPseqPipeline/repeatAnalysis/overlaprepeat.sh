peakbed=$1
genome=$2
outdir=$3
WorkDir=`dirname "$0"`
name=`basename $peakbed`
prefix=${outdir}/${name}
rsmkfl=$WorkDir/rsmk/${genome}rsmk.bed
windowBed -w 1 -a $peakbed -b $rsmkfl >  $prefix.rsmk.bed 

awk '{print $NF}' $prefix.rsmk.bed |sort |uniq -c  > ${prefix}_repeatdist.txt

R --vanilla --args inputfile="${prefix}_repeatdist.txt" refpvalue="$WorkDir/rsmk/${genome}rsmk.stat"  outputfile="$prefix.png"  < $WorkDir/peakDist.r
