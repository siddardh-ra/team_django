from django.shortcuts import render
from .models import *

# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
import os
from django.contrib.staticfiles.storage import staticfiles_storage


def upload_images(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to = '/accounts/login')
    else:

        batches = Batch.objects.filter(created_by = request.user)

        return render(request,template_name = 'batch_upload/create.html',context={'batches':batches})


def view_batches(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to = '/accounts/login')
    else:

        batches = Batch.objects.filter(created_by = request.user)

        return render(request,template_name = 'batch_upload/view.html',context={'batches':batches})


def process_upload(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to = '/accounts/login')
    else:

        data = request.POST
        print(request.FILES['batch'].__dict__)

        new_batch = Batch()
        new_batch.name = data["batch_name"]
        new_batch.project = data["project_name"]
        new_batch.description = data["description"]

        new_batch.created_by = request.user

        path = os.path.join('static',request.user.username,data['batch_name'])
        try:
            os.makedirs(path)
        except Exception as e:
            pass

        zip_path = path+"/"+request.FILES['batch'].name
        extracted_path = path+"/extracted/"

        with open(zip_path,'wb') as f:
            f.write(request.FILES['batch'].read())

        import zipfile

        try:
            os.makedirs(path+'/extracted/')
        except:
            pass

        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(path+"/extracted/")
        files=[]
        for r, d, f in os.walk(extracted_path):
            for f in f:
                if f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.png'):
                    files.append(os.path.join(r, f))

        # for f in files:
        #     print(f)
        # files = [f for f in os.listdir(extracted_path+request.FILES['batch'].name+"/") if f.endswith('.jpeg') or f.endswith('.jpg') or f.endswith('.png')]
        print(files,len(files))
        new_batch.total_images = len(files)
        new_batch.save()
        
        for file in files:
            bank = ImageBank()
            filename_temp=(file.split("/")[-1]).split(".")
            print(filename_temp)
            #print(request.scheme,'://',request.META.HTTP_HOST)
            bank.URL = file
            bank.file_name = filename_temp[0]
            bank.batch = new_batch
            bank.save()

        batches = Batch.objects.filter(created_by=request.user)

        return render(request, template_name='batch_upload/view.html', context={'batches': batches})


