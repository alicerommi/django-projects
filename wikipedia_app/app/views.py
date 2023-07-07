from django.http import JsonResponse
import pytz
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
import os, sys
import math
import datetime
from random import randint
from time import sleep

# Create your views here.
def login(request):
    return render(request,"login.html")

@login_required()
def home(request):
    return render(request, "home.html")


def sign_in(request):
    if request.method == "POST":
        u_email = request.POST.get('useremail')
        u_password = request.POST.get('userpassword')
        #print(email,password)
        user = authenticate(request,username=u_email, password=u_password)
        #print(user)
        if user is not None:
            login(user)
            return redirect("/home")
        else:
            messagess = {'err': 'You have entered wrong details. Try Again!'}
            return render(request, '', messagess)
    # return render(request, '')