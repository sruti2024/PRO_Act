from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="home"),
    path('signup/', views.signupUser, name="signup"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('find-email/', csrf_exempt(views.find_email), name='find_email'),
    path('validate-email/', csrf_exempt(views.email_validation), name='email_validate'),
    path('validate-username/', csrf_exempt(views.username_validation), name='username_validate'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('check-otp/', views.check_otp, name='check_otp'),
    path('validate-password/', csrf_exempt(views.password_validation),name='password_validate'),
    path('match-passwords/', csrf_exempt(views.match_passwords),name='password_match'),
    path('password/reset/', views.forgot_password, name="forgot_password"),
    path('project_add/', views.project_add, name="project_add"),
    path('project_view/', views.project_view, name="project_view"),
    path('profile/', views.profile , name="profile"),
    path('profile_update/',views.profile_update,name="profile_update"),
    path('contact/', views.contact , name="contact"),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('modules/<str:p_id>/', views.modules, name="modules")

]



urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)