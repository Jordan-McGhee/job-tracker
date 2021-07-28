from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

# Create your views here.

# LOGIN/REGISTER

def index(request):
    return render(request, "login_reg.html")

def register(request):
    if request.method == "POST":
        errors = User.objects.validator(request.POST)

        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')

        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id

        return redirect('/swolemates')

    return redirect('/')

def login(request):
    if request.method=="POST":
        
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, "Invalid Email/Password")
            return redirect('/')

        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id

        return redirect('/swolemates')

    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')