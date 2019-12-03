from django.shortcuts import render,redirect
from firstapp.models import image_trail
from django.utils import timezone


# Create your views here.
def imageupload(request):
    p = ' a'

    if request.method == 'POST':
        image_path = request.FILES['file']
        label_name1 = request.POST['label']
        
        image_detail = image_trail(label_name=label_name1,image_path=image_path,image_uploaded=timezone.now())
        image_detail.save()
        # p = image_trail.objects.all()
        p = image_trail.objects.filter(label_name=label_name1)
    return render(request, "imageupload.html",{'p':p})