from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from app.models import *
from.import models
from django.contrib.auth  import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        
        password = request.POST.get('password')
        user = authenticate(username=username,password = password)
        if user is not None:
            login(request,user)
            return redirect('/')
        
        messages.info(request,"invalid credentials")
    
    return render(request,'account/user_login.html')

def user_register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password= request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get('phone_field')
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request,"username has already taken..sorry!! ")
                return redirect('user_register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.info(request,"email id has already taken, sorry!!...")
                    return redirect('user_register')
                else:
                    user = User.objects.create_user(username=username,email=email,password=password)
                    user.save()
                    data=Customer(user=user,phone_field=phone)
                    data.save()
                    #login code new customer
                    our_user = authenticate(request,username=username,password=password)
                    if our_user is not None:
                        login(request,user)
                        return redirect('/')
        else:
            messages.info(request,"invalid password")
            return redirect('user_register')
    return render(request,'account/user_register.html')
    
    
    
    
def user_logout(request):
    logout(request)
    return redirect('/')
    

