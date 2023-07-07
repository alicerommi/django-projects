import time
from django.shortcuts import render,redirect
from modules.author_publications import author_publication
from django.http import JsonResponse
import json
import pandas as pd
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from mysite.serializers import *
from .models import *
from main import run
import psycopg2
from django.core import serializers
# from googlescholarproject.settings import DATABASES


from scholar.scholar.database import db
# Create your views here.
def index(request):
    global search
    search = ""
    if request.method == 'POST':
        search = request.POST['search']
    return render(request, 'index.html')

def university(request):
    global search
    search = ""
    if request.method == 'POST':

        search = request.POST['search']
    return render(request, 'university.html')
def authors(request):
    if search == "":
        data = {}
    else:
        run = author_publication(search)
        d = run.crawler()
        df = pd.DataFrame.from_dict(d)
        data = df.to_dict('records')
    return JsonResponse({'d': json.dumps(data)})

def titles_by_uni(request):

    if search == "":
        json_data = {}
    else:
        c = run()
        c.scraptitles(search)
        title = Title.objects.all()
        title_serializer = TitleSerializer(title, many=True)
        json_data = JSONRenderer().render(title_serializer.data)
    return HttpResponse(json_data, content_type='application/json')

def abc(request):
    return render(request,'abc.html')


def signin(request):
    if request.method== "POST":
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        print(loginusername)
        print(loginpass)
        json_data = serializers.serialize('json',Authen.objects.all())
        print(json_data)
        json_data = json.loads(json_data)
        bool = False
        for all in json_data:
            checkusername = all['fields']['username']
            checkpassword = all['fields']['password']
            if loginusername == checkusername and loginpass == checkpassword:
                print('yahoo')
                bool = True
                break
            else:
                continue
        if bool == False:
            print("user not found")
            return render(request,'login.html',{'d':'user not found'})
        elif bool == True:
            return render(request,'index.html')




    return render(request,'login.html')