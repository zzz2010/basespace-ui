
from django.core.files.uploadedfile import UploadedFile

def handle_uploaded_file(f, outdir):
  
   
    wrappedFile = UploadedFile(f)
    filename=wrappedFile.name
    outfile=outdir + filename
    destination = open(outfile, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    
    return filename
