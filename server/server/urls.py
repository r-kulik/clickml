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
    path('download_results', workspace_views.downloadResults, name="Download Results")
]

urlpatterns += [
    path('accounts/register', main_page_views.register, name='Register'),
    path('accounts/', main_page_views.register, name='Register done')
]

urlpatterns += [
    path('enter_as_gpu_machine', GPU_INTERFACES.__ENTER_AS_A_GPU_SERVER, name='Enter as a GPU SERVER'),
    path('get_dataset_file', GPU_INTERFACES.__GET_DATASET_FILE, name='Download the dataset file'),
    path('complete_learning_task_and_get_files',
         GPU_INTERFACES.__COMPLETE_LEARNING_TASK_AND_GET_FILES,
         name='Complete Task'),
    path('upload_model_configuration_file', GPU_INTERFACES.__UPLOAD_MODEL_CONFIGURATION_FILE,
         name='Upload Config Files'),
    path('complete_exploit_task_and_get_files', GPU_INTERFACES.__COMPLETE_EXPLOIT_TASK_AND_GET_FILES,
         name="Complete Exploit Task")
]

websocket_urlpatterns = [
    re_path(r'loading_results/\d+', consumers.ExploitLoadingConsumer.as_asgi())
]
