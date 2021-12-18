from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import random
from .models import *
from django.core.mail import send_mail
import datetime
from pytz import utc


def send_otp(user):
    usr_otp = random.randint(10000,99999)
    UserOTP.objects.create(user=user,otp=usr_otp)
    otp = UserOTP.objects.get(user=user)
    mess= f"Hello {user.first_name} \n Your OTP is {usr_otp} \n Thanks!!"
    send_mail(
        "Verify Your Email",
        mess,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently= False
    )
        

def signup(request):
    if request.method=="POST":
        get_otp= request.POST.get('otp')
        if get_otp:
            get_eml= request.POST.get('email')
            user= CustomUser.objects.get(email=get_eml)
            user_otp = UserOTP.objects.filter(user=user).last()
            timestamp = datetime.timedelta.total_seconds(datetime.datetime.now(utc) - user_otp.time_st)
            if int(get_otp) == user_otp.otp and timestamp <= 60:
                user.is_active = True
                user.save()
                messages.success(request,f"Account has been created for {user.first_name} You can login now!!")
                return redirect("signin")
            
            elif int(get_otp) == user_otp.otp and timestamp >= 60:
                messages.warning(request,"OTP has been expired New OTP has been sent to your mail and enter new otp !!")
                user_otp.delete()
                send_otp(user)
                return render(request,'user/signup.html',{'otp':True,'user':user}) 

            else:
                messages.warning(request,"Incorrect OTP!!")
                return render(request,'user/signup.html',{'otp':True,'user':user})

        form= CustomUserCreationForm(request.POST)

        if form.is_valid():
            user= form.save()
            user.is_active= False
            user.save()
            send_otp(user)
            
            messages.success(request,f"Account has been  submitted for {user.first_name}  Now check your email!")
            return render(request,'user/signup.html',{'otp':True,'user':user})
    else:
        form= CustomUserCreationForm()
        
    return render(request,'user/signup.html',{'form':form})

def signin(request):
    if request.method=="POST":
        get_otp=request.POST.get('otp')

        if get_otp:
            get_eml=request.POST.get('email')
            user=CustomUser.objects.get(email=get_eml)
            
            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active=True
                user.save()
                login(request,user)
                return redirect('index')
            else:
                messages.info(request,"Your OTP has been incorrect!!")
                return render(request,'user/signin.html',{'otp':True,'user':user})

        email= request.POST["email"]
        password= request.POST["password"]
        user= authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            messages.success(request,"Successfully loggedin")
            return redirect("index")

        elif not CustomUser.objects.filter(email=email).exists():
            messages.warning(request,"Invalid Credentials")
            return redirect("signin")

        elif not CustomUser.objects.get(email=email).is_active:
            user=CustomUser.objects.get(email=email)
            messages.warning(request,"Firstafall OTP must be entered")
            return render(request,'user/signin.html',{'otp':True,'user':user})

        else:
            messages.info(request,"Please enter correct credentials")
            return redirect("signin")

    return render(request,'user/signin.html')


@login_required
def success(request):
    return render(request,'user/success.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request,'You have been loggedout successfully!!')
    return redirect("signin")
            
                
                
                
            
        
            

    


