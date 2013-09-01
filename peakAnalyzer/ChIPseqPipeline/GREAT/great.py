import sys
import os
import urllib2

bed=sys.argv[1]
genome=sys.argv[2]
outdir=sys.argv[3]

bname=os.path.basename(bed)
bedurl=os.path.abspath(bed).replace("/home/sokemay/basespace/basespace-ui/basespace-ui/", "http://genome.ddns.comp.nus.edu.sg/")

print bedurl

greaturl="http://great.stanford.edu/public/cgi-bin/greatStart.php?outputType=batch&requestSpecies="+genome+"&requestURL="+bedurl

print greaturl

f =urllib2.urlopen(greaturl)
lines=f.readlines()
outfileName=outdir+"/" + bname+".great.out" 
outfile=open(outfileName, "w")
outfile.write(" ".join(lines))
outfile.close()



