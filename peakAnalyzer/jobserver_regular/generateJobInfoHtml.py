'''
Created on Mar 21, 2013

@author: soke may
'''
import os
import sys
import glob
import commands

def GetHumanReadable(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
        rounded=round(size,precision)
    return str(rounded)+" "+suffixes[suffixIndex]

def getPercentageReads(noreads, totreads):
    fractionreads=float(noreads)/float(totreads)
    pctreads=round((fractionreads*100), 2)
    return str(pctreads) + "%"

def generateMappingStats(result_dir):
    pkcall_outdir=result_dir+"/peakcalling_result/"
    maplogfile= glob.glob(pkcall_outdir+"*.maplog.txt")[0]
    pcrfilterfile=glob.glob(pkcall_outdir+"*.unique")[0]

    map_table='<table class="table table-bordered table-condensed">\
                <thead><tr><th></th><th>Non-Mapped</th><th>Multi-Map</th><th>Unique</th><th>PCR-Filtered</th><th>Total</th></tr></thead>'
    
    try:
        maplog=open(maplogfile,'r').readlines()
        maplog=maplog[1:5]
        
        numreads=list()
        pctreads=list()
        for l in maplog:
            bracketIndex=l.find("(")
            numreads.append(l[0:bracketIndex].strip())
        
        status,output=commands.getstatusoutput("wc -l " + pcrfilterfile)
        num_pcr=output.split()[0]
        num_total=numreads[0]
        num_unmap=numreads[1]
        num_uniq=numreads[2]
        num_mm=numreads[3]
        
        num_reads_html='<tr><td>Number of Reads</td><td>'+num_unmap+'</td><td>'+num_mm +'</td><td>'+num_uniq+'</td><td>'+num_pcr+'</td><td>'+num_total+'</td></tr>'
        
        pct_reads_html='<tr><td>%(of total) Reads</td><td>'+getPercentageReads(num_unmap)+'</td><td>'+getPercentageReads(num_mm) +'</td><td>'+getPercentageReads(num_uniq)+'</td><td>'+getPercentageReads(num_pcr)+'</td><td>'+getPercentageReads(num_total)+'</td></tr>'
    
        
        map_table+='<tbody>'+'</tbody></table>'
        
    except:
        map_table+='</table>'    
    return map_table

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

#generate general job desc table
html_desc='<div><div class="breadcrumb"><h4>Job Description </h4></div>'
style_table='<style> .table.table-bordered.table-condensed td{text-align:center;}#table_general td{width:33.33%;}#table_samples td{width:50%;}#table_controls td{width:50%;}.table.table-bordered.table-condensed th{text-align:center;}</style>'
table_general='<table  class="table table-bordered table-condensed" id="table_general">\
<tr class="info"><td><strong>Job Title</strong></td><td><strong>Assembly</strong></td><td><strong>Detected Cell-line</strong></td></tr>\
<tr><td>' +title+'</td><td><a target="_blank" href="http://genome.ucsc.edu/cgi-bin/hgGateway?db='+genome+'">'+genome+'</a></td><td>'+cellline+'</td></tr></table>'


#sample list table
table_samples='<table class="table table-bordered table-condensed" id="table_samples"><tr class="info"><td ><strong>Sample files</strong></td><td><strong>File Size</strong></td><tr>' 
samplelist=samples.split(",")
for f in samplelist:
    bname=os.path.basename(f)
    fsize=os.path.getsize(f)
    fsize_str=GetHumanReadable(fsize)
    table_samples+='<tr><td>'+bname +'</td><td>'+fsize_str+'</td></tr>'
table_samples+='</table>'

#control list table
table_controls='' 
controllist=controls.split(",")
if controllist:
    table_controls+='<table class="table table-bordered table-condensed" id="table_controls"><tr class="info"><td ><strong>Control files</strong></td><td><strong>File Size</strong></td><tr>'
    for f in controllist:
        if f:
            bname=os.path.basename(f)
            fsize=os.path.getsize(f)
            fsize_str=GetHumanReadable(fsize)
            table_controls+='<tr><td>'+bname +'</td><td>'+fsize_str+'</td></tr>'
        else:
            table_controls+='<tr><td>None</td><td>-</td></tr>'
    table_controls+='</table>'

div_files='<div class="row"><div class="span6">'+table_samples+'</div><div class="span6">'+table_controls+'</div></div>'

#generate read mapping and peak calling stats
pkCalling_dir=result_dir+"/peakcalling_result/"
pkconfig=pkCalling_dir+"pk.cfg"
pkconfigcontent=open(pkconfig).read()

pkcall_html=''
if pkconfigcontent.strip():
    map_html='<div class="breadcrumb"><h4>Reads Mapping Statistics</h4></div>'
    
    map_table=generateMappingStats(result_dir)
 
    map_html+=map_table
    pkcallstats_html='<div class="breadcrumb"><h4>Peak Calling Statistics</h4></div>'
    pkcall_html= map_html+pkcallstats_html

#html_gen=html_desc+style_table+table_general+table_samples+table_controls
html_gen=html_desc+style_table+table_general+div_files
html_out=html_gen+ pkcall_html+'</div>'
jobdesc_out=open(jobdesc_outfile, 'w')
jobdesc_out.write(html_out)
jobdesc_out.close()


