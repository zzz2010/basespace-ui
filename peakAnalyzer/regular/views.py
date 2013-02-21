import datetime, os, sys,  time
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.http import  *
from django.core.files.uploadedfile import UploadedFile
from django.http import Http404
from regular.models import *
from jobserver.models import Job
from django.utils import timezone
import peakAnalyzer.settings
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from jobserver.tasks import *
from django import forms
from peakAnalyzer.settings import MEDIA_ROOT
import json
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,authenticate, login
from basespace.UploadFileHandler import handle_uploaded_file
from django.contrib.auth.models import User

FileTypes={'Extensions':'bam,vcf,fastq,gz,bed,peak'}

@login_required
def hello(request):
    return HttpResponse("hello")
    
#@login_required
#def listUploadedFiles(request, session_id):
#    
#    user        = myAPI.getUserById('current')
#    myuser=User.objects.filter(UserId=user.Id)[0]
#    outdir=peakAnalyzer.settings.MEDIA_ROOT+"/"+user.Email+"/"
#    
#    tmpdir=outdir+"tmp/"
#    os.system("mkdir " + tmpdir)
#    tmp=tmpdir+"uploadedFiles.tmp.txt"
#    listCmd="find " + outdir + " -maxdepth 1 -type f  > " +tmp
#    os.system(listCmd)
#    tmplist= open(tmp, "r")
#    uploadedfiles=list()
#    for line in tmplist:
#        line = line.strip()
#        tmpline=line.split("/")
#        uploadedfiles.append(tmpline[len(tmpline)-1])
#    
#    os.system("rm -r " + tmp )
#    
#    sam = list()
#    bam=list()
#    bed=list()
#    fasta=list()
#    fastq=list()    
#    
#    for f in sorted(uploadedfiles):
#        if ".sam" in f:
#            sam.append(f)
#        if ".bam" in f:
#            bam.append(f)
#        if ".bed" in f:
#            bed.append(f)
#        if ".fasta" in f:
#            fasta.append(f)
#        if ".fastq" in f:
#            fastq.append(f)
#    
#    output={'sam':sam, 'bam':bam, 'bed':bed, 'fasta': fasta,'fastq':fastq}
#    #response_dict={'files':arr}
#    return HttpResponse(json.dumps(output), content_type='application/json')        
#    #return render_to_response('basespace/uploadedlist.html',{'files_list':uploadedfiles,'session_id':session_id})
#    #return HttpResponse(uploadedfiles)

@login_required
@csrf_exempt
def uploadFiles(request):
       
    user        = User.objects.get(username=request.user.username)
    outdir=peakAnalyzer.settings.MEDIA_ROOT+"/"+user.email+"/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    
    if request.method == 'POST':
       filename=handle_uploaded_file(request.FILES['files[]'], outdir)
       err=""
       path=outdir+filename
       prop = [{'name':filename, 'type':"", 'error': err, 'path': path}]
       response_dict={"files":prop}
       return HttpResponse(json.dumps(response_dict), content_type='application/json')    
    
       
@login_required
def listProject(request):
    projects_list=list()
    name=request.user.username
    user        = User.objects.get(username=name)
    projects = UserProject.objects.filter(owner=user)
    if len(projects)==0:
        projectTitle=user.username+"'s Project"
        proj=UserProject(ProjectId=user.id,Name=projectTitle,owner=user)
        proj.save()
    else:
        proj=projects[0]
            
    projects_list.append(proj)   
        
    return render_to_response('regular/index.html', {'user': user,'projects_list':projects_list})


@login_required
@csrf_exempt
def submitJob(request,session_id):
 
    try:
        session=basespace.models.Session.objects.get(pk=session_id)
        myAPI=session.getBSapi()
    except basespace.models.Session.DoesNotExist:
        raise Http404
    samplefids=list()
    controlfids=list()
    cell_line=""
    ref_genome=""
    jobtitle=""
    for postid,postv in request.POST.iteritems():
        if "ctrl" in postid:
            for fid in postv.split(','):    #fid is int if from basespace
                if fid=="":
                    continue
                controlfids.append(fid)
        elif "sample" in postid:
            for fid in postv.split(','):
                if fid=="":
                    continue
                samplefids.append(fid)
        elif "Title" in postid:
            jobtitle=postv
        elif "Genome" in postid:
            ref_genome=postv
        elif "Cell" in postid:
            cell_line=postv
    user        = myAPI.getUserById('current')
    myuser=User.objects.filter(UserId=user.Id)[0]

    outdir=peakAnalyzer.settings.MEDIA_ROOT+"/"+user.Email+"/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    samplefiles=""
    controlfiles=""
    

    myjob=myuser.job_set.create(status="Downloading",ref_genome=ref_genome,cell_line=cell_line,jobtitle=jobtitle,sampleFiles=samplefiles,controlFiles=controlfiles,submitDate=timezone.now())
    #downloadSCFiles(sfidlist, cfidlist,myAPI, outdir, myjob.id)
    basespace_Download_PeakCalling_Processing.delay(samplefids,controlfids,session_id,outdir,myjob.id)
#    return HttpResponse(simplejson.dumps(request.POST))
    return HttpResponse(simplejson.dumps({myjob.id:myjob.jobtitle}), mimetype="application/json");


@csrf_exempt
def loginUser(request):
    state = ""
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state="Logged in"
                session_id=4
                return redirect('/basespace/' + str(session_id) + "/listProject/" )  #debug
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "The username or password entered is incorrect."

    return render_to_response('basespace/login.html',{'state':state})

@csrf_exempt
def logoutUser(request):
    logout(request)
    return redirect('/../peakAnalyzer/basespace/login')

    


