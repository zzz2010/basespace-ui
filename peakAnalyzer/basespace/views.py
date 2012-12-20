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
import jobserver.models
from django.utils import timezone
import basespace.settings
import peakAnalyzer.settings


FileTypes={'Extensions':'bam,vcf,fastq,gz'}
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
    return redirect('basespace.views.listFolders',session_id=session.id)


def listAppResultFiles(request,session_id,ar_id):
    try:
        session=basespace.models.Session.objects.get(pk=session_id)
        myAPI=session.getBSapi()
    except basespace.models.Session.DoesNotExist:
        raise Http404
    ar=myAPI.getAppResultById(ar_id)
    files=ar.getFiles(myAPI,myQp=FileTypes)
    return render_to_response('basespace/filelist.html', {'files_list':files,'session_id':session_id})
        
        
def listSampleFiles(request,session_id,sa_id):
    try:
        session=basespace.models.Session.objects.get(pk=session_id)
        myAPI=session.getBSapi()
    except basespace.models.Session.DoesNotExist:
        raise Http404
    sa=myAPI.getSampleById(sa_id)
    files=sa.getFiles(myAPI,myQp=FileTypes)
    return render_to_response('basespace/filelist.html', {'files_list':files,'session_id':session_id})
        
def listFolders(request,session_id):
    outstr=""
    myProjects=list()
    genome_ids=set()
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
            if hasattr(ar, 'HrefGenome'):
                genome_id=ar.HrefGenome.replace(basespace.settings.version+"/genomes/","")
                genome_ids.add(genome_id)
            if len(my_ar)==0:
                myproject.appresult_set.create(AppResultId=ar.Id,Name=ar.Name)

        samples = singleProject.getSamples(myAPI)
        for sa in samples:
            my_sa=Sample.objects.filter(SampleId=sa.Id)
            if hasattr(sa, 'HrefGenome'):
                genome_id=sa.HrefGenome.replace(basespace.settings.version+"/genomes/","")
                genome_ids.add(genome_id)
            if len(my_sa)==0:
                myproject.sample_set.create(SampleId=sa.Id,Name=sa.Name)
        
    genome_names=list()
    for gid in genome_ids:
        genome_names.append(myAPI.getGenomeById(gid).Build) 
        
    return render_to_response('basespace/index.html', {'genome_names':"|".join(genome_names),'user': myuser,'projects_list':projects_list,'session_id':str(session_id)})

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
    for postid,postv in request.POST:
        if "cb__" in postid:
            fid=postid.split("__")[1]
            if postv=="checked":
                controlfids.append(fid)
            else:
                samplefids.append(fid)
        elif "title" in postid:
            jobtitle=postv
        elif "genome" in postid:
            ref_genome=postv
    user        = myAPI.getUserById('current')
    myuser=User.objects.filter(UserId=user.Id)[0]
    
    outdir=peakAnalyzer.settings.MEDIA_ROOT+"/"+user.Email+"/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    samplefiles=""
    controlfiles=""
    for fid in samplefids:
        f = myAPI.getFileById(fid)
        outf=outdir+f.Name
        f.downloadFile(myAPI,outdir)
        if samplefiles!="":
            samplefiles+=","
        samplefiles+=outf

    for fid in controlfids:
        f = myAPI.getFileById(fid)
        outf=outdir+f.Name
        f.downloadFile(myAPI,outdir)
        if controlfiles!="":
            controlfiles+=","
        controlfiles+=outf
    myjob=myuser.job_set.create(status="Downloading",ref_genome=ref_genome,cell_line=cell_line,jobtitle=jobtitle,sampleFiles=samplefiles,controlFiles=controlfiles,submitDate=timezone.now())
    return HttpResponse(simplejson.dumps({myjob.id:myjob.jobtitle}), mimetype="application/json");

def demo(request,user_id):
    u=p = get_object_or_404(User, pk=user_id)
    return render_to_response('basespace/demo.html', {'user': u})


    


