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
result_dir=sys.argv[6]
jobdesc_outfile=sys.argv[7]

#job=get_object_or_404(RegularJob, pk=jobid)
#title=str(job.jobtitle)
#genome=str(job.ref_genome)
#cellline=str(job.cell_line)
#samples=str(job.sampleFiles)
#controls=str(job.controlFiles)

samplelist=samples.split(",")
numsamples=len(samplelist)
#generate general job desc table
html='<div><div class="breadcrumb"><h4>Job Description </h4></div>'
style_table='<style> .table.table-bordered.table-condensed td{text-align:center;}#table_general td{}#table_samples td{width:50%;}</style>'
table_general='<table  class="table table-bordered table-condensed" id="table_general">\
<tr class="info"><td><strong>Job Title</strong></td><td><strong>Assembly</strong></td><td><strong>Detected Cell-line</strong></td>\
<td ><strong>Sample files</strong></td><td><strong>File Size</strong></td> <td><strong>Control files</strong></td><td><strong>File Size</strong></td></tr>\
<tr><td rowspan="'+str(numsamples)+'">' +title+'</td><td rowspan="'+str(numsamples)+'"><a target="_blank" href="http://genome.ucsc.edu/cgi-bin/hgGateway?db='+genome+'">'+genome+'</a></td><td rowspan="'+str(numsamples)+'">'+cellline+'</td>\
</tr>'

table_general+="</table>"
table_samples='<table class="table table-bordered table-condensed" id="table_samples"><tr class="info"><td ><strong>Sample files</strong></td><td><strong>File Size</strong></td><tr>'    


for f in samplelist:
    bname=os.path.basename(f)
    fsize=os.path.getsize(f)
    fsize_str=GetHumanReadable(fsize)
    table_samples+='<tr><td>'+bname +'</td><td>'+fsize_str+'</td></tr>'
table_samples+='</table>'

#generate read mapping and peak calling stats
pkCalling_dir=result_dir+"/peakcalling_result/"
pkconfig=pkCalling_dir+"pk.cfg"
pkconfigcontent=open(pkconfig).read()

pkcall_html=''
if pkconfigcontent.strip():
    map_html='<div class="breadcrumb"><h4>Reads Mapping Statistics</h4></div>'
    pkcallstats_html='<div class="breadcrumb"><h4>Peak Calling Statistics</h4></div>'
    pkcall_html= map_html+pkcallstats_html

html_jobdesc=html+style_table+table_general+table_samples+ pkcall_html+'</div>'
jobdesc_out=open(jobdesc_outfile, 'w')
jobdesc_out.write(html_jobdesc)
jobdesc_out.close()


