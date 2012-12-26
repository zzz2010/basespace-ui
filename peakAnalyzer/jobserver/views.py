import basespace
import datetime, os, sys,  time
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse
from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
from django.http import Http404
from django.shortcuts import redirect
from basespace.models import Project,User,AppResult,Sample,File
from jobserver.models import Job
from django.utils import timezone
import basespace.settings
import peakAnalyzer.settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from jobserver.tasks import *

# Create your views here.
def listjob(request,user_id):
    u=get_object_or_404(User, pk=user_id)
    css=dict()
    css["Downloading"]=""
    css["Data_Ready"]="info"
    css["PeakCalling"]="info"
    css["Analyzing"]="warning"
    css["Completed"]="success"
    css["Error"]="error"
    return render_to_response('jobserver/joblist.html', {'jobs_list':u.job_set.all(),'css':css})

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def CENTDIST_result(dir1):
    myTab=os.path.basename(dir1)
    html_str="<script type='text/javascript'>$('#"+myTab+"').click(function (e) {"
    html_str+= "$(this).load(http://genome.ddns.comp.nus.edu.sg/~chipseq/webseqtools2/TASKS/Motif_Enrichment/viewresult.php?rundir="+dir1+")})</script>"
    html_str+="<div class='tab-pane' id='"+os.path.basename(dir1)+"'></div>"
    
    return html_str
    
def resultfolder_html(dir1):
    html_str="<div class='tab-pane' id='"+os.path.basename(dir1)+"'>"
    #show image first
    types = ('*.jpg', '*.png','*.bmp') 
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(str(dir1)+"/"+files))
    for fl in files_grabbed:
        weburl=fl.replace(peakAnalyzer.settings.MEDIA_ROOT,"/peakAnalyzer"+peakAnalyzer.settings.MEDIA_URL)
        html_str+="<div><a  href='"+weburl+"' target=_blank><img src='"+weburl+"' width='400'/><br>"+os.path.basename(fl)+"</a></div>"
    #show file download link with accept format
    
    html_str+="</div>"
    return html_str
    
def viewresult(request,job_id):
    job=get_object_or_404(Job, pk=job_id)
    result_dir=peakAnalyzer.settings.MEDIA_ROOT+"/"+job.user.Email+"/"+str(job.id)+"/pipeline_result/"
    result_list=get_immediate_subdirectories(result_dir)
    content_html=" "
    for dir1 in result_list:
        content_html+=resultfolder_html(str(result_dir)+"/"+str(dir1))
    return render_to_response('jobserver/viewresult.html', {'result_list':result_list,'job':job,'content_html':content_html})