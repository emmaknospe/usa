from django.urls import path
from . import views


urlpatterns = [
    path('create/<int:scholarship_id>/', views.create_application, name='create-application'),
    path('create-question/<slug:question_type>/', views.create_question, name='create-question'),
    path('edit-question/<int:question_id>/', views.edit_question, name='edit-question'),
    path('edit-question-save/', views.edit_question_save, name='edit-question-save'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete-question'),
    path('apply/<int:scholarship_id>/', views.apply, name='apply'),
    path('submit-application/<int:application_id>/', views.submit_application, name='submit-application'),
    path('withdraw/<int:application_response_id>/', views.withdraw_application, name='withdraw-application')
]