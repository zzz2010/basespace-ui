rm -rf test/output
mkdir test/output

#python profileAroundPeaks_multiTag.py test/treated.bed test/output  test/CHB113.tags.unique test/CHB114.tags.unique test/CHB115.tags.unique

dir="/data5/zhizhuo/hTERT/CHH_new/FDR02"
dir2="/data5/zhizhuo/plap11_data/CHH_new"
python profile5k_gaye.py $dir/intersect.peak $dir   $dir2/control_CHH905_1/MAIN/CHH905.tags.unique $dir2/sample_CHH906/MAIN/CHH906.tags.unique $dir2/sample_CHH907/MAIN/CHH907.tags.unique $dir2/sample_CHH908/MAIN/CHH908.tags.unique
~ 
