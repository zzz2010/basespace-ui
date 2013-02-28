import datetime, os, sys,  time,traceback
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import redirect
from jobserver_regular.models import RegularJob
from django.utils import timezone
import peakAnalyzer.settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from jobserver_regular.tasks import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def listjob(request,user_id):
    u=get_object_or_404(User, pk=user_id)
    css=dict()
    css["Downloading"]=""
    css["Data_Ready"]="info"
    css["PeakCalling"]="info"
    css["Processing"]="warning"
    css["Completed"]="success"
    css["Error"]="error"
    return render_to_response('jobserver_regular/joblist.html', {'jobs_list':u.regularjob_set.all(),'css':css})

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]

def CENTDIST_result(dir1):
    myTab=os.path.basename(dir1)
#    html_str="<script type='text/javascript'>$('#tab__"+myTab+"').click(function () {"
#    html_str+= "$(this).load('http://genome.ddns.comp.nus.edu.sg/~chipseq/webseqtools2/TASKS/Motif_Enrichment/viewresult.php?rundir="+dir1+"');"
#    #html_str="<script type='text/javascript'>window.alert('hello');</script>"
#    html_str+="});</script>\n"
    html_str="<div class='tab-pane' id='"+os.path.basename(dir1)+"""'><iframe id="iFrame1" name="iFrame1" 
    width="100%" onload="this.height=iFrame1.document.body.scrollHeight" frameborder="0" 
    src='http://genome.ddns.comp.nus.edu.sg/~chipseq/webseqtools2/TASKS/Motif_Enrichment/viewresult_peakAnalyzer.php?rundir="""+dir1+"'></iframe></div>\n"
    
    return html_str

def GREAT_result(dir1):
    myTab=os.path.basename(dir1)
    html_str="<div class='tab-pane' id='"+os.path.basename(dir1)+"'>"+'<script> $(document).ready( function () {\
$(\'.table.table-striped.table-bordered.table-condensed\').dataTable({\
            "sDom": "<\'row\'<\'span6\'l><\'span6\'f>r>t<\'row\'<\'span6\'i><\'span6\'p>>",\
            "sPaginationType": "bootstrap",\
            "aoColumns": [{ "sType": \'string\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'percent\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'percent\' },]\
           }); } );</script>'
    
    filelist=os.listdir(dir1)
    table=''
    for f in filelist:
        if 'html' in f:
            try:
                table=open(dir1 +"/"+f,'r').read()
            except:
                print "file format error"
    html_str=html_str+table + '</div>\n'
    return html_str

def denovoMotif_result(dir1):
    myTab=os.path.basename(dir1)
    html_str='<div class="tab-pane" id="'+os.path.basename(dir1)+'">'
     
    filelist=os.listdir(dir1)
    table=''
    for f in filelist:
        if 'html' in f:
            try:
                table=open(dir1 +"/"+f,'r').read()
            except:
                print "file format error"
    pwm_result=dir1.replace("/home/chipseq/basespace/peakAnalyzer/peakAnalyzer/../", "/peakAnalyzer/") + "/SEME_clust.pwm"
    html_button='<a style="padding-left:130px padding-top:50px" id="download" href="'+pwm_result +'"><button class="btn btn-primary" type="submit">Download PWM Result</button></a>'
    
    html_str=html_str+table+html_button+'</div>\n'
    
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
    
    html_str+="</div>\n"
    return html_str


@login_required      
def viewresult(request,job_id):
    job=get_object_or_404(RegularJob, pk=job_id)
    result_dir=peakAnalyzer.settings.MEDIA_ROOT+"/"+job.user.email+"/"+str(job.id)+"/pipeline_result/"
    result_list=get_immediate_subdirectories(result_dir)
    content_html=" "
    for dir1 in result_list:
        if "CENTDIST" in dir1:
            content_html+=CENTDIST_result(str(result_dir)+"/"+str(dir1))
        elif "denovo" in dir1:
            content_html+=denovoMotif_result(str(result_dir)+"/"+str(dir1))
        elif "GREAT" in dir1:
            content_html+=GREAT_result(str(result_dir)+"/"+str(dir1))
        
        else:
            content_html+=resultfolder_html(str(result_dir)+"/"+str(dir1))
    return render_to_response('jobserver/viewresult.html', {'result_list':result_list,'job':job,'content_html':content_html})