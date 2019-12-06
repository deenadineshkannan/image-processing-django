#Author:dinesh kannan dated on 04/12/2019
#this file to receive images from trial users and store it to database 
# and invoke yolo to detect objects
#function imageupload  is to get images and upload to DB
#function trial_detect is to invoke yolo darkflow to identify pretrained objects(80 classes)
from django.shortcuts import render,redirect
from firstapp.models import image_trial
from django.utils import timezone
from werkzeug.utils import secure_filename
import os, glob
from pathlib import Path
from os import listdir
from os.path import isfile, join
from subprocess import call
from django.core.files.storage import FileSystemStorage
from django.conf import settings
label_name = ""
instance_path = os.path.dirname(__file__)
media_url = settings.MEDIA_URL
# Create your views here.
def imageupload(request):
    if request.method == 'POST':
        f = request.FILES['file']
        label_name = request.POST['label']                   #get label input for dataset from upload.html
        print(label_name)
        try:
            #create directory for images and annotations as a child of label directory
            os.makedirs(os.path.join(media_url, label_name), exist_ok=False)
            print(instance_path)
            os.makedirs(os.path.join(media_url, label_name,'images'), exist_ok=False)
            os.makedirs(os.path.join(media_url, label_name,'annotations'), exist_ok=False)
        except FileExistsError:
            #throw error if label is empty
            if label_name =="":
                warning_msg = "please provide name"
                return render(request,'imageupload.html')
            #throw error if directory already exists in label name
            warning_msg = 'Label alread exists, choose unique label'
            print(label_name)
            #if label name is not valid  reload the entire page
            return render(request,'imageupload.html')
        uploadedImageList = request.FILES['file']     #store all uploaded images as object in uploadedImageList
        fs = FileSystemStorage(location=os.path.join(media_url, label_name,'images'))
        filename = fs.save(secure_filename(uploadedImageList.name),uploadedImageList)
        print(uploadedImageList)
        # for uploadedImage in uploadedImageList:
        #     print(uploadedImageList)
        #     try:
        #         uploadedImageList.save(os.path.join(instance_path, label_name,'images', secure_filename(uploadedImage.filename)))
        #         pass
        #     except FileExistsError:
        #     # throw error if image exists in image directory
        #         warning_msg = 'image alread exists, clear the directory'
        #         return render(request,'imageupload.html')  
        #         pass
        # image_path_glob = '../yolo_helmet/instance/'+label_name+'/images/*.jpg'
        # file_path_list_full = []
        # file_path_list_full = glob.glob(image_path_glob)
        return  redirect('trialdetect',label_name)
    return  render(request,'imageupload.html')


def imageupload2(request):
    p = ' a'
    if request.method == 'POST':
        image_path = request.FILES['file']
        # image_path = request.FILES.getlist('file')
        label_name1 = request.POST['label']
        #label_name1 = "Trial"
        p = label_name1
        image_detail = image_trial(label_name=label_name1,image_path=image_path,image_uploaded=timezone.now())
        image_detail.save()
        # p = image_trial.objects.all()
        # p = image_trial.objects.filter(label_name=label_name1)
    # return render(request, "imageupload.html",{'p':p})
        return redirect('trialdetect',p)
    
    pth = os.path.dirname(__file__)
    print(pth)
    return render(request, "imageupload.html",{'p':p})

def trialdetect(request, p):
    import os
    # a = request.GET
    print(os.getcwd())
    os.chdir("darkflowmaster")
    #! /usr/bin/env python
    import sys
    from darkflow.cli import cliHandler
    # sys.argv = "flow --imgdir sample_img/ --model cfg/yolo.cfg --load bin/yolov2.weights  --gpu 1.0"
    # sys.argv[0]="flow"
    print("=========================")
    print(p)
    # sys.argv[8:]="--imgdir sample_img/ --model cfg/yolo.cfg --load bin/yolov2.weights  --gpu 1.0"
    # print(sys.argv[1])
    # sys.argv[2:]="sample_img/"
    # sys.argv[3]="--model"
    # sys.argv[4]="cfg/yolo.cfg "
    # sys.argv[5]="--load"
    # sys.argv[6]="bin/yolov2.weights"
    # sys.argv[7]="--gpu"
    # sys.argv[8]="1.0"
    # print(sys.argv)
    from subprocess import call
    # imgdir = "sample_img/"
    imgdir = "../"+media_url+p+"/images/"
    print(imgdir,"ddddddddddddddddddddddddddddddddddddddddddd")
    call("flow --imgdir "+imgdir+" --model cfg/yolo.cfg --load bin/yolov2.weights  --gpu 1.0",shell=True)
    outdir = '../'+media_url+p+'/images/out/*.jpg'
    image_path_glob = '.jpg'
    print(image_path_glob)
    print(outdir)
    file_path_list_full = []
    print("#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#")
    file_path_list_full = glob.glob(outdir)
    print(file_path_list_full)
    os.chdir("..")
    print(os.getcwd())
    print(outdir)
    return render(request, "trial_detect.html",{'p':file_path_list_full[0]})