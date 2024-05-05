from django.urls import path
from . import views


urlpatterns = [
    path('create/<int:organization_id>/', views.create_scholarship, name='create-scholarship'),
    path('view/<int:scholarship_id>/', views.view_scholarship, name='view-scholarship'),
    path('search/', views.search_scholarships, name='search-scholarships'),
    path('get_similar_key_words/<str:key_word>/', views.get_similar_key_words, name='get-similar-key-words'),
    path('launch_scholarship/<int:scholarship_id>/', views.launch_scholarship, name='launch-scholarship'),
    path('retract_scholarship/<int:scholarship_id>/', views.retract_scholarship, name='retract-scholarship')
]