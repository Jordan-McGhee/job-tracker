from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

# Create your views here.

# LOGIN/REGISTER/LOGOUT

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

        return redirect('/jobtracker/dashboard')

    return redirect('/')

def login(request):
    if request.method=="POST":
        
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, "Invalid Email/Password")
            return redirect('/')

        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id

        return redirect('/jobtracker/dashboard')

    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

# DASHBOARD

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])

    context = {
        "user": user,
        "jobs": user.jobs.all()
    }

    return render(request,"dashboard.html", context)

# ADD JOB POSTING
def add_job(request):
    return render(request, "new_job.html")

def create_new_job_posting(request):
    if request.method == "POST":
        errors = Job.objects.validator(request.POST)

        if len(errors) > 0:
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f"/jobtracker/add_job")

        job = Job.objects.create(
            company = request.POST['company'],
            role = request.POST['role'],
            city = request.POST['city'],
            state = request.POST['state'],
            company_website = request.POST['company_website'],
            job_posting_url = request.POST['job_posting_url'],
            status = request.POST['status'],
        )
    return redirect(f'/jobtracker/job/{job.id}')


# EDIT JOB POSTING
def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "job": job
    }
    return render(request, "edit_job.html", context)

def update_job(request, job_id):
    if request.method == "POST":
        errors = Job.objects.validator(request.POST)

        if len(errors) > 0:
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f"/jobtracker/edit_job")


        job = Job.objects.get(id=job_id)

        job.company = request.POST['company']
        job.role = request.POST['role']
        job.city = request.POST['city']
        job.state = request.POST['state']
        job.company_website = request.POST['company_website']
        job.job_posting_url = request.POST['job_posting_url']
        job.status = request.POST['status']
        job.save()

    return redirect(f'/jobtracker/job/{job_id}')


# VIEW JOB POSTING
def view_job(request, job_id):
    job = Job.objects.get(id=job_id)

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "job": job,
        "comments": job.comments.all()
    }
    return render(request, "view_job.html", context)

def create_comment(request, job_id):
    if request.method == "POST":
        job = Job.objects.get(id=job_id)

        errors = Comment.objects.validator(request.POST)

        if len(errors) > 0:
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f"/jobtracker/job/{job_id}")

        Comment.objects.create(
            content = request.POST['content'],
            job = job
        )

    return redirect(f"/jobtracker/job/{job_id}")

def delete_comment(request, job_id, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(id=comment_id)
        comment.delete()

    return redirect(f"/jobtracker/job/{job_id}")