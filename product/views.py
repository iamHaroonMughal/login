from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout 
from django.contrib.auth.decorators import login_required
# Create your views here.
@ login_required(login_url="login/")
def receipes(request):
    if request.method == "POST":
        data = request.POST
        receipe_Image = request.FILES.get('receipe_Image')
        receipe_name = data.get("receipe_name")
        receipe_deiscription = data.get("receipe_deiscription")
        Receipe.objects.create(
            receipe_Image = receipe_Image,
            receipe_name = receipe_name,
            receipe_deiscription = receipe_deiscription
        )
        return redirect("/receipes/")
    
    queryset = Receipe.objects.all()
    if request.GET.get('search'):
        queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))
        
    
    
    
    context = {'receipes': queryset}
    
    return render(request, 'receipes.html' , context)


def delete_receipe(request , id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    
    return redirect('/receipes/')

def update_receipe(request , id):
    queryset = Receipe.objects.get(id = id)
    if request.method == "POST":
        data = request.POST
        receipe_Image = request.FILES.get('receipe_Image')
        receipe_name = data.get("receipe_name")
        receipe_deiscription = data.get("receipe_deiscription")
        
        queryset.receipe_name = receipe_name
        queryset.receipe_deiscription = receipe_deiscription
        
        if receipe_Image:
            queryset.receipe_Image = receipe_Image
            
        queryset.save()
        return redirect('/receipes/') 
        
            
    context = {'receipe' : queryset}
    
    return render(request , 'update_receipe.html' , context)


def login_page(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if not User.objects.filter(username = username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/login/')
        
        user = authenticate(username = username , password = password)
    
        if user is None:
            messages.success(request, "Invalid Username")
            return redirect('/login/')
        
     
        else:
            login(request , user)
            return redirect('/receipes/')
        
    
    return render(request , "login.html")


def register(request):
    if request.method =="POST":
        firstname = request.POST.get("firstname")
        lastname =  request.POST.get("lastname")
        username = request.POST.get("username")
        password = request.POST.get("password" )
        
        
        user = User.objects.filter(username = username) 
        
        if user.exists():
            messages.info(request, "Username already taken")
            return redirect('/register/')
         
        
        user = User.objects.create(
            first_name = firstname,
            last_name = lastname,
            username = username
        )
        
        
        user.set_password(password)
        user.save()
        
        messages.info(request, "Account Created Successfully")
        
        return redirect('/login/')
        
    
    
    return render(request , "register.html")



def log_out(request):
    logout(request)
    return redirect('/login/')
    