from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from home.models import Project_add

# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'index.html')

def loginUser(request):
    if request.method=='POST':
        username= request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            return render(request,'login.html')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('/login')

def project_add(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        desc=request.POST.get('desc')
        link=request.POST.get('link')
        stack=request.POST.get('stack')
        project_add=Project_add(name=name , desc=desc, link=link, stack=stack, date=datetime.today())
        project_add.save()
        messages.success(request, 'Your Project has been added')

    return render(request,'project_add.html')

def project_view(request):
    obj=Project_add.objects.all
    return render(request,'project_view.html',{'object':obj})

def profile(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'profile.html')