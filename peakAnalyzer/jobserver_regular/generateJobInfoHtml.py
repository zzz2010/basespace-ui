'''
Created on Mar 21, 2013

@author: soke may
'''
import os
import sys

def GetHumanReadable(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
        rounded=round(size,precision)
    return str(rounded)+" "+suffixes[suffixIndex]

title=sys.argv[1]
genome=sys.argv[2]
cellline=sys.argv[3]
samples=sys.argv[4]
controls=sys.argv[5]
jobdesc_outfile=sys.argv[6]

html='<div><div class="breadcrumb"><h4>Job Description </h4></div>'
style_table='<style> .table.table-bordered.table-condensed td{text-align:center;}#table_general td{width:33.33%;}#table_samples td{width:50%;}</style>'
table_general='<table  class="table table-bordered table-condensed" id="table_general">\
<tr class="info"><td><strong>Job Title</strong></td><td><strong>Assembly</strong></td><td><strong>Detected Cell-line</strong></td></tr>\
<tr><td>' +title+'</td><td><a href="http://genome.ucsc.edu/cgi-bin/hgGateway?db='+genome+'">'+genome+'</a></td><td>'+cellline+'</td></tr></table>'

table_samples='<table class="table table-bordered table-condensed" id="table_samples"><tr class="info"><td ><strong>Sample files</strong></td><td><strong>File Size</strong></td><tr>'    

samplelist=samples.split(",")
for f in samplelist:
    bname=os.path.basename(f)
    fsize=os.path.getsize(f)
    fsize_str=GetHumanReadable(fsize)
    table_samples+='<tr><td>'+bname +'</td><td>'+fsize_str+'</td></tr>'
table_samples+='</table>'

html_jobdesc=html+style_table+table_general+table_samples+'</div>'
jobdesc_out=open(jobdesc_outfile, 'w')
jobdesc_out.write(html_jobdesc)
jobdesc_out.close()


