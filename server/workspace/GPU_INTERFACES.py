import datetime
import json
import os

import requests
from django.http import HttpResponse, HttpRequest, FileResponse

from .models import WorkingGpuRemoteServer, UploadTokens, LearningTask, MLMODEL


def __ENTER_AS_A_GPU_SERVER(request: HttpRequest) -> HttpResponse:
    IP_ADDRESS = __get_ip_address(request)
    for instance in WorkingGpuRemoteServer.objects.filter(IP_ADDRESS=IP_ADDRESS):
        instance.delete()
    remote_server = WorkingGpuRemoteServer(
        IP_ADDRESS=IP_ADDRESS,
        LAST_REQUEST=datetime.datetime.now()
    )
    remote_server.save()
    return HttpResponse("OK")


def __GET_DATASET_FILE(request: HttpRequest) -> FileResponse:
    token = request.GET.get('UPLOAD_TOKEN', '')
    if len(token) == 0:
        return "Some exception has occured"
    file_to_download = UploadTokens.objects.filter(UPLOAD_TOKEN=token)[0].FILE_PATH
    return FileResponse(file_to_download)



def __COMPLETE_LEARNING_TASK_AND_GET_FILES(request: HttpRequest) -> HttpResponse:
    """
    схема запроса
    click-ml.ru/complete_learning_task_and_get_files?task_id={task_id}
    :param request:
    :return:
    """
    if request.method == "POST":
        learning_task_id = request.POST.get("task_id")
        learning_task: LearningTask = LearningTask.objects.get(id=learning_task_id)
        learning_task.success = 1
        learning_task.save()

        if not os.path.exists('/ml_models'):
            os.makedirs('/ml_models')
        if not os.path.exists(f'/ml_models/{learning_task.user.username}'):
            os.makedirs(f'/ml_models/{learning_task.user.username}')
        if not os.path.exists(f'/ml_models/{learning_task.user.username}/{learning_task.project_name}'):
            os.makedirs(f'/ml_models/{learning_task.user.username}/{learning_task.project_name}')

        ml_model = MLMODEL(
            user = learning_task.user,
            project_name = learning_task.project_name
        )
        ml_model.save()

        return HttpResponse(
            json.dumps(
                {
                    "ml_model_id": ml_model.id,
                    "upload_valid_token": ml_model.valid_token_to_upload_files
                }
            )
        )



def __get_ip_address(request) -> str:
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
