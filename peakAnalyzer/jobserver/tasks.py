'''
Created on 2012-12-21

@author: zhangzhizhuo
'''
from celery import task
from basespace.models import Project,User,AppResult,Sample,File,Session
import os
from jobserver.models import Job
from celery import chord,group,chain

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

@task
def basespace_Download_PeakCalling_Processing(sfidlist,cfidlist,session_id,outdir,jobid):
    #download first
    basespace_download_update_task(sfidlist,cfidlist,session_id,outdir,jobid)
    
    #peak calling
    
    
    #processing 
    