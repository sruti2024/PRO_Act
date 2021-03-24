from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="home"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('find-email/', csrf_exempt(views.find_email), name='find_email'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('check-otp/', views.check_otp, name='check_otp'),
    path('validate-password/', csrf_exempt(views.password_validation),name='password_validate'),
    path('password/reset/', views.forgot_password, name="forgot_password"),
    path('project_add/', views.project_add, name="project_add"),
    path('project_view/', views.project_view, name="project_view"),
    path('profile/', views.profile , name="profile"),
    path('profile_update/',views.profile_update,name="profile_update"),
    path('contact/', views.contact , name="contact"),

]



urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)