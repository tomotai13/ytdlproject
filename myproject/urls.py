
from django.contrib import admin
from django.urls import path,include
from .views import test, test1
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ytdl/',include('ytdlapp.urls')),
    path('pytube_url/', test),
    path('tets/', test1),
]
