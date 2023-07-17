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
from django.urls import path, re_path
from django.conf.urls import include
from workspace import main_page_views as main_page_views
from workspace import views as workspace_views
from workspace import GPU_INTERFACES
from workspace import consumers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page_views.index, name='Home page'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    path('workspace', workspace_views.main, name='Workspace'),
    path('create_new_model', workspace_views.createNewModel, name='Create New Model'),
    path('model_creation_settings', workspace_views.modelCreationSettings, name='Set up a model'),
    path('use_model', workspace_views.useMlModel, name='Use Model'),
    path('view_results', workspace_views.viewResults, name='View Results'),
    path('download_results', workspace_views.downloadResults, name="Download Results"),
    path('delete_model', workspace_views.__DELETE_MODEL, name="delete model")
]

urlpatterns += [
    path('accounts/register', main_page_views.register, name='Register'),
    path('accounts/', main_page_views.register, name='Register done')
]

urlpatterns += [
    path('get_learning_task', GPU_INTERFACES.__GET_LEARNING_TASK, name='Get Learn Task'),
    path('complete_learning_task',
         GPU_INTERFACES.__COMPLETE_LEARNING_TASK_AND_GET_FILES,
         name='Complete Task'),
    path('get_exploit_task', GPU_INTERFACES.__GET_EXPLOIT_TASK, name='Get exploit task'),
    path('get_exploit_task_model_files', GPU_INTERFACES.__GET_EXPLOIT_TASK_MODEL_FILES,
         name='Get exploit task model files'),
    path('complete_exploit_task', GPU_INTERFACES.__COMPLETE_EXPLOIT_TASK_AND_GET_FILES,
         name="Complete Exploit Task"),
    path('accept_percent', GPU_INTERFACES.__ACCEPT_PERCENT, name='Accept Percent'),
    path('report_learning_task_exception', GPU_INTERFACES.__REPORT_LEARNING_TASK_EXCEPTION, name='RLTE'),
    path('report_exploit_task_exception', GPU_INTERFACES.__REPORT_EXPLOIT_TASK_EXCEPTION, name='RLTE')
]


urlpatterns += [
    path("yandex_6e171de854288ea5.html", workspace_views.returnYandexVerification, name='A')
]

websocket_urlpatterns = [
    re_path(r'loading_results/\d+', consumers.ExploitLoadingConsumer.as_asgi()),
    re_path(f'learning_results/', consumers.LearningLoadingConsumer.as_asgi())
]


