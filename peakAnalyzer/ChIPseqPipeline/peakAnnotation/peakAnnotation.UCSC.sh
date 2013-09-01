### please note: peak region is defined as +/- 1bp from the center of the regions, or from the summit of the peaks. This depends on the definition
peakfile=$1
genome=$2
outdir=$3

WorkDir=`dirname "$0"`
x=$outdir/`basename $peakfile` 
    awk '{center = int(($2+$3)/2); printf("%s\t%ld\t%ld\t1\n",$1,center-1,center+1)}'  ${peakfile} > ${x}.region.txt
    echo ${x}.region.txt
    cp -f ${x}.region.txt ${x}.annotated.xls
    for y in promoters_2500bp_2500bp genes_regions exons.combined TTS_2500bp_2500bp promoters_0_20K 
    do
        java -cp $WorkDir/../LGL/LGL.jar LGL.overlap.RegionOverlapWithAnnotation ${x}.region.txt $WorkDir/genes/UCSC_${genome}/UCSC_${genome}_${y}.txt  ${x}.annotatedwith.${y}.txt
        echo ${x}.annotatedwith.${y}.txt 
        cut -f4 <${x}.annotatedwith.${y}.txt  | sort | uniq -c
        cut -f4,5 ${x}.annotatedwith.${y}.txt >${x}.annotatedwith.${y}.temp.txt
        paste ${x}.annotated.xls ${x}.annotatedwith.${y}.temp.txt >${x}.temp2.txt
        mv -f ${x}.temp2.txt ${x}.annotated.xls    
    done
    echo
    wc -l ${x}.region.txt
    echo promoters "(+/- 2.5Kb to TSS)"
    awk '{if(($5=="Yes"))print}' <${x}.annotated.xls | wc -l 
    awk '{if(($5=="Yes"))print}' <${x}.annotated.xls > ${x}.promoter.txt 
    echo exons "(excluding the regions 2.5Kb from TSS)"
    awk '{if(($5=="No") &&($9=="Yes"))print}' <${x}.annotated.xls | wc -l
    awk '{if(($5=="No") &&($9=="Yes"))print}' <${x}.annotated.xls > ${x}.exon.txt
    echo introns "(excluding the regions 2.5Kb from TSS)"
    awk '{if(($5=="No") &&($7=="Yes")&&($9=="No"))print}' <${x}.annotated.xls | wc -l
    awk '{if(($5=="No") &&($7=="Yes")&&($9=="No"))print}' <${x}.annotated.xls > ${x}.intron.txt
    echo "3-prime"s "(0-2.5Kb from transcription termination site)"
    awk '{if(($5=="No") &&($7=="No")&&($9=="No")&&($11=="Yes"))print}' <${x}.annotated.xls | wc -l
    awk '{if(($5=="No") &&($7=="No")&&($9=="No")&&($11=="Yes"))print}' <${x}.annotated.xls > ${x}.3-prime.txt
    echo distal promoters "(2.5Kb-20Kb upstream of TSS)"
    awk '{if(($5=="No") &&($7=="No")&&($9=="No")&&($11=="No")&&($13=="Yes"))print}' <${x}.annotated.xls | wc -l
    awk '{if(($5=="No") &&($7=="No")&&($9=="No")&&($11=="No")&&($13=="Yes"))print}' <${x}.annotated.xls > ${x}.distal-promoter.txt
    echo inter-genics "(20Kb upstream of any TSS, and 2.5Kb downstream of any TSS)"
    awk '{if(($5=="No") &&($7=="No")&&($9=="No")&&($11=="No")&&($13=="No"))print}' <${x}.annotated.xls | wc -l
    awk '{if(($5=="No") &&($7=="No")&&($9=="No")&&($11=="No")&&($13=="No"))print}' <${x}.annotated.xls > ${x}.inter-genic.txt

python $WorkDir/./summarize.py `basename ${x}` $genome $outdir
#rm $outdir/*temp*
#rm $outdir/*annotate*
#rm *region*

