from django.shortcuts import render, redirect
from django.http import JsonResponse
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
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm,UserUpdateForm
from django.core.mail import send_mail


# Create your views here.

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, 'index.html')

def contact(request):
	if request.method == "POST":
		message_name = request.POST['message-name']
		message_email = request.POST['message-email']
		message = request.POST['message']

		# send an email
		send_mail(
			message_name, # subject
			message, # message
			message_email, # from email
			['PRO_ACT@gmail.com'], # To Email
			)

		return render(request, 'contact.html', {'message_name': message_name})

	else:
		return render(request, 'contact.html', {})

def signupUser(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        new_user = User(first_name=fname, last_name=lname,
                           email=email, username=username, password=password)
        new_user.password = make_password(new_user.password)
        new_user.is_active = True
        new_user.save()
        return render(request, "login.html", {"message": "You can now login to your account."})
    return render(request, "signup.html")


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
            if not request.POST.get('remember', None):
                request.session.set_expiry(0)
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

def email_validation(request):
    data = json.loads(request.body)
    email = data['email']
    pattern = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if User.objects.filter(email=email).exists():
        return JsonResponse({'email_error': 'You are already registered. Please login to continue.'}, status=409)
    if not bool(re.match(pattern, email)):
        return JsonResponse({'email_error': 'Please enter a valid email address.'})
    return JsonResponse({'email_valid': True})

def username_validation(request):
    data = json.loads(request.body)
    username = data['username']
    if User.objects.filter(username=username).exists():
        return JsonResponse({'username_error': 'Username is already taken. Please choose another'}, status=409)
    if len(username) < 5:
        return JsonResponse({'username_length_error': 'Username must be atleast 5 characters long'})
    return JsonResponse({'username_valid': True})


def gen_otp():
    return randint(100000, 999999)


def send_otp(request):
    user_email = request.GET['email']
    try:
        user_name = request.GET['fname']
    except Exception:
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

def match_passwords(request):
    data = json.loads(request.body)
    password1 = data['password1']
    password2 = data['password2']
    print(password1,password2)
    if str(password1) == str(password2):
        return JsonResponse({'password_match': True})
    else:
        print("Sending")
        return JsonResponse({'password_mismatch': 'Password and Confirm Password do not match.','passwords': f'{password1} {password2}'})

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

# making login required for project add page and redirecting it to the login page
@login_required(login_url="/login")
def project_add(request):
    context = {
        "tags": {
            "Java": "java",
            "cpp": "C++",
            "React":"react",
            "Django":"django",
            "Html":"html",
            "CSS":"css",
            "Angular":"angular",
            "Python":"python",
        }
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        link = request.POST.get('link')
        stack = request.POST.getlist('stack')
        project_add = Project_add(
            name=name, desc=desc, link=link, stack=stack, date=datetime.today())
        project_add.save()
        messages.success(request, 'Your Project has been added')

    return render(request, 'project_add.html',context)


def project_view(request):
    obj = Project_add.objects.all
    return render(request, 'project_view.html', {'object': obj})


# Redirecting anonymous login to the right login page
@login_required(login_url="/login")
def profile(request):
    return render(request,'profile.html')


def profile_update(request):
    if request.method=="POST":
        u_form=UserUpdateForm(request.POST,request.FILES,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'You account has been updated.')
            return redirect('profile')


    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)


    context={
        'u_form':u_form,
        'p_form':p_form,
    }
    return render(request,'profile_update.html',context)

def changepassword(request):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break
    if curr == 0:
        return redirect("login")
    error=""
    if request.method == 'POST':
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
            u = User.objects.get(username__exact = request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    context={'error':error}
    return render(request, 'changepassword.html',context)

def modules(request, p_id):
    obj = Project_add.objects.get(pid = p_id)
    context= {"obj": obj}
    return render(request, 'modules.html', context)

