from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_posts, name="view-posts"),
    path('add-post/', views.add_post, name="add-post")
]