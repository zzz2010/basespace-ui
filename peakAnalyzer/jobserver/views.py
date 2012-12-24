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
   