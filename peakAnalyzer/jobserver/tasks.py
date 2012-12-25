'''
Created on 2012-12-21

@author: zhangzhizhuo
'''
from celery import task
from basespace.models import Project,User,AppResult,Sample,File,Session
import os,glob
import ConfigParser
from jobserver.models import Job
from celery import chord,group,chain
from jobserver import settings
import operator

def mkpath(outdir):
        if not os.path.exists(outdir):
                os.makedirs(outdir)

@task
def downloadFile(fid,session_id,outFileName):
    if os.path.exists(outFileName):
        return
    session=Session.objects.get(pk=session_id)
    api=session.getBSapi()
    api.fileDownload(fid,os.path.dirname(outFileName),os.path.basename(outFileName))
    
@task
def basespace_download_update_task(sfidlist,cfidlist,session_id,outdir,jobid):
    session=Session.objects.get(pk=session_id)
    api=session.getBSapi()
    s_outfiles=list()
    c_outfiles=list()
    downloadtaks_list=list()
    logger = basespace_Download_PeakCalling_Processing.get_logger(logfile='tasks.log')
    
    for fid in sfidlist:
        f = api.getFileById(fid)
        outfile=outdir+str(fid)+"__"+f.Name
        s_outfiles.append(outfile)
        logger.info("Adding %s" % (outfile))
        downloadtaks_list.append(downloadFile.s(fid,session_id,outfile))
       # downloadGroup.
    for fid in cfidlist:
        f = api.getFileById(fid)
        outfile=outdir+str(fid)+"__"+f.Name
        c_outfiles.append(outfile)
        logger.info("Adding %s" % (outfile))
        downloadtaks_list.append(downloadFile.s(fid,session_id,outfile))
    #do download parallel
    downG=group(downloadtaks_list)()
    downG.get(timeout=1000*60*60)
    #do the update database
    myjob=Job.objects.get(pk=jobid)
    myjob.sampleFiles=s_outfiles
    myjob.controlFiles=c_outfiles
    myjob.status="Data_Ready"
    myjob.save()
      
@task()
def add(x, y):
    return x + y
#########################################ChIPseq Pipeline#####################################
@task
def Denovo_Motif(peakfile,outdir2,genome):
    mkpath(outdir2)
    cmd="sh "+settings.toolpath+"./DenovoMotif/runMetaNovo.sh "+peakfile+" "+settings.GenomeDIR+"/"+genome+"/ "+settings.WebseqtoolDIR+" "+outdir2+" > "+outdir2+"/log.txt 2>&1"
    print cmd
    exec(cmd)
    
@task
def CENTDIST(peakfile,outdir2,genome,denovoDir):
    mkpath(outdir2)
    if denovoDir!="":
        cmd1="python "+settings.toolpath+"/CENTDIST/combineDeNovo.py "+denovoDir+" "+outdir2
        print cmd1
        exec(cmd1)
    cmd="sh "+settings.toolpath+"/CENTDIST/runCENTDIST.sh "+peakfile+" "+settings.GenomeDIR+"/"+genome+"/ "+outdir2+"/motifDB "+settings.WebseqtoolDIR+" "+outdir2
    print cmd
    exec(cmd)

@task
def TagProfileAroundPeaks(peakfile,outdir2,inputdir):
    taglist=glob.glob(inputdir+"/*/MAIN/*.tags.unique")
    mkpath(outdir2)
    cmd2="python "+settings.toolpath+"./profileAroundPeaks/profile5k.py "+peakfile+" "+outdir2+" "+" ".join(taglist)
    print cmd2
    exec(cmd2)

##repeat analysis###
@task
def repeatAnalysis(peakfile,outdir2,genome):
    mkpath(outdir2)
    cmd="sh "+settings.toolpath+"./repeatAnalysis/overlaprepeat.sh "+peakfile+" "+genome+" "+outdir2
    print cmd
    exec(cmd)
  
@task
def TSSPlot(peaklist,outdir2,genome):
    mkpath(outdir2)
    cmd="python "+settings.toolpath+"./TSSPlot/TssDistTable.py "+genome
    for peak in peaklist:
            cmd+=" "+peak
    exec(cmd+" > "+outdir2+"/peak_tssplot.txt")
    exec("R "+outdir2+"/peak_tssplot.txt  --no-save "+" < "+settings.toolpath+"./TSSPlot/plotTss.R &")

@task
def conservationPlot(peakfile,outdir2,genome):
    mkpath(outdir2)
    cmd="sh "+settings.toolpath+"./conservationPlot/plotCons.sh "+peakfile+" "+settings.phastconsDIR+"/"+genome+" "+outdir2
    print cmd
    exec(cmd)
    

@task
def genomeProfile(peakfile,outdir2,genome):
    mkpath(outdir2)
    cmd="sh "+settings.toolpath+"./genomeProfile/profileGenome.sh "+peakfile+" "+genome+" "+outdir2
    print cmd
    exec(cmd)

@task 
def GREAT(peakfile,outdir2,genome):  
    mkpath(outdir2)
    bed3peak=outdir2+os.path.basename(peakfile)
    os.system("cut -f 1-3 "+peakfile+" > "+bed3peak)
    cmd="python "+settings.toolpath+"./GREAT/runGREAT.py "+bed3peak+" "+genome+" "+outdir2
    print cmd
    exec(cmd)



    

@task
def Pipeline_Processing_task_general(peaklist,taskconfig):
    taskStr=""
    if taskconfig.has_option("task","task"):
            taskStr=taskconfig.get("task", "task")
    taskSet=set(taskStr.split(","))
    if taskStr=="":
            taskSet=set()
    inputdir=taskconfig.get("task", "dataDIR")
    outdir=taskconfig.get("task", "outputDIR")
    genome=taskconfig.get("task", "genome")
    tasklist=list()
    for peakfile in peaklist:
        #denovo motif
        if len(taskSet)==0 or "denovoMotif" in taskSet :
            outdir2=outdir+"/denovoMotif/"
            tasklist.append(Denovo_Motif.s(peakfile,outdir2,genome))
            
        #CENTDIST
        if len(taskSet)==0 or "CENTDIST" in taskSet :
            denovoDir=""
            if len(taskSet)==0 or "denovoMotif" in taskSet:
                denovoDir=outdir+"/denovoMotif/"
                tasklist[len(tasklist)-1]=chain((tasklist[len(tasklist)-1],CENTDIST.s(peakfile,outdir2,genome,denovoDir)))
            else:
                tasklist.append(CENTDIST.s(peakfile,outdir2,genome,denovoDir))
        
        ##Tag around peak##
        if len(taskSet)==0 or "TagProfileAroundPeaks" in taskSet :
            outdir2=outdir+"/TagProfileAroundPeaks/"
            tasklist.append(TagProfileAroundPeaks.s(peakfile,outdir2,inputdir))
        
        ##repeat analysis###
        if len(taskSet)==0 or "repeatAnalysis" in taskSet :
            outdir2=outdir+"/repeatAnalysis/"
            tasklist.append(repeatAnalysis.s(peakfile,outdir2,genome))
            
        ##Conservation Plot##
        if len(taskSet)==0 or "conservationPlot" in taskSet :
            outdir2=outdir+"/conservationPlot/"
            tasklist.append(conservationPlot.s(peakfile,outdir2,genome))
        
        ##Genome Profile Plot##
        if len(taskSet)==0 or "genomeProfile" in taskSet :
            outdir2=outdir+"/genomeProfile/"
            tasklist.append(genomeProfile.s(peakfile,outdir2,genome))
            
        ##GO analysis##
        if len(taskSet)==0 or "GREAT" in taskSet :
            outdir2=outdir+"/GREAT/"
            tasklist.append(GREAT.s(peakfile,outdir2,genome))
            
            
    return group(tasklist)

def checkCellName(testName, knownName):
    return (testName in knownName) or (knownName in testName)


def getMostOccCellName(lines):
    cell_count=dict()
    for cell in settings.known_cells:
        cell_count[cell]=0
    for line in lines:
        comps=line.strip().split()
        fname=os.path.basename(comps[0])
        for cell in cell_count.keys():
            if cell in fname:
                cell_count[cell]+=cell_count[cell]
                break
    
    sorted_x = sorted(cell_count.iteritems(), key=operator.itemgetter(1))
    cell_line=sorted_x[len(sorted_x)-1][0]
    return cell_line
        
@task   
def ENCODE_TF_chipseq(peakfile,outdir2,genome):
    cmd="sh "+settings.toolpath+"./peaksetSummary/peaksetSummary.sh "+peakfile+" '"+settings.ENCODEchipseqDIR+"/"+genome+"/*.narrowPeak' "+outdir2
    print cmd
    exec(cmd)
    cell_line=""
    try:
        lines=open(outdir2+os.path.basename(peakfile)+".peakset.overlap.top").readlines()
        cell_line=getMostOccCellName(lines)
    except:
        cell_line=""
    return cell_line


@task
def histonePlot(peakfile,outdir2,genome,cellline_used):
    #check data generator: broad
    histoneDir=settings.ENCODEhistoneDIR+"/"+genome+"/"
    datastr="".join(glob.glob(histoneDir+"*"+cellline_used+"*.bigWig"))
    if "BroadHistone" in datastr:
            cellline_used="BroadHistone"+cellline_used
    elif "SydhHistone" in datastr:
            cellline_used="SydhHistone"+cellline_used
    elif "UwHistone" in datastr:
            cellline_used="UwHistone"+cellline_used
    cmd="python "+settings.toolpath+"./histonePlot/plotHistoneDist.py "+peakfile+" "+cellline_used+" "+histoneDir+" "+outdir2
    print cmd
    exec(cmd)
    if cellline_used=="":
        #check the cell line with largest file size
        datfiles=glob.glob(outdir2+"*.dat")
        flsizes=dict()
        for fl in datfiles:
            flsizes[os.path.basename(fl)]=os.path.getsize(fl)
            
        sorted_x = sorted(flsizes.iteritems(), key=operator.itemgetter(1))
        sorted_x.reverse()
        lines=list()
        for x in sorted_x[0:5]:
            lines.append(x[0])
        cellline_used=getMostOccCellName(lines)
    return cellline_used

@task
def Pipeline_Processing_task_cellline(peaklist,taskconfig):
    taskStr=""
    if taskconfig.has_option("task","task"):
            taskStr=taskconfig.get("task", "task")
    taskSet=set(taskStr.split(","))
    if taskStr=="":
            taskSet=set()
    inputdir=taskconfig.get("task", "dataDIR")
    outdir=taskconfig.get("task", "outputDIR")
    genome=taskconfig.get("task", "genome")
    tasklist=list()
    
    cellline1=taskconfig.get("task","cellline")
    cellline2=taskconfig.get("task","alternative_cellline")
    known_match_cell=""
    for known_cell in settings.known_cells:
        if checkCellName(cellline1, known_cell):
            known_match_cell=known_cell
            break
        elif checkCellName(cellline2, known_cell):
            known_match_cell=known_cell
            break
    for peakfile in peaklist:
        #encode_chipseq overlap#
        outdir2=outdir+"/encode_chipseq/"
        if known_match_cell=="":
            known_match_cell=ENCODE_TF_chipseq(peakfile,outdir2,genome)
        else:
            tasklist.append(ENCODE_TF_chipseq.s(peakfile,outdir2,genome))
        
        #encode_histone profile#
        if known_match_cell=="":
            known_match_cell=histonePlot(peakfile,outdir2,genome,"")
        else:
            tasklist.append(histonePlot.s(peakfile,outdir2,genome,known_match_cell))
        
    return group(tasklist)
            
@task
def Pipeline_Processing_task(taskconfigfile,outdir,jobid):
    #do the update database
    myjob=Job.objects.get(pk=jobid)
    myjob.status="Processing"
    myjob.save()
    try:
        taskconfig=ConfigParser.ConfigParser()
        taskconfig.readfp(open(taskconfigfile))
        inputdir=taskconfig.get("task", "dataDIR")
        outdir=taskconfig.get("task", "outputDIR")
        genome=taskconfig.get("task", "genome")
        peakdir=outdir+"/peakfiles/"
        if not os.path.exists(peakdir):
                os.makedirs(peakdir)
        
        for lib in os.listdir(inputdir):
                libdir=inputdir+"/"+lib
                if os.path.isdir(libdir):
                        exec("sh "+settings.toolpath+"./preprocessing/preprocess.sh "+libdir+" "+taskconfig.get("task", "CCAT_FC")+" "+taskconfig.get("task", "MACS_FC")+" "+peakdir)
        outf=open(peakdir+"/peakcount.html",'w')
        peaklist=glob.glob(peakdir+"/*_*.bed")
        fullpeaklist=glob.glob(peakdir+"/fullpeak/*_*.bed")
        grouptasks=group(Pipeline_Processing_task_general.s(peaklist,taskconfig),Pipeline_Processing_task_cellline.s(peaklist,taskconfig))
        grouptasks.get(timeout=1000*60*60)
        #do the update database
        myjob=Job.objects.get(pk=jobid)
        myjob.status="Completed"
        myjob.save()
    except:
        myjob=Job.objects.get(pk=jobid)
        myjob.status="Error"
        myjob.save()
    
@task
def basespace_Download_PeakCalling_Processing(sfidlist,cfidlist,session_id,outdir,jobid):
    #download first
    basespace_download_update_task(sfidlist,cfidlist,session_id,outdir,jobid)
    
    #peak calling
    
    
    #processing 
    