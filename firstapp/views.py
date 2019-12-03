from django.shortcuts import render
from django.http import HttpResponse
from .models import Details1

# Create your views here.
def home(request):
    dests = Details1.objects.all()
    print(dests)
    return render(request, "home.html", {'dests':dests})

def add(request):
    val1 = int(request.POST['num1'])
    val2 = int(request.POST['num2'])
    res = val1 + val2
    return render(request,'result.html',{'result': res})

def base(request):
    return render(request,"base.html")

def single(request):
    return render(request,"single.html")