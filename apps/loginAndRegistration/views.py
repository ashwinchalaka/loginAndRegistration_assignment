from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import *
import bcrypt

def index(request):
    if 'loggedIn' in request.session:
        return redirect(reverse('loggedin'))
    return render(request, 'loginAndRegistration/index.html')

def processRegistration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect(reverse('home'))
    else:
        tempHash = bcrypt.hashpw(request.POST['password'].strip().encode(), bcrypt.gensalt())
        currentEmail = request.POST['email']
        if not User.objects.filter(email = currentEmail):
            tempUser = User.objects.create(first_name=request.POST['first_name'].strip(), last_name=request.POST['last_name'].strip(), email=request.POST['email'].strip().lower(), password=tempHash)
            messages.success(request, "Successfully registered")
        elif User.objects.filter(email = currentEmail):
            messages.error(request, "That email is already registered")
        return redirect(reverse('home'))

def processLogin(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags = key)
        return redirect(reverse('home'))
    else:
        currentEmail = request.POST['email'].strip()
        savedUser = User.objects.filter(email = currentEmail)
        if savedUser:
            passMatch = bcrypt.checkpw(request.POST['password'].strip().encode(), savedUser.values()[0]['password'].encode())
        else:
            messages.error(request, "That email is not registered")
        if savedUser and passMatch:
            request.session['loggedIn'] = savedUser.values()[0]['first_name']
            return redirect(reverse('loggedin'))
    return redirect(reverse('home'))

def login(request):
    if 'loggedIn' in request.session:
        return render(request, 'wall/wall.html')
    else:
        return redirect(reverse('home'))

def processLogout(request):
    request.session.clear()
    return redirect(reverse('home'))