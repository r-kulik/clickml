import datetime
import json
import os
import secrets

import channels.layers
import requests
from django.http import HttpResponse, HttpRequest, FileResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

from .models import WorkingGpuRemoteServer, UploadTokens, LearningTask, MLMODEL
from asgiref.sync import async_to_sync

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
    file_to_download = default_storage.open(UploadTokens.objects.filter(UPLOAD_TOKEN=token)[0].FILE_PATH)
    return FileResponse(file_to_download)


@csrf_exempt
def __COMPLETE_LEARNING_TASK_AND_GET_FILES(request: HttpRequest) -> HttpResponse:
    """
    схема запроса
    click-ml.ru/complete_learning_task_and_get_files?task_id={task_id}
    :param request:
    :return:
    """
    if request.method == "POST":
        learning_task_id = int(request.headers.get('taskid', -1))
        assert learning_task_id != -1
        print(f'GET A COMPLETION OF TASK #{learning_task_id}')
        learning_task: LearningTask = LearningTask.objects.get(id=learning_task_id)
        learning_task.success = 1
        learning_task.save()
        ml_model = MLMODEL(
            user = learning_task.user,
            project_name = learning_task.project_name,
            valid_token_to_upload_files=secrets.token_urlsafe(),
            creation_time=datetime.datetime.now()
        )
        ml_model.save()
        learning_task.delete()

        return HttpResponse(
            json.dumps(
                {
                    "ml_model_id": ml_model.id,
                    "upload_valid_token": ml_model.valid_token_to_upload_files
                }
            )
        )

@csrf_exempt
def __COMPLETE_EXPLOIT_TASK_AND_GET_FILES(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        layer = channels.layers.get_channel_layer()
        print("trying to broadcast message through redis channel")
        async_to_sync(layer.group_send)("waiting_results", {
            "type": "results.get",
            "text": "Hello there"
        })
        return HttpResponse("OK")

@csrf_exempt
def __UPLOAD_MODEL_CONFIGURATION_FILE(request: HttpRequest) -> HttpResponse:
    allowed_filetypes = {
        'json': 'config_best_json_file',
        'encoder': 'encoder_best_file',
        'scaler': 'scaler_best_file',
        'model': 'model_best_file'
    }
    if request.method == "POST":
        upload_token = request.headers.get('token', '')
        model_id = int(request.headers.get('modelid', '-1'))
        filetype = request.headers.get('filetype', '')

        assert model_id != -1
        ml_model: MLMODEL = MLMODEL.objects.get(id=model_id)
        assert upload_token == ml_model.valid_token_to_upload_files
        assert filetype in allowed_filetypes.keys()

        file = request.FILES['file']
        file_name = default_storage.save(
            f"projects/{ml_model.user.username}/{ml_model.project_name}/{file.name}",
            file
        )
        ml_model.__setattr__(allowed_filetypes[filetype], file_name)
        ml_model.save()

        if ml_model.config_best_json_file is not None and\
            ml_model.encoder_best_file is not None and\
            ml_model.scaler_best_file is not None and\
            ml_model.model_best_file is not None:
            ml_model.ready_to_use = 1
            ml_model.save()
        return HttpResponse(
            "File was handled and saved correctly"
        )


def __get_ip_address(request) -> str:
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
