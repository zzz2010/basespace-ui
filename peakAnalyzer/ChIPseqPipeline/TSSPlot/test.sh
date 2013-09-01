#python TssDistTable2.py test/histone_peak/pb1_hg19.tss  test/histone_peak/*.bed > test/tss.dist

#python profile5k_yf.py   test/histone_peak/pb1_hg19.tss  test/ test/tag/*.bed #
#python profile5k_yf.py   test/histone_peak/e2f1_hg19.tss  test/ test/tag/B*.bed test/tag/C*.bed test/tag/E*.bed test/tag/P*.bed 


#python TssDistTable.py hg19 /home/sokemay/basespace/basespace-ui/basespace-ui/peakAnalyzer/userdata/sokemay@gmail.com/19/peakcalling_result/ctcfpeak_ixn.summits.bed > test/peak_tssplot.txt


python TssDistTable.py hg19 /home/sokemay/test_scriptd/uu_AR.bed > test/peak_tssplot.txt

R test/peak_tssplot.txt --no-save < plotTss.R
