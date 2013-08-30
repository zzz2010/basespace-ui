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
from jobserver_regular.tasks import mkpath

# Create your views here.
def listjob(request,user_id):
    u=get_object_or_404(User, pk=user_id)
    css=dict()
    css["Downloading"]=""
    css["Data_Ready"]="info"
    css["Read Mapping"]="info"
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

    #html_str="<div class='tab-pane' id='"+os.path.basename(dir1)+"""'><iframe id="iFrame1" name="iFrame1" 
    #width="100%" onload="this.height=iFrame1.document.body.scrollHeight" frameborder="0" 
    #src='/~sokemay/Motif_Enrichment/viewresult_peakAnalyzer.php?rundir="""+dir1+"'></iframe></div>\n"  #onload='this.height=iFrame1.document.body.scrollHeight'
    html_str="<div class='tab-pane' id='"+os.path.basename(dir1)+"'><object id='iFrame1' name='iFrame1'  width='100%'  height='800' frameborder='0'  data='/~sokemay/Motif_Enrichment/viewresult_peakAnalyzer.php?rundir="+dir1+"' type='text/html'></object></div>\n"
    
    
    return html_str

def GREAT_result(dir1):
    myTab=os.path.basename(dir1)
    html_str="<div class='tab-pane' id='"+os.path.basename(dir1)+"'>"+'<script> $(document).ready( function () {\
$(\'.table.table-striped.table-bordered.table-condensed\').dataTable({\
           "aaSorting": [[ 1, "asc" ], [7,"asc"]],\
            "sDom": "<\'row\'<\'span6\'l><\'span6\'f>r>t<\'row\'<\'span6\'i><\'span6\'p>>",\
            "sPaginationType": "bootstrap",\
             "aoColumns": [{ "sType": \'string\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'percent\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'numeric\' },{ "sType": \'percent\' },]\
           }); } );</script>'
    
    htmlfile=glob.glob(dir1+"/*.html")
    if htmlfile:
        table=open(htmlfile[0],'r').read()
    else:
        table=''
    #DEBUG URL
    try:
        fileurl=glob.glob(dir1+"/*.txt")[0]  #renamed great output to xls filetype
        fileurl=fileurl.replace("/home/sokemay/basespace/basespace-ui/basespace-ui/peakAnalyzer/", "../../../")
    except:
        fileurl=''
    download_btn='<div style="padding-bottom:20px" id="great_download_btn"><a target="_blank" href="'+fileurl+'"><button class="btn btn-success">Download Peak Gene Associations <span class="icon-download icon-white"></button></span></a></div>'
    html_str=html_str+download_btn+table + '</div>\n'
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
    pwm_result=dir1.replace("/home/sokemay/basespace/basespace-ui/basespace-ui/peakAnalyzer/", "../../../") + "/SEME_clust.pwm"
    html_button='<a target="_blank" style="padding-bottom:150px" id="download" href="'+pwm_result +'"><button class="btn btn-primary" type="submit">Download PWM Result <span class="icon-download icon-white"></span></button></a>'
    
    html_str=html_str+html_button+ table+'</div>\n'
    
    return html_str

def resultfolder_html(dir1):
    html_str="<div class='tab-pane' id='"+os.path.basename(dir1)+"'>"
    #show image first
    types = ('*.jpg', '*.png','*.bmp') 
    files_grabbed = []
    json_file=[]
    
    json_file.extend(glob.glob(str(dir1)+"/*.json"))
    hasJ=(len(json_file)>0)
    for fl in json_file:
        #jsfile=(str(dir1)+"/test1.json").replace(peakAnalyzer.settings.MEDIA_ROOT,"/peakAnalyzer"+peakAnalyzer.settings.MEDIA_URL)
        jsfile=fl.replace(peakAnalyzer.settings.MEDIA_ROOT,"/peakAnalyzer"+peakAnalyzer.settings.MEDIA_URL);
        wid='800'
        html_str+="<script type=\"text/javascript\">\n$(document).ready(function() {$.getJSON(\'"+jsfile+"\', function(data) {"
        if 'repeat' in dir1 or 'peakAnno' in dir1:
            html_str+="data.series[0].dataLabels.formatter=eval('('+data.series[0].dataLabels.formatter+')');"
            if 'repeat' in dir1:
                wid='1200'
        html_str+="var chart = new Highcharts.Chart(data);});})\n</script>\n"
        html_str+="<div id=\""+os.path.basename(jsfile).split('.json')[0]+"\" style=\"width: "+wid+"px\"></div>\n"
    
    #show file download link with accept format
    if not hasJ:
        for files in types:
            files_grabbed.extend(glob.glob(str(dir1)+"/"+files))
        for fl in files_grabbed:
            weburl=fl.replace(peakAnalyzer.settings.MEDIA_ROOT,"/peakAnalyzer"+peakAnalyzer.settings.MEDIA_URL)
            html_str+="<div><a  href='"+weburl+"' target=_blank><img src='"+weburl+"' width='800'/><br>"+os.path.basename(fl)+"</a></div>"
        
    html_str+="</div>\n"
    return html_str

def jobinfo_html(job, result_dir):
    toolpath=os.path.join(peakAnalyzer.settings.ROOT_DIR, '../jobserver_regular').replace('\\','/')
    outdir=result_dir+'/job_info/'
    mkpath(outdir)
    job_desc_out=outdir+"jobdescription.html"
    
    #add alt cellline
    try:
        alt_cl=open(result_dir+"/pipeline_result/detected_cl.txt").readline()
    except:
        alt_cl=''
    
   # os.system("rm " + job_desc_out)
    cmd="python "+toolpath+"/generateJobInfoHtml.py '" + job.jobtitle + "' '" + job.ref_genome+ "' '" + job.cell_line + "' '"+alt_cl +"' '" + job.sampleFiles+ "' '" + job.controlFiles + "' " +result_dir+ " " + job_desc_out + ' '+toolpath
#    cmd="python "+toolpath+"/generateJobInfoHtml.py " + str(job.id) +" "+result_dir+ " " +job_desc_out
    print cmd
    os.system(cmd)
    try:
        job_desc=open(job_desc_out).read()
    except:
        job_desc=''
    html_str="<div class='tab-pane active' id='job_info'>" +job_desc+ "</div>"
    
    
    return html_str

@login_required      
def viewresult(request,job_id):
    user        = User.objects.get(username=request.user.username) 
    job=get_object_or_404(RegularJob, pk=job_id)
        
    if job.user==user:
        result_dir=peakAnalyzer.settings.MEDIA_ROOT+"/"+job.user.email+"/"+str(job.id)+"/pipeline_result/"
        result_list=get_immediate_subdirectories(result_dir)

        #generate job info html
        job_info_html=jobinfo_html(job, str(result_dir)+"../")

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
        return render_to_response('jobserver/viewresult.html', {'result_list':result_list,'job':job,'content_html':content_html, 'job_info':job_info_html})
            
    else:
        return render_to_response('jobserver/view_result_not_authorized.html')

    
def viewResultDemo(request):
    job_id='176'
    job=get_object_or_404(RegularJob, pk=job_id)
    result_dir=peakAnalyzer.settings.MEDIA_ROOT+"/yrjie0@gmail.com/176/pipeline_result/"
    result_list=get_immediate_subdirectories(result_dir)

    #generate job info html
    job_info_html=jobinfo_html(job, str(result_dir)+"../")

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
    return render_to_response('jobserver/viewresult.html', {'result_list':result_list,'job':job,'content_html':content_html, 'job_info':job_info_html})
