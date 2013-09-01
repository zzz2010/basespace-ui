inputbed=$1
genome=$2
outdir=$3    
x=`basename $inputbed`

WorkDir=`dirname "$0"`
## bin size: 100Kb
java -cp $WorkDir/../LGL/LGL.jar LGL.shortReads.ProfileGenome $inputbed  $WorkDir/./genome_length_$genome.txt $WorkDir/./profileConfig.txt $outdir/${x}

R $outdir/${x}.profile.xls $WorkDir/chroms.txt --no-save < $WorkDir/plotProfiles.r

