from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import OTPModel
from datetime import datetime
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.conf import settings
from home.models import Project_add
from random import randint
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
import json
import urllib
import re


# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect("login")
    return render(request, 'index.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, 'login.html', {'error': 'Invalid Login Credentials'})
    return render(request, 'login.html')


def logoutUser(request):
    logout(request)
    return redirect('/login')


def find_email(request):
    data = json.loads(request.body)
    email = data['email']
    if not User.objects.filter(email=email).exists():
        return JsonResponse({'email_error': 'You are not registered. Please signup to continue.'}, status=404)
    return JsonResponse({'email_valid': True})


def gen_otp():
    return randint(100000, 999999)


def send_otp(request):
    user_email = request.GET['email']
    user = User.objects.get(email=user_email)
    user_name = user.first_name
    otp = gen_otp()     # Generate OTP
    # Save OTP in database and send email to user
    try:
        OTPModel.objects.create(user=user_email, otp=otp)
        data = {
            'receiver': user_name.capitalize(),
            'otp': otp
        }
        html_content = render_to_string("emails/otp.html", data)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            f"One Time Password | PRO ACT",
            text_content,
            "PRO ACT <no-reply@pro_act.com>",
            [user_email]
        )
        print("sending email")
        email.attach_alternative(html_content, "text/html")
        email.send()
        print("Sent")
        return JsonResponse({'otp_sent': f'An OTP has been sent to {user_email}.'})
    except Exception as e:
        print(e)
        return JsonResponse({'otp_error': 'Error while sending OTP, try again'})


def match_otp(email, otp):
    otp_from_db = OTPModel.objects.filter(user=email).last().otp
    return str(otp) == str(otp_from_db)

def check_otp(request):
    req_otp = request.GET['otp']
    req_user = request.GET['email']
    if match_otp(req_user, req_otp):
        return JsonResponse({'otp_match': True})
    return JsonResponse({'otp_mismatch': 'OTP does not match.'})


def password_validation(request):
    data = json.loads(request.body)
    try:
        password1 = data['password1']
    except Exception:
        password1 = data['password']
    pattern = '^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%&_])(?=\S+$).{8,20}$'
    if bool(re.match(pattern, password1)):
        return JsonResponse({'password_valid': True})
    else:
        return JsonResponse({'password_error': 'Password must be 8-20 characters long and must contain atleast one uppercase letter, one lowercase letter, one number(0-9) and one special character(@,#,$,%,&,_)'})


def forgot_password(request):
    if request.method == "POST":
        try:
            password = request.POST.get('password')
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return render(request, "login.html", {"message": "Password changed successfully. You can now login with your new password."})
        except Exception:
            return render(request, "forgot-password.html", {"error": "Password could not be changed, please try again."})
    return render(request, "forgot-password.html")


def project_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        link = request.POST.get('link')
        stack = request.POST.get('stack')
        project_add = Project_add(
            name=name, desc=desc, link=link, stack=stack, date=datetime.today())
        project_add.save()
        messages.success(request, 'Your Project has been added')

    return render(request, 'project_add.html')


def project_view(request):
    obj = Project_add.objects.all
    return render(request, 'project_view.html', {'object': obj})


def profile(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request,'profile.html')
