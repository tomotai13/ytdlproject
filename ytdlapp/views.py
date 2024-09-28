 #from django
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

#from third party

from pytube import YouTube, Search
from yt_dlp import YoutubeDL

#from other file
from .forms import UrlForm

#from standard
import json
import logging
import re

logger = logging.getLogger('ytdlapp')

#define yt-dlp-ver code
def confine_video(url):
    array = []
    ops = {
        'skip_download':True
    }
    with YoutubeDL(ops) as ydl:
        res = ydl.extract_info(url)
        array = res
    formats = array["formats"]
    ok_video2 = []
    for el in formats:
        if (el['ext'] == "mp4") and (not bool(el.get("manifest_url"))) and (el["acodec"] != 'none'):
            ok_video2.append(el)

    return ok_video2


def pytubeView(request):
    context={'form':UrlForm(), 'video':'', 'message':'','title':'',}

    if request.method == 'POST':

        url = request.POST.get('url')
        #mp34 = request.POST.get('mp34')
        g_url = re.compile(r'%3D([a-zA-Z0-9-_\.]{11})&usg').search(url)

        if g_url is not None:
            id = g_url.groups()[0]
            url = 'https://www.youtube.com/watch?v={}'.format(id)

        if len(url) == 11:
            url = 'https://www.youtube.com/watch?v={}'.format(url)

        check_url = url[0:33]

        if 'https:' in check_url and 'youtu' in check_url:
            try:
                result = confine_video(url)
                selected_video = result[len(result)-1]
                
                context['video'] = selected_video.get("url")
                context['title'] = "video title is not loaded"
            except Exception as e:
                context['message'] = e
                logger.error(e)

            else:
                #logger.info(context['title'])
                pass
        else:
            context['message'] = '正しいURLを入力してください'

    return render(request, 'ytdl/ptd.html', context)


def search(request):
    return render(request, 'ytdl/serachPtd.html',{})


@csrf_exempt
def ajax_search(request):
    if request.method == "GET":
        return redirect('/ytdl/search-url/', permanent=True)
    
    if request.method == 'POST' and request.body:
        try:
            json_dict = json.loads(request.body)
            query = json_dict['query']

            s = Search(query)
            dict_data = {}
            d = []
            for r in s.results:
                #dict_data['thumbnail_url'] = r.thumbnail_url
                dict_data['video_id'] = r.video_id
                dict_data['thumbnail_url'] = 'https://i.ytimg.com/vi/' + r.video_id + '/mqdefault.jpg'
                dict_data['title'] = r.title
                d.append(dict_data.copy())
        except:
            logger.error(query)
            d.append('error')
        else:
            logger.info(query)

        d = json.dumps(d, ensure_ascii=False)

        return JsonResponse(d, safe=False)


@csrf_exempt
def ajax_stream(request):
    if request.method == "GET":
        return redirect('/ytdl/search-url/', permanent=True)
    
    if request.method == "POST":

        d = {'error':None,}
        json_dict = json.loads(request.body)

        id = json_dict['video_id']
        if len(id) == 11:
            url = 'https://www.youtube.com/watch?v={}'.format(id)

        if 'https' in url or 'youtu' in url:
            try:
                result = confine_video(url)
                selected_video = result[len(result)-1]
                
                d['stream_url'] = selected_video.get("url")
                d['stream_title'] = "video title is not loaded"
                
            except:
                d['error'] = 'error'
                logger.error(url)
            else:
                #logger.info(d['stream_title'])
                pass


        d = json.dumps(d, ensure_ascii=False)

        return JsonResponse(d, safe=False)


