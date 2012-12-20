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
from inspect import getmodule
from multiprocessing import Pool

FileTypes={'Extensions':'bam,vcf,fastq,gz'}




def async(decorated):
    r'''Wraps a top-level function around an asynchronous dispatcher.

        when the decorated function is called, a task is submitted to a
        process pool, and a future object is returned, providing access to an
        eventual return value.

        The future object has a blocking get() method to access the task
        result: it will return immediately if the job is already done, or block
        until it completes.

        This decorator won't work on methods, due to limitations in Python's
        pickling machinery (in principle methods could be made pickleable, but
        good luck on that).
    '''
    # Keeps the original function visible from the module global namespace,
    # under a name consistent to its __name__ attribute. This is necessary for
    # the multiprocessing pickling machinery to work properly.
    module = getmodule(decorated)
    decorated.__name__ += '_original'
    setattr(module, decorated.__name__, decorated)

    def send(*args, **opts):
        return async.pool.apply_async(decorated, args, opts)

    return send

async.pool = Pool(4)

##download files routine
def downloadFiles(fidlist,api,outdir):
    outfiles=""
    for fid in fidlist:
        f = api.getFileById(fid)
        f.downloadFile(api,outdir)
        if outfiles!="":
            outfiles+=","
        outfiles+=outdir+f.Name
            
    
@async
def downloadSCFiles(sfidlist,cfidlist,api,outdir,jobid):
    myjob=Job.objects.get(pk=jobid)
    sfiles=downloadFiles(sfidlist,api,outdir)
    cfiles=downloadFiles(cfidlist,api,outdir)
    myjob.sampleFiles=sfiles
    myjob.controlFiles=cfiles
    myjob.status="Downloaded"
    myjob.save()#update database
    
    
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
    genome_name=""
    ar=myAPI.getAppResultById(ar_id)
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
    if hasattr(sa, 'HrefGenome'):
        genome_id=sa.HrefGenome.replace(basespace.settings.version+"/genomes/","")
        genome_name=myAPI.getGenomeById(genome_id).Build
    files=sa.getFiles(myAPI,myQp=FileTypes)
    return render_to_response('basespace/filelist.html', {'genome_name':genome_name,'files_list':files,'session_id':session_id})
        
def listFolders(request,session_id):
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
                myproject.appresult_set.create(AppResultId=ar.Id,Name=ar.Name)

        samples = singleProject.getSamples(myAPI)
        for sa in samples:
            my_sa=Sample.objects.filter(SampleId=sa.Id)

            if len(my_sa)==0:
                myproject.sample_set.create(SampleId=sa.Id,Name=sa.Name)
        

        
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
    sfidlist=list()
    cfidlist=list()
    outdir=peakAnalyzer.settings.MEDIA_ROOT+"/"+user.Email+"/"
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    samplefiles=""
    controlfiles=""
    for fid in samplefids:
        sfidlist.append(fid)
        if samplefiles!="":
            samplefiles+=","
        samplefiles+=fid

    for fid in controlfids:
        cfidlist.append(fid)
        if controlfiles!="":
            controlfiles+=","
        controlfiles+=fid
    myjob=myuser.job_set.create(status="Downloading",ref_genome=ref_genome,cell_line=cell_line,jobtitle=jobtitle,sampleFiles=samplefiles,controlFiles=controlfiles,submitDate=timezone.now())
    downloadSCFiles(sfidlist, cfidlist,myAPI, outdir, myjob.id)
    
    return HttpResponse(simplejson.dumps(request.POST))
 #   return HttpResponse(simplejson.dumps({myjob.id:myjob.jobtitle}), mimetype="application/json");

def demo(request,user_id):
    u=p = get_object_or_404(User, pk=user_id)
    return render_to_response('basespace/demo.html', {'user': u})


    


