'''
Created on Feb 20, 2013

@author: soke may
'''
from django.db import models
import os
import peakAnalyzer.settings
from django.contrib.auth.models import User

class Project(models.Model):
    ProjectId=models.IntegerField()
    Name=models.CharField(max_length=50)
    owner=models.ForeignKey(User)
    def __unicode__(self):
        return self.Name
