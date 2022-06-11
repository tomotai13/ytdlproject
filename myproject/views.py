from django.http import HttpResponse
from django.shortcuts import render

def test(request):
    return HttpResponse('エラーが発生中しばらく時間を空けてからアクセスしてください  ２日ほどお待ちください')

def test1(request):
    return render(request, 'test.html')