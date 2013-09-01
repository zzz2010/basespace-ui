export rootdir=$3
export genomedir=$2
export PYTHONPATH=$rootdir/COMMONPY
export RLIB=$rootdir/LIB
export PATH=$rootdir/PROG:$PATH

WorkDir=`dirname "$0"`

peakfile=$1.2k
genomedir=$2
webseqtoolDir=$3
outdir=$4

head -n 2000 $1 > $peakfile
metanovo="python2.7 $webseqtoolDir/TASKS/metaNovo/run.py"

configfile=$outdir/"metanovo.cfg"

cat $WorkDir/config.txt |sed "s,GDIR,$genomedir,g"|sed "s,PFILE,$peakfile,g" |sed "s,OUTDIR,$outdir,g"   > $configfile 

$metanovo -configfile $configfile 2>&1





