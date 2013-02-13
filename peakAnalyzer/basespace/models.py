'''
Created on 2012-12-14

@author: zhangzhizhuo
'''
from django.db import models
import os
import cPickle as Pickle
from BaseSpacePy.api.BaseSpaceAPI import BaseSpaceAPI
import peakAnalyzer.settings
from django.contrib.auth.models import User
import basespace.settings
_TMP_DIR = os.path.join(peakAnalyzer.settings.ROOT_DIR, 'tmp')

class Session(models.Model):
    SessionId = models.CharField(max_length=200)
    FilePath = models.CharField(max_length=200)
    def getBSapi(self):
        if os.path.exists(self.FilePath):
            f = open(self.FilePath)
            BSapi = Pickle.load(f)
            f.close()
            return BSapi
        else:
            print "Looks like we haven't stored anything for this session yet"
            return None
    def init(self,BSapi):
        self.SessionId=BSapi.appSessionId
        self.FilePath = _TMP_DIR+"/"+BSapi.appSessionId + '.pickle'
        f = open(self.FilePath,'w')
        Pickle.dump(BSapi, f)
        f.close()
    def __unicode__(self):
	return self.SessionId

class User(models.Model):
    Email=models.EmailField()
    BaseSpaceId=models.IntegerField()
    Name=models.CharField(max_length=200)
    def __unicode__(self):
                return self.Name

class Project(models.Model):
	ProjectId=models.IntegerField()
	Name=models.CharField(max_length=50)
	owner=models.ForeignKey(User)
	def __unicode__(self):
		return self.Name

class AppResult(models.Model):
    project=models.ForeignKey(Project)
    Name=models.CharField(max_length=200)
    Detail=models.CharField(max_length=200)
    AppResultId=models.IntegerField()
    def __unicode__(self):
	    return self.Name
    
class Sample(models.Model):
    project=models.ForeignKey(Project)
    Name=models.CharField(max_length=200)
    Detail=models.CharField(max_length=200)
    SampleId=models.IntegerField()
    def __unicode__(self):
        return self.Name
    
class File(models.Model):
    FileId=models.IntegerField()
    Name=models.CharField(max_length=200)
    Path=models.CharField(max_length=400)
    ContentType=models.CharField(max_length=10)
    def __unicode__(self):
        return self.Name