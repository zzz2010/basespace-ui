from django.http import HttpResponse
def aboutus(request):
    return HttpResponse("aboutus")

def howtouse(request):
    return HttpResponse("howtous")