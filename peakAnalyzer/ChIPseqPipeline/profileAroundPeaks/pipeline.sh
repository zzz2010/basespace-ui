for x in profile_10bp_2Kbins # profile_10bp_200bins
do
    java -cp /data3/guoliang/lib/LGL.jar LGL.shortReads.ProfileRegion2 ../uniquereads/check/newpauline_peak/CHB115.tags.unique  treated_ccat.txt.bed ${x}.txt  treated_tag.aroundPeaks.10Kb
    java -cp /data3/guoliang/lib/LGL.jar LGL.shortReads.ProfileRegion2 ../uniquereads/check/newpauline_peak/CHB114.tags.unique  treated_ccat.txt.bed ${x}.txt  untreated_tag.aroundPeaks.10Kb
    java -cp /data3/guoliang/lib/LGL.jar LGL.shortReads.ProfileRegion2 ../uniquereads/check/newpauline_peak/CHB113.tags.unique  treated_ccat.txt.bed ${x}.txt  input_tag.aroundPeaks.10Kb
done

