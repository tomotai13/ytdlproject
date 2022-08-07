from django.urls import path
from .views import pytubeView, search, ajax_search, ajax_stream

app_name = "youtube"
urlpatterns = [
    path('pytube-url/', pytubeView, name='pytube'),
    path('search-url/', search, name='a'),
    path('ajax_search/',ajax_search, name='ajax_search'),
    path('ajax_stream/', ajax_stream, name='ajax_stream'),
]
