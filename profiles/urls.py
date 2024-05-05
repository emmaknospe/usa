from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.UserHomeView.as_view(), name='user-home'),
    path('student_setup/<int:setup_stage>/', views.setup_student, name='student-profile-setup'),
    path('donor_setup/<int:setup_stage>/', views.setup_donor, name='donor-profile-setup')
]