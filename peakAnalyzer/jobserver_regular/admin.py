from jobserver_regular.models import *
from django.contrib import admin



class JobAdmin(admin.ModelAdmin):
    # ...
    list_display = ('jobtitle', 'submitDate','status','user')
    
    
admin.site.register(RegularJob,JobAdmin)