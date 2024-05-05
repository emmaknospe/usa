from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.redirect_to_home_view, name='redirect-to-home-view'),
    path('student_home/<str:tab>/', views.student_home, name='student-home'),
    path('donor_home/<str:tab>/', views.donor_home, name='donor-home'),
    path('admin_home/<str:tab>/', views.admin_home, name='admin-home'),
    path('setup_student/<int:setup_stage>/', views.setup_student, name='setup-student'),
    path('setup_admin/', views.setup_admin, name='setup-admin'),
    path('setup_donor/', views.SetupDonorView.as_view(), name='setup-donor'),
    path('setup_organization/', views.SetupOrganizationView.as_view(), name='setup-organization'),
    path('process_setup_organization/', views.process_setup_organization, name='process-setup-organization'),
    path('organization_homepage/<int:organization_id>/<str:tab>/', views.organization_homepage,
         name='organization-home'),
    path('profile/<int:profile_id>/', views.view_profile, name='view-profile')
]