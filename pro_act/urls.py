from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    # path('', TemplateView.as_view(template_name=views.index)),
    path('admin/', admin.site.urls),
    path('',include('home.urls')),
    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
