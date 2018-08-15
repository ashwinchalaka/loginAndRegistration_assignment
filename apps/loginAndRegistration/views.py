from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import *

def index(request):
    if 'loggedIn' in request.session:
        return redirect(reverse('loggedin'))
    return render(request, 'loginAndRegistration/index.html')

def processRegistration(request):
    # pass the post data to the method we wrote and save the response in a variable called errors
    errors = User.objects.basic_validator(request.POST)
    # check if the errors object has anything in itcopy
    if len(errors):
        # if the errors object contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect(reverse('home'))
    else:
        # if the errors object is empty, that means there were no errors!
        currentEmail = request.POST['email']
        if not User.objects.filter(email = currentEmail):
            tempUser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'])
            messages.success(request, "Successfully registered")
            # redirect to a success route
        elif User.objects.filter(email = currentEmail):
            messages.success(request, "That email is already registered")
        return redirect(reverse('home'))

def processLogin(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(reverse('home'))
    else:
        currentEmail = request.POST['email']
        currentUser = User.objects.filter(email = currentEmail)
        if currentUser:
            request.session['loggedIn'] = currentUser.values()[0]['first_name']
            return redirect(reverse('loggedin'))
    return redirect(reverse('home'))

def login(request):
    return render(request, 'loginAndRegistration/loginSuccess.html')

def processLogout(request):
    request.session.clear()
    return redirect(reverse('home'))