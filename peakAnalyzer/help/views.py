from django.http import HttpResponse
from django.shortcuts import render_to_response
def aboutus(request):
    return render_to_response("help/aboutus.html")

def howtouse(request):
    return render_to_response("help/usage.html")

def helpDoc(request):
    return render_to_response("help/helpdoc.html")