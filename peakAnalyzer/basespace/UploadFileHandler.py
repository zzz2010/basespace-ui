from basespace.models import User, Session
import peakAnalyzer.settings
import basespace

def handle_uploaded_file(f, session_id):
  
    try:
        session=basespace.models.Session.objects.get(pk=session_id)
        myAPI=session.getBSapi()
    except basespace.models.Session.DoesNotExist:
        raise "error"
    user        = myAPI.getUserById('current')
    myuser=User.objects.filter(UserId=user.Id)[0]
    outdir=peakAnalyzer.settings.MEDIA_ROOT+"/"+user.Email+"/"
    outfile=outdir + "name.bed"
    destination = open(outfile, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
