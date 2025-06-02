from django.shortcuts import render

from django.http import HttpResponse
import datetime


# def teste(request):
#     return render(request, 'index.html')

def current_datetime(request):
    now = datetime.datetime.now()
    html = '<html lang="en"><body>It is now %s.</body></html>' % now
    return HttpResponse(html)
