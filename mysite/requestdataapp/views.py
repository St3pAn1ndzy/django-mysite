from django.core.files.storage import FileSystemStorage
from django.http.request import HttpRequest
from django.shortcuts import render


def handle_file_upload(request: HttpRequest):
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        file_size = myfile.size
        if file_size < 1024:
            file_name = fs.save(myfile.name, myfile)
            print('saved file', file_name)
        else:
            print('file over 1024 Mb. File size:', file_size)

    return render(request, 'requestdataapp/file-upload.html')
