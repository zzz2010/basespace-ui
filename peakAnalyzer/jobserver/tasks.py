'''
Created on 2012-12-21

@author: zhangzhizhuo
'''
from celery import task
from basespace.models import Project,User,AppResult,Sample,File,Session
import os
from celery import chord,group,chain

@task
def downloadFile(fid,session_id,outFileName):
    session=Session.objects.get(pk=session_id)
    api=session.getBSapi()
    api.fileDownload(fid,os.path.dirname(outFileName),os.path.basename(outFileName))
    
@task
def basespace_download_update_task(sfidlist,cfidlist,session_id,outdir,jobid):
    session=Session.objects.get(pk=session_id)
    api=session.getBSapi()
    s_outfiles=list()
    c_outfiles=list()
    downloadGroup=group()
    for fid in sfidlist:
        f = api.getFileById(fid)
        outfile=outdir+f.Name
        s_outfiles.append(outfile)
       # downloadGroup.
    for fid in sfidlist:
        f = api.getFileById(fid)
        outfile=outdir+f.Name
        c_outfiles.append(outfile)
        
@task()
def add(x, y):
    return x + y

@task
def basespace_Download_PeakCalling_Processing(sfidlist,cfidlist,session_id,outdir,jobid):
    #download first
    a=1
    
    #peak calling
    
    
    #processing 
    