'''
Created on Mar 21, 2013

@author: soke may
'''
import os
import sys
import glob
import commands

title=sys.argv[1]
genome=sys.argv[2]
cellline=sys.argv[3]
samples=sys.argv[4]
controls=sys.argv[5]
result_dir=sys.argv[6]
jobdesc_outfile=sys.argv[7]
toolpath=sys.argv[8]

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
                <thead><tr><th></th><th>Non-Map</th><th>Multi-Map</th><th>Unique</th><th>PCR-Filtered</th><th>Total</th></tr></thead>'
    
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
        
        num_reads_html='<tr><td>Number of Reads</td><td>'+num_unmap+'</td><td>'+num_mm +'</td><td><span class="label label-info">'+num_uniq+'</span></td><td><span class="label label-important">'+num_pcr+'</span></td><td><span class="label label-inverse">'+num_total+'</span></td></tr>'
        
        pct_reads_html='<tr><td>% (of total) Reads</td><td>'+getPercentageReads(num_unmap, num_total)+'</td><td>'+getPercentageReads(num_mm, num_total) +'</td><td>'+getPercentageReads(num_uniq, num_total)+'</td><td>'+getPercentageReads(num_pcr, num_total)+'</td><td>-</td></tr>'
        
        #plot distribution of reads
        outputdir=result_dir+'/job_info/'
        cmd='R ' + outputdir+ ' '+ num_unmap +' '+num_mm+' ' + num_uniq + ' --no-save < '+toolpath+'/plotPie.R'
        os.system(cmd)
        
        #DEBUG
        imgurl=str(outputdir+'/reads_distribution.png').replace("/home/sokemay/basespace/basespace-ui/basespace-ui","")
        plot_html='<tr><td colspan="6"><img src="'+ imgurl +'"></td></tr>'
        map_table+='<tbody>'+num_reads_html+pct_reads_html+plot_html + '</tbody></table>' #end of mapping stats table
        
    except:
        map_table+='</table>'    
    return map_table

def getStatsTable(fname):
    stats_table='<table class="table table-bordered table-condensed" id="stat_table"><thead><tr><th style="width:25%"></th><th>Length</th><th>Tags</th><th>Fold Enrichment</th></tr></thead><tbody>'
    
    try:
        f=open(fname).readlines()
        numpeaks=f[0]
        stats=f[1:]
        for i in xrange(len(stats)):
            l=stats[i].replace('"','')
            if i==0 or i==1:  #min and max
                stats_table+='<tr>'
            elif i==2:           #mean
                stats_table+='<tr class="error">'
            elif i==3:          #sd   
                stats_table+='<tr class="info">'
                
            tmpsplit=l.split('\t')

            for i in xrange(len(tmpsplit)):
                if i==0:
                    stats_table+='<td style="width:25%"><strong>' + str(tmpsplit[i]) + '</strong></td>'
                else:
                    stats_table+='<td style="width:25%">' + str(tmpsplit[i]) + '</td>'
            
        stats_table+='</tr>'
    except:
        stats_table+='</tbody></table>'
        
    stats_table+='</tbody></table>'
    return numpeaks,stats_table

def getThrStatsTable(fname,statType):
    table='<table class="table table-bordered table-condensed"><tr><td colspan="3"><strong>#Reads at Different '+statType+' Thresholds</strong></td></tr>'
    
    try:
        f=open(fname).readlines()
        for i in xrange(len(f)):
            l=f[i].replace('"','')
            table+='<tr>'
            tmpsplit=l.split('\t')
            
            #table+='<td style="width:33.3%">' + str(tmpsplit[0]) + '</td>'
            if i>0:
                for content in tmpsplit:
                    table+='<td style="width:33.3%">' + str(content) + '</td>'
                table+='</tr>'
            else:
                table+='<td style="width:33.3%"><span class="label label-info">'+tmpsplit[0] +'</span></td>\
                <td style="width:33.3%"><span class="label label-warning">'+ tmpsplit[1] + '</span></td>\
                <td style="width:33.3%"><span class="label label-error">' +tmpsplit[1] + '</span></td>'
    except:
        table+='</table>'
    table+='</table>'
    return table

def getRowContents(line):
    runattr=''
    runval=''
    pat1="is determined as"
    pat2=":"
    pat3="="
    
    if pat1 in line:
        runattr=line.split(pat1)[0]
        runval=line.split(pat1)[1]
    elif pat2 in line:
        runattr=line.split(pat2)[0]
        runval=line.split(pat2)[1]
    elif pat3 in line:
        runattr=line.split(pat3)[0]
        runval=line.split(pat3)[1]
        
    return runattr.strip(), runval.strip()

def getRunInfo(npeaks,fname):
    runinfo='<table class="table table-bordered table-condensed"><tr><td colspan="2"><strong>Run Info</strong></td></tr>'
    runinfo+='<tr><td style="width:50%;"><strong>No. of Peaks</strong></td><td><span class="label label-success">'+str(npeaks)+'</span></td></tr>'
    f=open(fname).readlines()
    for i in xrange(len(f)):
        if not f[i].startswith("#"):
            break
    pos=i+4
    for j in xrange((i+1),len(f)):
        if f[j].startswith("#"): #omit max dup tags at same pos info
            tmp=f[j]
            tmp=tmp.replace("#","").strip()
            runattr, runval =getRowContents(tmp)
            if j!=pos:
                runinfo+='<tr><td style="width:50%;"><strong>'+runattr+'</strong></td><td>' + runval+'</td></tr>'
        else:
            break
        
    return runinfo+'</table>'

def generatePkCallingStats(result_dir):
    pkcall_html='<div class="breadcrumb"><h4>Peak Calling Statistics</h4></div>'
    pkcall_outdir=result_dir+"/peakcalling_result/"
    peakxls= glob.glob(pkcall_outdir+"*.xls")[0]
    
    #get pkcalling stats from R script
    outputdir=result_dir+'/job_info/'
    cmd='R ' + outputdir+ ' '+ peakxls+ ' --no-save < '+toolpath+'/getPeakCallStats.R'
    os.system(cmd)
    
    numpeaks,stats_html=getStatsTable(outputdir+"stats.tmp")
    feStats=getThrStatsTable(outputdir+"feStats.tmp", "Fold Enrichment")
    pvalStats=getThrStatsTable(outputdir+"pvalStats.tmp", "-10*log10(pvalue)")
    bindTables='<div class="row-fluid"><div class="span6">'+stats_html+'</div><div class="span6">'+feStats+pvalStats+'</div></div>'
    
    macs_version='1.4.2'
    macs_info='<style> #table_macs td{text-align:center;width:50%} #table_macs tr td:FIRST-CHILD{font-weight:bold;}</style> <table id="table_macs" class="table table-bordered table-condensed"><tr><td colspan="2"><strong>MACS Arguments</strong></td></tr>\
    <tr><td>MACS Version</td><td>'+macs_version+'</td><tr><td>Effective Genome Size</td><td>2.70e+09</td></tr><tr><td>Band Width</td>\
    <td>300</td></tr><tr><td>Model Fold</td><td>10,30</td></tr><tr><td>p-value Cutoff</td><td>1.00e-05</td></tr><tr><td>Range for calculating regional lambda</td><td>10000 bps</td></tr></table>'
    
    run_info=getRunInfo(numpeaks, peakxls)

    bind_geninfo='<div class="row-fluid"><div class="span6">'+macs_info+'</div><div class="span6">' + run_info + '</div></div>'
    pkcall_html+=bind_geninfo + bindTables 
    return pkcall_html

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

div_files='<div class="row-fluid"><div class="span6">'+table_samples+'</div><div class="span6">'+table_controls+'</div></div>'

#generate read mapping and peak calling stats
pkCalling_dir=result_dir+"/peakcalling_result/"
pkconfig=pkCalling_dir+"pk.cfg"
pkconfigcontent=open(pkconfig).read()

pkcall_html=''
if pkconfigcontent.strip():
    map_html='<div class="breadcrumb"><h4>Reads Mapping Statistics</h4></div>'
    
    map_table=generateMappingStats(result_dir)
 
    map_html+=map_table
    pkcallstats_html=generatePkCallingStats(result_dir)
    pkcall_html= map_html+pkcallstats_html

#html_gen=html_desc+style_table+table_general+table_samples+table_controls
html_gen=html_desc+style_table+table_general+div_files
html_out=html_gen+ pkcall_html+'</div>'
jobdesc_out=open(jobdesc_outfile, 'w')
jobdesc_out.write(html_out)
jobdesc_out.close()


