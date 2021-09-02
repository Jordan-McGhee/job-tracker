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

def guest(request):
    user = User.objects.filter(email="guestyguest@guest.com")

    if user:
        user = User.objects.get(email = "guestyguest@guest.com")
    else:
        user = User.objects.create(first_name = "Guesty", last_name = "Guest", email="guestyguest@guest.com", password = "12345678")
    request.session['user_id'] = user.id

    return redirect('/jobtracker/dashboard')

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

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "status_choices": Job.status_choices
    }

    return render(request, "new_job.html", context)

def create_new_job_posting(request):
    if request.method == "POST":
        user = User.objects.get(id=request.session['user_id'])
        errors = Job.objects.validator(request.POST)

        if len(errors) > 0:
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f"/jobtracker/add_job")

        company_url = request.POST['company_website']
        job_posting = request.POST['job_posting_url']

        if "https://" in request.POST['company_website']:
            company_url = request.POST['company_website'][8:]

        if "https://" in request.POST['job_posting_url']:
            job_posting = request.POST['job_posting_url'][8:]

        job = Job.objects.create(
            company = request.POST['company'],
            role = request.POST['role'],
            city = request.POST['city'],
            state = request.POST['state'],
            company_website = company_url,
            job_posting_url = job_posting,
            status = request.POST['status'],
            description = request.POST['description'],
            user = user
        )
    return redirect(f'/jobtracker/job/{job.id}')


# EDIT JOB POSTING
def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "job": job,
        "status_choices": Job.status_choices,
        "job_status": job.get_status_display()
    }
    return render(request, "edit_job.html", context)

def update_job(request, job_id):
    if request.method == "POST":
        errors = Job.objects.validator(request.POST)

        if len(errors) > 0:
            for k,v in errors.items():
                messages.error(request, v)
            return redirect(f"/jobtracker/job/{job_id}/edit")

        company_url = request.POST['company_website']
        job_posting = request.POST['job_posting_url']

        if "https://" in request.POST['company_website']:
            company_url = request.POST['company_website'][8:]

        if "https://" in request.POST['job_posting_url']:
            job_posting = request.POST['job_posting_url'][8:]

        job = Job.objects.get(id=job_id)

        job.company = request.POST['company']
        job.role = request.POST['role']
        job.city = request.POST['city']
        job.state = request.POST['state']
        job.company_website = company_url
        job.job_posting_url = job_posting
        job.status = request.POST['status']
        job.description = request.POST['description']
        job.save()

    return redirect(f'/jobtracker/job/{job_id}')

def delete_job(request, job_id):
    if request.method == "POST":
        job = Job.objects.get(id=job_id)
        job.delete()

    return redirect("/jobtracker/dashboard")


# VIEW JOB POSTING
def view_job(request, job_id):
    job = Job.objects.get(id=job_id)

    # print(f"Look here: {job.get_status_display()}")

    context = {
        "user": User.objects.get(id=request.session['user_id']),
        "job": job,
        "comments": job.comments.all(),
        "status_choices": Job.status_choices,
        "job_status": job.get_status_display()
    }
    return render(request, "view_job.html", context)

def view_status_update(request, job_id):
    if request.method == "POST":
        job = Job.objects.get(id=job_id)
        # print(f"Original: {job.status}")
        job.status = request.POST['status']
        # print(f"request.POST = {request.POST['status']}")
        # print(f"Changed to: {job.status}")
        job.save()

    return redirect(f'/jobtracker/job/{job_id}')

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