for x in CHE049M_L3  CHG007M_L5  CHK019M_L5  CHM160M_L4  CHM163M_L4
#for x in CHE048M_L2 CHG016M_L4 CHM076M CHM077M CTCF_K562M_L7
do
    awk '{if($9=="Yes")print $2}' < ${x}.peak.annotated.xls > ${x}.petCount.withInteraction.txt
    awk '{if($9=="No") print $2}' < ${x}.peak.annotated.xls > ${x}.petCount.withoutInteraction.txt
    #R --no-save --no-readline --args interFile="${x}.petCount.withInteraction.txt" noInterFile="${x}.petCount.withoutInteraction.txt" outputPrefix="${x}.petCountDist"  ylabel="PET counts" < petCountBoxplot.r
done

