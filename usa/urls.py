"""usa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from scholarships.views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('profiles.urls')),
    path('profiles/', include('accounts.urls')),
    path('scholarships/', include('scholarships.urls')),
    path('applications/', include('applications.urls')),
    path('content/', include('content.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', IndexView.as_view(), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
