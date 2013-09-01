libDir=$1
ccat_FC=$2
macs_FC=$3
outdir=$4

libname=`basename $libDir`
WorkDir=`dirname "$0"`
fulloutdir=$outdir/fullpeak/

mkdir $fulloutdir
sh $WorkDir/getbed_ccat.sh $libDir/CCAT3/*.significant.peak ${ccat_FC} > $outdir/${libname}_ccat.bed

rm $libDir/MACS/*_negative_peaks.xls

sh $WorkDir/getbed_macs.sh $libDir/MACS/*_peaks.xls ${macs_FC} > $outdir/${libname}_macs.bed


if [  -s "$outdir/${libname}_ccat.bed" ]
then
        echo "";
sh $WorkDir/getbed_ccat.sh $libDir/CCAT3/*.significant.peak 1 > $fulloutdir/${libname}_ccat.bed
else
        rm $outdir/${libname}_ccat.bed
fi

if [  -s "$outdir/${libname}_macs.bed" ]
then
        echo "";
sh $WorkDir/getbed_macs.sh $libDir/MACS/*_peaks.xls 1 > $fulloutdir/${libname}_macs.bed
else
        rm $outdir/${libname}_macs.bed
fi
