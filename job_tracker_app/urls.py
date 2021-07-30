from django.urls import path
from . import views

urlpatterns = [
    # LOGIN/REGISTER/LOGOUT FUNCTIONS
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    # DASHBOARD
    path('jobtracker/dashboard', views.dashboard),

    # ADD JOB/CREATE JOB
    path('jobtracker/add_job', views.add_job),
    path('jobtracker/create_job', views.create_new_job_posting),

    # EDIT JOB
    path('jobtracker/job/<int:job_id>/edit', views.edit_job),
    path('jobtracker/job/<int:job_id>/update', views.update_job),

    # VIEW JOB
    path('jobtracker/job/<int:job_id>', views.view_job),
    path('jobtracker/job/<int:job_id>/add_comment', views.create_comment),
    path('jobtracker/job/<int:job_id>/comment/<int:comment_id>/delete_comment', views.delete_comment),
]