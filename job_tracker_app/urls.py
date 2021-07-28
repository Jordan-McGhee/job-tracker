from django.urls import path
from . import views

urlpatterns = [
    # LOGIN/REGISTER/LOGOUT FUNCTIONS
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

    # DASHBOARD
    path('jobtracker/dashboard', views.dashboard)
]