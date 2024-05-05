from django.urls import path
from . import views


urlpatterns = [
    path('create/<int:organization_id>/', views.create_scholarship, name='create-scholarship'),
    path('view/<int:scholarship_id>/', views.view_scholarship, name='view-scholarship'),
    path('search/', views.search_scholarships, name='search-scholarships')
]