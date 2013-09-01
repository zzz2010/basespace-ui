# python plotHistoneDist.py CHB115_guoliang.peak Hmec
import os
import sys
import glob

print '<Usage> <peak_file.BED> <file.bigWig> <output_file>'

peakfile=sys.argv[1]
bwfile=sys.argv[2]
output=sys.argv[3]

os.system("./plotWigDensity_peak_jq.sh "+peakfile+" "+bwfile+" > "+output)
print "DONE - ./plotWigDensity_peak.sh"
#os.system("R "+datfiles_str+" --no-save --args --slave < "+toolpath+"plotBigWigSummary_multi.R") 
#os.system("R "+datfiles_str+" --no-save --args --slave < "+toolpath+"plotGaye.R")
 
#os.system("rm "+datfiles_str)
