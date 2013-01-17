import basespace
import datetime, os, sys,  time
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.http import  *
from django.core.files.uploadedfile import UploadedFile
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
from basespace.UploadFileHandler import handle_uploaded_file
from django import forms
from peakAnalyzer.settings import MEDIA_ROOT

FileTypes={'Extensions':'bam,vcf,fastq,gz,bed,peak'}

class UploadFileForm(forms.Form):
   # title = forms.CharField(max_length=50)
    #file  = forms.FileField()
    file = forms.Field(widget=forms.FileInput, required=True)

class SimpleFileForm(forms.Form):
    file = forms.Field(widget=forms.FileInput, required=False)

# Create your views here.
def createSession(request):
    if 'appsessionuri' not in request.GET:
        return HttpResponse("Hello!")
    AppSessionId=request.GET['appsessionuri'].replace(basespace.settings.version+"/appsessions/",'')
    BSapi = BaseSpaceAPI(basespace.settings.client_key, basespace.settings.client_secret, basespace.settings.BaseSpaceUrl, basespace.settings.version, AppSessionId)
    BSapi.updatePrivileges(request.GET['authorization_code'])
    myToken = BSapi.getAccessToken()
    print myToken
    myAPI= BaseSpaceAPI(basespace.settings.client_key, basespace.settings.client_secret, basespace.settings.BaseSpaceUrl, basespace.settings.version, AppSessionId, AccessToken=myToken)
    
    session=basespace.models.Session()
    session.init(myAPI)
    session.save()
    return redirect('basespace.views.listProject',session_id=session.id)


def listAppResultFiles(request,session_id,ar_id):
    try:
        session=basespace.models.Session.objects.get(pk=session_id)
        myAPI=session.getBSapi()
    except basespace.models.Session.DoesNotExist:
        raise Http404
    genome_name=""
    ar=myAPI.getAppResultById(ar_id)
    myar=AppResult.objects.get(AppResultId=ar_id)
    myar.Detail=ar.Description
    myar.save()
    genome_name="-"
    if hasattr(ar, 'HrefGenome'):
        genome_id=ar.HrefGenome.replace(basespace.settings.version+"/genomes/","")
        genome_name=myAPI.getGenomeById(genome_id).Build
    files=ar.getFiles(myAPI,myQp=FileTypes)
    return render_to_response('basespace/filelist.html', {'genome_name':genome_name,'files_list':files,'session_id':session_id})
        
        
def listSampleFiles(request,session_id,sa_id):
    try:
        session=basespace.models.Session.objects.get(pk=session_id)
        myAPI=session.getBSapi()
    except basespace.models.Session.DoesNotExist:
        raise Http404
    genome_name=""
    sa=myAPI.getSampleById(sa_id)
    mysa=Sample.objects.get(SampleId=sa_id)
    mysa.Detail=sa.ExperimentName+","+str(sa.Read1)+"-"+str(sa.Read2)
    mysa.save()
    genome_name="-"
    if hasattr(sa, 'HrefGenome'):
        genome_id=sa.HrefGenome.replace(basespace.settings.version+"/genomes/","")
        genome_name=myAPI.getGenomeById(genome_id).Build
    files=sa.getFiles(myAPI,myQp=FileTypes)
    return render_to_response('basespace/filelist.html', {'genome_name':genome_name,'files_list':files,'session_id':session_id})

@csrf_exempt
def listUploadedFiles(request, session_id):
    try:
        session=basespace.models.Session.objects.get(pk=session_id)
        myAPI=session.getBSapi()
    except basespace.models.Session.DoesNotExist:
            raise Http404
 
#    if request.method== 'POST':
#        if 'file' in request.FILES:
#            file = request.FILES['file']
#
#            # Other data on the request.FILES dictionary:
#            #   filesize = len(file['content'])
#            #   filetype = file['content-type']
#
#            filename = file['filename']
#
#            fd = open('%s/%s' % (MEDIA_ROOT, filename), 'wb')
#            fd.write(file['content'])
#            fd.close()
#
#            return HttpResponseRedirect(' upload_success.html')
#    else:
#        # display the form
#        form = SimpleFileForm()
#        return render_to_response('basespace/fileupload.html', { 'form': form })
 
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        values = form.errors
        if form.is_valid():
            #filenames=handle_uploaded_file(request.FILES['file'], session_id)
            
#            values.sort()
#            html = []
#            for k, v in values:
#                html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
#            return HttpResponse('<table>%s</table>' % '\n'.join(html))
            return HttpResponse("file uploaded!")
        else:
            return HttpResponse(values)
    else:
        form = UploadFileForm()
    return render_to_response('basespace/fileupload.html', {'session_id':session_id,'form': form})
    #return HttpResponse("uploaded")
   #return render_to_response('basespace/index.html', {'session_id':session_id})
        
def listProject(request,session_id):
    outstr=""
    myProjects=list()
    try:
        session=basespace.models.Session.objects.get(pk=session_id)
        myAPI=session.getBSapi()
        appsession=myAPI.getAppSessionById(str(session.SessionId))
        prjstr=appsession.References[0].Href
        if "project" in prjstr:
            trigger_project=myAPI.getProjectById(prjstr.replace(basespace.settings.version+"/projects/",""))
            myProjects.append(trigger_project)
    except basespace.models.Session.DoesNotExist:
        raise Http404
    
    user        = myAPI.getUserById('current')
    if len(User.objects.filter(UserId=user.Id))==0:
        myuser=basespace.models.User(UserId=user.Id,Email=user.Email,Name=user.Name)
        myuser.save()
    else:
        myuser=User.objects.filter(UserId=user.Id)[0]
    if len(myProjects)==0:
        myProjects   = myAPI.getProjectByUser('current')
    projects_list=list()
    for singleProject in myProjects:
        outstr+="<H>"+singleProject.Name+"</H>"
        if len(Project.objects.filter(ProjectId=singleProject.Id))==0:
            myproject=myuser.project_set.create(ProjectId=singleProject.Id,Name=singleProject.Name)
        else:
            myproject=Project.objects.filter(ProjectId=singleProject.Id)[0] 
        projects_list.append(myproject)   
        appResults=singleProject.getAppResults(myAPI)
        for ar in appResults:
            my_ar=AppResult.objects.filter(AppResultId=ar.Id)

            if len(my_ar)==0:
                myproject.appresult_set.create(AppResultId=ar.Id,Name=ar.Name,Detail=ar.Id)

        samples = singleProject.getSamples(myAPI)
        for sa in samples:
            my_sa=Sample.objects.filter(SampleId=sa.Id)

            if len(my_sa)==0:
                myproject.sample_set.create(SampleId=sa.Id,Name=sa.Name,Detail=sa.Id)
        

        
    return render_to_response('basespace/index.html', {'user': myuser,'projects_list':projects_list,'session_id':str(session_id)})

def listFiles(request,session_id):
    outstr=""
    myProjects=list()
    try:
        session=basespace.models.Session.objects.get(pk=session_id)
        myAPI=session.getBSapi()
        appsession=myAPI.getAppSessionById(str(session.SessionId))
        prjstr=appsession.References[0].Href
        if "project" in prjstr:
            trigger_project=myAPI.getProjectById(prjstr.replace(basespace.settings.version+"/projects/",""))
            myProjects.append(trigger_project)
    except basespace.models.Session.DoesNotExist:
        raise Http404
    
    user        = myAPI.getUserById('current')
    if len(User.objects.filter(UserId=user.Id))==0:
        myuser=basespace.models.User(UserId=user.Id,Email=user.Email,Name=user.Name)
        myuser.save()
    else:
        myuser=User.objects.filter(UserId=user.Id)[0]
    if len(myProjects)==0:
        myProjects   = myAPI.getProjectByUser('current')
    for singleProject in myProjects:
        outstr+="<H>"+singleProject.Name+"</H>"
        if len(Project.objects.filter(ProjectId=singleProject.Id))==0:
            myproject=myuser.project_set.create(ProjectId=singleProject.Id,Name=singleProject.Name)
        else:
            myproject=Project.objects.filter(ProjectId=singleProject.Id)[0]	
        appResults=singleProject.getAppResults(myAPI)
        for ar in appResults:
            my_ar=AppResult.objects.filter(AppResultId=ar.Id)
            if len(my_ar)==0:
                myproject.appresult_set.create(AppResultId=ar.Id,Name=ar.Name)
            files = ar.getFiles(myAPI,myQp=FileTypes)
            for f in files:
                my_file=File.objects.filter(FileId=f.Id)
                if len(my_file)==0:
                    my_file=File(Name=f.Name,FileId=f.Id,Path=f.Path)
                outstr+="<p>"+str(f)
        samples = singleProject.getSamples(myAPI)
        for sa in samples:
            my_sa=Sample.objects.filter(SampleId=sa.Id)
            if len(my_sa)==0:
                myproject.sample_set.create(SampleId=ar.Id,Name=ar.Name)
    
            files = sa.getFiles(myAPI,myQp=FileTypes)
            for f in files:
                my_file=File.objects.filter(FileId=f.Id)
                if len(my_file)==0:
                    my_file=File(Name=f.Name,FileId=f.Id,Path=f.Path)
                outstr+="<p>"+str(f)
            
    return HttpResponse(outstr)


    
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
            for fid in postv.split(','):
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

def demo(request,user_id):
    u= get_object_or_404(User, pk=user_id)
    return render_to_response('basespace/demo.html', {'user': u})


    


