from django.shortcuts import render
from .models import Article
from django.http import HttpResponse

# Create your views here.


def app_list(request):
    articles =Article.objects.all().order_by('date')
    return render(request,'myapp/app_list.html',{'articles':articles})

def app_detail(request,slug):
    return HttpResponse(slug)