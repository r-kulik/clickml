"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from main_page import views as main_page_views
from workspace import views as workspace_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page_views.index, name='Home page'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('workspace', workspace_views.main, name='Workspace'),
    path('create_new_model', workspace_views.createNewModel, name='Create New Model')
]

urlpatterns += [
    path('accounts/register', main_page_views.register, name='Register'),
    path('accounts/', main_page_views.register, name='Register done')
]
