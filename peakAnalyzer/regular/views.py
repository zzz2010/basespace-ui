'''
Created on Feb 20, 2013

@author: soke may
'''
import basespace
import datetime, os, sys,  time
from django.utils import simplejson
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.http import  *
from django.core.files.uploadedfile import UploadedFile
from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
from django.http import Http404
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
import json
from django.utils import simplejson
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
def hello(request):
    return HttpResponse("Hello")