import basespace
import datetime, os, sys,  time
from django.utils import simplejson
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponse
from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
from django.http import Http404
from django.shortcuts import redirect
from basespace.models import Project,User,AppResult,Sample,File
import basespace.settings



FileTypes={'Extensions':'bam,vcf'}
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
    return redirect('basespace.views.listFiles',session_id=session.id)

def listFiles(request,session_id):
    outstr=""
    myProjects=list()
    try:
        session=basespace.models.Session.objects.get(pk=session_id)
        myAPI=session.getBSapi()
        appsession=myAPI.getAppSessionById(str(session.SessionId))
        prjstr=appsession.References.Href
        if "project" in prjstr:
            trigger_project=myAPI.getProjectById(prjstr.replace(basespace.settings.version+"/projects/",""))
            myProjects.append(trigger_project)
    except basespace.models.Session.DoesNotExist:
        raise Http404
    if len(myProjects)==0:
        user        = myAPI.getUserById('current')
        if len(User.objects.filter(UserId=user.Id))==0:
            myuser=basespace.models.User(UserId=user.Id,Email=user.Email,Name=user.Name)
            myuser.save()
        else:
            myuser=User.objects.filter(UserId=user.Id)[0]
        myProjects   = myAPI.getProjectByUser('current')
    for singleProject in myProjects:
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
        my_sa=Sample.objects.filter(AppResultId=sa.Id)
        if len(my_sa)==0:
            myproject.sample_set.create(SampleId=ar.Id,Name=ar.Name)

        files = sa.getFiles(myAPI,myQp=FileTypes)
        for f in files:
            my_file=File.objects.filter(FileId=f.Id)
            if len(my_file)==0:
                my_file=File(Name=f.Name,FileId=f.Id,Path=f.Path)
            outstr+="<p>"+str(f)
            
    return HttpResponse(outstr)


