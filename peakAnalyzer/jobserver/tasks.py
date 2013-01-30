'''
Created on 2012-12-21

@author: zhangzhizhuo
'''
from celery import task
from basespace.models import Project,User,AppResult,Sample,File,Session
import os,glob,traceback
import ConfigParser
from jobserver.models import Job
from celery import chord,group,chain
from jobserver import settings
import basespace.settings
import peakAnalyzer
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
##change
def basespace_download_update_task(sfidlist,cfidlist,session_id,outdir,jobid):
    session=Session.objects.get(pk=session_id)
    api=session.getBSapi()
    s_outfiles=list()
    c_outfiles=list()
    downloadtaks_list=list()
    logger = basespace_Download_PeakCalling_Processing.get_logger(logfile='tasks.log')
    
    print "sfidlist", sfidlist
    print "cfidlist", cfidlist
    
    for fid in sfidlist:
        if(str(fid).isdigit()):
            f = api.getFileById(fid)
            outfile=outdir+str(fid)+"__"+f.Name
            s_outfiles.append(outfile)
            logger.info("Adding %s" % (outfile))
            downloadtaks_list.append(downloadFile.s(fid,session_id,outfile)) #skip this step for uploaded file
        else:
            outfile2=outdir+str(fid)
            s_outfiles.append(outfile2)
           # downloadGroup.
    for fid in cfidlist:
        if(str(fid).isdigit()):
            f = api.getFileById(fid)
            outfile=outdir+str(fid)+"__"+f.Name
            c_outfiles.append(outfile)
            logger.info("Adding %s" % (outfile))
            downloadtaks_list.append(downloadFile.s(fid,session_id,outfile))
        else:
            outfile2=outdir+str(fid)
            c_outfiles.append(outfile2)
    #do download parallel
    if downloadtaks_list:
        downG=group(downloadtaks_list)()
        downG.get(timeout=1000*60*60)
    #do the update database
    myjob=Job.objects.get(pk=jobid)
    myjob.sampleFiles=",".join(s_outfiles)
    myjob.controlFiles=",".join(c_outfiles)
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
    os.system(cmd)
    return outdir2
    
@task
def CENTDIST(denovoDir,peakfile,outdir2,genome):
    mkpath(outdir2)
    if denovoDir!="":
        cmd1="python "+settings.toolpath+"/CENTDIST/combineDeNovo.py "+denovoDir+" "+outdir2
        print cmd1
        os.system(cmd1)
    cmd="sh "+settings.toolpath+"/CENTDIST/runCENTDIST.sh "+peakfile+" "+settings.GenomeDIR+"/"+genome+"/ "+outdir2+"/motifDB "+settings.WebseqtoolDIR+" "+outdir2
    print cmd
    os.system(cmd)

@task
def TagProfileAroundPeaks(peakfile,outdir2,inputdir):
    taglist=glob.glob(inputdir+"/*.tags.unique")
    mkpath(outdir2)
    cmd2="python "+settings.toolpath+"./profileAroundPeaks/profile5k.py "+peakfile+" "+outdir2+" "+" ".join(taglist)
    print cmd2
    os.system(cmd2)

##repeat analysis###
@task
def repeatAnalysis(peakfile,outdir2,genome):
    mkpath(outdir2)
    cmd="sh "+settings.toolpath+"./repeatAnalysis/overlaprepeat.sh "+peakfile+" "+genome+" "+outdir2
    print cmd
    os.system(cmd)
  
@task
def TSSPlot(peaklist,outdir2,genome):
    mkpath(outdir2)
    cmd="python "+settings.toolpath+"./TSSPlot/TssDistTable.py "+genome
    for peak in peaklist:
            cmd+=" "+peak
    os.system(cmd+" > "+outdir2+"/peak_tssplot.txt")
    os.system("R "+outdir2+"/peak_tssplot.txt  --no-save "+" < "+settings.toolpath+"./TSSPlot/plotTss.R &")

@task
def conservationPlot(peakfile,outdir2,genome):
    mkpath(outdir2)
    cmd="sh "+settings.toolpath+"./conservationPlot/plotCons.sh "+peakfile+" "+settings.phastconsDIR+"/"+genome+" "+outdir2
    print cmd
    os.system(cmd)
    

@task
def helloworld():
    print "hello world"

@task
def genomeProfile(peakfile,outdir2,genome):
    mkpath(outdir2)
    cmd="sh "+settings.toolpath+"./genomeProfile/profileGenome.sh "+peakfile+" "+genome+" "+outdir2
    print cmd
    os.system(cmd)

@task 
def GREAT(peakfile,outdir2,genome):  
    mkpath(outdir2)
    bed3peak=outdir2+os.path.basename(peakfile)
    os.system("cut -f 1-3 "+peakfile+" > "+bed3peak)
    cmd="python "+settings.toolpath+"./GREAT/runGREAT.py "+bed3peak+" "+genome+" "+outdir2
    print cmd
    os.system(cmd)


@task
def peakAnnotation(peakfile, outdir2, genome):
    mkpath(outdir2)
    cmd="sh "+settings.toolpath+"./peakAnnotation/peakAnnotation.UCSC.sh "+peakfile+" "+genome+" "+outdir2
    print cmd           
    os.system(cmd)
    

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
    print taskSet
    for peakfile in peaklist:
        #denovo motif
        if len(taskSet)==0 or "denovoMotif" in taskSet :
            outdir2=outdir+"/denovoMotif/"
            tasklist.append(Denovo_Motif.s(peakfile,outdir2,genome))
            
        #CENTDIST
        if len(taskSet)==0 or "CENTDIST" in taskSet :
            denovoDir=""
            outdir2=outdir+"/CENTDIST/"
            if len(taskSet)==0 or "denovoMotif" in taskSet:
                denovoDir=outdir+"/denovoMotif/"
                tasklist[len(tasklist)-1]=chain(tasklist[len(tasklist)-1],CENTDIST.s(peakfile,outdir2,genome))
            else:
                tasklist.append(CENTDIST.s(denovoDir,peakfile,outdir2,genome))
        
        #TSS plot
        if len(taskSet)==0 or "TSSPlot" in taskSet :
            outdir2=outdir+"/TSSPlot/"
            plist=[peakfile]
            tasklist.append(TSSPlot.s(plist,outdir2,genome))
        ##Tag around peak##
        #if len(taskSet)==0 or "TagProfileAroundPeaks" in taskSet :
        #    outdir2=outdir+"/TagProfileAroundPeaks/"
        #    tasklist.append(TagProfileAroundPeaks.s(peakfile,outdir2,inputdir))
        
        ##peak annotation##
        if len(taskSet)==0 or "peakAnnotation" in taskSet:
            outdir2=outdir+"/peakAnnotation/"
            tasklist.append(peakAnnotation.s(peakfile, outdir2, genome))
        
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
       
    return group(tasklist)()
    
def checkCellName(testName, knownName):
    if testName:
        return (testName in knownName) or (knownName in testName)
    else:
        return (False) 


def getMostOccCellName(lines):
    cell_count=dict()
    for cell in settings.known_cells:
        cell_count[cell]=0
    for line in lines:
        comps=line.strip().split()
        fname=os.path.basename(comps[0])
        for cell in cell_count.keys():
            if cell in fname:
                cell_count[cell]+=1
                break
    
    sorted_x = sorted(cell_count.iteritems(), key=operator.itemgetter(1))
    cell_line=sorted_x[len(sorted_x)-1][0]
    return cell_line
        
@task   
def ENCODE_TF_chipseq(peakfile,outdir2,genome):
    mkpath(outdir2)
    cmd="sh "+settings.toolpath+"./peaksetSummary/peaksetSummary.sh "+peakfile+" '"+settings.ENCODEchipseqDIR+"/"+genome+"/*.narrowPeak' "+outdir2
    print cmd
    os.system(cmd)
    cell_line=""
    
    print "peakfile:", peakfile
    print os.path.basename(peakfile)
    filename=outdir2+os.path.basename(peakfile)+".peakset.overlap.top"
    print "file",filename
    try:
        filename=outdir2+os.path.basename(peakfile)+".peakset.overlap.top"
        lines=open(filename).readlines()
        cell_line=getMostOccCellName(lines[0:5])
    except:
        cell_line=""
    return cell_line


@task
def histonePlot(peakfile,outdir2,genome,cellline_used):
    mkpath(outdir2)
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
    os.system(cmd)
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
        if len(taskSet)==0 or "encode_chipseq" in taskSet :
            outdir2=outdir+"/encode_chipseq/"
            if known_match_cell=="":
                known_match_cell=ENCODE_TF_chipseq(peakfile,outdir2,genome)
                print known_match_cell
            else:
                tasklist.append(ENCODE_TF_chipseq.s(peakfile,outdir2,genome))
   
          #encode_histone profile#
        if len(taskSet)==0 or "histonePlot" in taskSet :
            outdir2=outdir+"/histonePlot/"
            if known_match_cell=="":
                known_match_cell=histonePlot(peakfile,outdir2,genome,"")
            else:
                tasklist.append(histonePlot.s(peakfile,outdir2,genome,known_match_cell))
    print known_match_cell
    taskconfig.set("task", "cellline", known_match_cell)
   
    return group(tasklist)()
            
@task
def Pipeline_Processing_task(taskconfigfile,jobid):
    #do the update database
    myjob=Job.objects.get(pk=jobid)
    myjob.status="Processing"
    myjob.save()
    try:
        taskconfig=ConfigParser.ConfigParser()
        taskconfig.readfp(open(taskconfigfile))
        inputdir=taskconfig.get("task", "dataDIR")
        peaklist=glob.glob(inputdir+"/*summits.bed")
        print "running pipeline..."
      #  grouptasks=group(Pipeline_Processing_task_general.s(peaklist,taskconfig),Pipeline_Processing_task_cellline.s(peaklist,taskconfig, jobid))()
        grouptasks=group(Pipeline_Processing_task_general.s(peaklist,taskconfig),Pipeline_Processing_task_cellline.s(peaklist,taskconfig))()
        grouptasks.get(timeout=1000*60*60)
        #do the update database
        
        print "change status"
        myjob=Job.objects.get(pk=jobid)
        myjob.status="Completed"
        myjob.cell_line=taskconfig.get("task","cellline")
        print myjob.cell_line
        myjob.save()
        print myjob.cell_line
    except Exception, e:
        traceback.print_exc()
        print e
        myjob=Job.objects.get(pk=jobid)
        myjob.status="Error"
        myjob.save()

toolpath=os.path.join(peakAnalyzer.settings.ROOT_DIR, '../jobserver').replace('\\','/')

def isRawFile(inputFile):
    try:
        with open(inputFile, 'r') as f:
            lines = len(list(filter(lambda x: x.strip(), f)))
            isLarge=(lines>10000000)
            isMapped=(".fastq" or ".fasta" or ".fq" or ".fa" ) in inputFile
            isRaw= isLarge or isMapped 
    except:
        isRaw=False
    return isRaw

@task
def PeakCalling_task(outdir,jobid):
    #make configure file
    myjob=Job.objects.get(pk=jobid)
    myjob.status="PeakCalling"
    myjob.save()
    outdir2=outdir+ "/peakcalling_result/"
    mkpath(outdir2)
    cfgFileName=outdir2+"/pk.cfg"
    cfgFile=open(cfgFileName,'w')
    
    #copy summits files to outdir2 and rename to *summits.bed 
    moveCmd = "cp {0} " + outdir2 + "{1}"
    
    for sfl in myjob.sampleFiles.split(','):
        print "sfl:",sfl;
        if isRawFile(sfl):
            cfgFile.write(sfl+"\n")
        else:
            #check for sample files
            if sfl.strip(): 
                temp=sfl.split("/")
                basename=temp[len(temp)-1]
                sfl_summits = basename.replace(".bed", ".summits.bed")
                cpCmd=moveCmd.format(sfl, sfl_summits)
                print cpCmd
                os.system(cpCmd)
    if myjob.controlFiles:
            cfgFile.write("===\n")
    for cfl in myjob.controlFiles.split(','):
        print "cfl:",cfl
        if isRawFile(cfl):
            cfgFile.write(cfl+"\n")
        else:
            #check for control files
            if cfl.strip():
                temp=cfl.split("/")
                basename=temp[len(temp)-1]
                cfl_summits = basename.replace(".bed", ".summits.bed")
                cpCmd=moveCmd.format(cfl, cfl_summits)
                print cpCmd
                os.system(cpCmd)
    cfgFile.close()
    
    #check if cfgfile is empty
    tmpFile=open(cfgFileName, "r")
    if tmpFile.read().strip() != "":   
        cmd="python "+toolpath+"/JQpeakCalling.py "+outdir2+"/pk.cfg "+settings.bowtie2_path+" "+settings.bowtie2_index+myjob.ref_genome+" "+settings.genome_length_path+myjob.ref_genome+".txt "+outdir2
        print(cmd)
        os.system(cmd)
    else:
        print("Peak Calling skipped")

@task 
def upload_file(appResults,localfile,dirname,api):
    filetype="image/png"
    if localfile.endswith('.txt') or localfile.endswith('.bed') or localfile.endswith('.html'):
        filetype='text/plain'
    try:
        appResults.uploadFile(api, localfile , os.path.basename(localfile),'/'+dirname+'/', filetype)
    except:
        pass
    
@task
def create_upload_AppResult(outdir,session_id,jobid):   
    session_id=4 #debug 
    session=Session.objects.get(pk=session_id)
    myjob=Job.objects.get(pk=jobid)
    api=session.getBSapi()
    appsession=api.getAppSessionById(str(session.SessionId))
    prjstr=appsession.References[0].Href
    trigger_project=api.getProjectById(prjstr.replace(basespace.settings.version+"/projects/",""))
    appResults = trigger_project.createAppResult(api,str(jobid),myjob.jobtitle,appSessionId='')
    tasklist=list()
    #upload peak calling result
    for localfile in glob.glob(outdir+"/peakcalling_result/*.bed"):
        tasklist.append(upload_file.s(appResults,localfile,'peakcalling_result',api))
    for localfile in glob.glob(outdir+"/peakcalling_result/*.bam"):
        tasklist.append(upload_file.s(appResults,localfile,'peakcalling_result',api))
    for localfile in glob.glob(outdir+"/peakcalling_result/*.xls"):
        tasklist.append(upload_file.s(appResults,localfile,'peakcalling_result',api))
    for localfile in glob.glob(outdir+"/peakcalling_result/*.pdf"):
        tasklist.append(upload_file.s(appResults,localfile,'peakcalling_result',api))
    for localfile in glob.glob(outdir+"/peakcalling_result/*.png"):
        tasklist.append(upload_file.s(appResults,localfile,'peakcalling_result',api))
    upG=group(tasklist)()
    upG.get(timeout=1000*60*60)
    return appResults


def get_immediate_subdirectories(dir1):
    return [name for name in os.listdir(dir1)
            if os.path.isdir(os.path.join(dir1, name))]
@task
def upload_AppResult(outdir,session_id,appResults):  
 #   session_id=5 #debug 
    session=Session.objects.get(pk=session_id)
    api=session.getBSapi()
    tasklist=list()
    dirlist=get_immediate_subdirectories(outdir)
    for dir1 in dirlist:
        for localfile in glob.glob(str(outdir)+"/"+dir1+"/*.png"):
            tasklist.append(upload_file.s(appResults,localfile,dir1,api))
    upG=group(tasklist)()
    upG.get(timeout=1000*60*60)
    
@task
def basespace_Download_PeakCalling_Processing(sfidlist,cfidlist,session_id,outdir,jobid):
    
    #download first
    basespace_download_update_task(sfidlist,cfidlist,session_id,outdir,jobid)
    
    outdir=outdir+str(jobid)#later files have to be in the jobid folder    

    #peak calling
    #raw uploaded files subject to peak calling 
    #else mv to dataDIR and renamed to match *summits.bed
    PeakCalling_task(outdir,jobid)
    
    #upload peak
    appresult_handle=create_upload_AppResult.delay(outdir,session_id,jobid)
    #processing
    myjob=Job.objects.get(pk=jobid)
    outdir2=outdir+"/pipeline_result/"
    mkpath(outdir2)
    taskconfigfile=outdir2+"task.cfg"
    print "config:", taskconfigfile
    configwrite=open(taskconfigfile,'w')
    configwrite.write("[task]\n")
    configwrite.write("dataDIR="+outdir+"/peakcalling_result/"+"\n")
    configwrite.write("cellline="+myjob.cell_line+"\n")
    configwrite.write("alternative_cellline="+myjob.cell_line+"\n")
    configwrite.write("genome="+myjob.ref_genome+"\n")
    configwrite.write("outputDIR="+outdir2+"\n")
    configwrite.close()
    Pipeline_Processing_task(taskconfigfile,jobid)
    upload_AppResult.delay(outdir2,session_id,appresult_handle.get()) 
    