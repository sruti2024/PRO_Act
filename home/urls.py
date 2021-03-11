from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index,name="home"),
    path('login', views.loginUser,name="login"),
    path('logout', views.logoutUser,name="logout"),
    path('project_add', views.project_add , name="project_add"),
    path('project_view', views.project_view , name="project_view")

]
