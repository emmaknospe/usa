# profiles/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('register_student/', views.RegisterStudent.as_view(), name='register-student'),
    path('register_donor/', views.RegisterDonor.as_view(), name='register-donor')
]