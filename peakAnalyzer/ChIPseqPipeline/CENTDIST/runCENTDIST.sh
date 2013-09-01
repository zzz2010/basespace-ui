export rootdir=$4
export genomedir=$2
export PYTHONPATH=$rootdir/COMMONPY
export RLIB=$rootdir/LIB


WorkDir=`dirname "$0"`
peakfile=$1
genomedir=$2
pwmfile=$3
webseqtoolDir=$4
outdir=$5

centdist="python2.7 $webseqtoolDir/TASKS/Motif_Enrichment/run.py"

configfile=$outdir/"centdist.cfg"

cat $WorkDir/config.txt |sed "s,GDIR,$genomedir,g"|sed "s,PFILE,$peakfile,g" |sed "s,OUTDIR,$outdir,g" |sed "s,PWMFILE,$pwmfile,g"  > $configfile 

$centdist -configfile $configfile 2>&1





