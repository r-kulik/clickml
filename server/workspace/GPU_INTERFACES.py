import datetime
import json
import os
import secrets

import channels.layers
import requests
from django.http import HttpResponse, HttpRequest, FileResponse, HttpResponseBase
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt

from asgiref.sync import async_to_sync

from .models import LearningTask, MLMODEL, ExploitTask


@csrf_exempt
def __COMPLETE_LEARNING_TASK_AND_GET_FILES(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        learning_task_id = int(request.headers.get('taskid', -1))
        assert learning_task_id != -1
        print(f'GET A COMPLETION OF TASK #{learning_task_id}')
        learning_task: LearningTask = LearningTask.objects.get(id=learning_task_id)
        learning_task.success = 1

        zip_file_name = default_storage.save(
            f'projects/{learning_task.user.username}/{secrets.token_urlsafe()}.zip',
            request.FILES['file']
        )

        ml_model = MLMODEL(
            user = learning_task.user,
            project_name = learning_task.project_name,
            model_zip_file=zip_file_name,
            creation_time=datetime.datetime.now(),
            model_main_metric_name="UNDEFINED METRIC",
            model_main_metric_value=0,
            model_task_type=learning_task.task_type
        )
        ml_model.save()
        learning_task.delete()

        layer = channels.layers.get_channel_layer()
        async_to_sync(layer.group_send)("waiting_learning_task_info", {
            "type": "complete",
            "text": json.dumps({"learning_task_id": learning_task_id, "ml_model_id": ml_model.id})
        })

        return HttpResponse("OK")




@csrf_exempt
def __COMPLETE_EXPLOIT_TASK_AND_GET_FILES(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        layer = channels.layers.get_channel_layer()

        task_id = int(request.headers.get('taskid', '-1'))
        assert task_id != -1

        exploit_task: ExploitTask = ExploitTask.objects.get(id=task_id)
        exploit_task.result_file_name = default_storage.save(f"results/{secrets.token_urlsafe()}.csv", request.FILES['file'])
        exploit_task.success = True
        exploit_task.save()

        # print("trying to broadcast message through redis channel")
        async_to_sync(layer.group_send)("waiting_results", {
            "type": "results.get",
            "text": json.dumps({"task_id": exploit_task.id,
                 "success": exploit_task.success})
        })
        return HttpResponse("OK")


@csrf_exempt
def __ACCEPT_PERCENT(request: HttpRequest) -> HttpResponse:
    learning_task_id = int(request.GET.get('learning_task_id'))
    completion_percentage = float(request.GET.get('completion_percentage'))
    main_metric_value = float(request.GET.get('main_metric_value'))

    layer = channels.layers.get_channel_layer()
    async_to_sync(layer.group_send)("waiting_learning_task_info", {
        "type": "info.get",
        "text": json.dumps({"learning_task_id": learning_task_id,
                            "completion_percentage": completion_percentage,
                            "main_metric_value": main_metric_value})
    })
    return HttpResponse("OK")

@csrf_exempt
def __GET_LEARNING_TASK(request: HttpRequest) -> HttpResponseBase:

    task_pool: list[LearningTask] = LearningTask.objects.filter(GPU_SERVER_IP = "")
    if len(task_pool) == 0:
        return HttpResponse("NO TASKS");
    learning_task: LearningTask = task_pool[0];
    learning_task.GPU_server_IP = __get_ip_address(request)
    learning_task.request_time = datetime.datetime.now()
    learning_task.save()

    return FileResponse(
        default_storage.open(learning_task.dataset_source_file_name),
        headers={
            'Content-Disposition': 'attachment; filename="dataset.csv"',
            "taskid": learning_task.id,
            "tasktype": learning_task.task_type,
            "targetvariable": learning_task.target_variable,
            "mainmetricname": learning_task.main_metric_name
        },
    )


def __GET_EXPLOIT_TASK(request: HttpRequest) -> HttpResponseBase:
    exploit_tasks: list[ExploitTask] = ExploitTask.objects.filter(GPU_SERVER_IP = "", success = False)
    if len(exploit_tasks) == 0:
        return HttpResponse("NO TASKS")
    exploit_task: ExploitTask = exploit_tasks[0]
    exploit_task.GPU_SERVER_IP = __get_ip_address(request)
    exploit_task.request_time = datetime.datetime.now()
    exploit_task.save()

    return FileResponse(
        default_storage.open(
            exploit_task.csv_file_name
        ),
        headers={
            'Content-Disposition': 'attachment; filename="dataset.csv"',
            "taskid": exploit_task.id,
        }
    )


def __GET_EXPLOIT_TASK_MODEL_FILES(request: HttpRequest) -> HttpResponseBase:
        task_id=int(request.GET.get('task_id', '-1'))
        assert task_id != -1
        exploit_task: ExploitTask = ExploitTask.objects.get(id=task_id)
        return FileResponse(
            default_storage.open(
                exploit_task.ml_model.model_zip_file
            ),
            headers={
                'Content-Disposition': 'attachment; filename="dataset.csv"',
                "taskid": exploit_task.id,
            }
        )

@csrf_exempt
def __REPORT_LEARNING_TASK_EXCEPTION(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        json_data = json.loads(request.body)
        task_id = int(json_data.get('taskId', '-1'))
        learning_task: LearningTask = LearningTask.objects.get(id=task_id)

        layer = channels.layers.get_channel_layer()
        async_to_sync(layer.group_send)("waiting_learning_task_info", {
            "type": "exception.occurred",
            "text": json.dumps({
                "learning_task_id": learning_task.id,
                "exception": json_data.get('exceptionText', "Some exception has been occurred")
            })
        })
        learning_task.delete()
        return HttpResponse("Exception handled")

@csrf_exempt
def __REPORT_EXPLOIT_TASK_EXCEPTION(request:HttpRequest) -> HttpResponse:
    if request.method == "POST":
        json_data = json.loads(request.body)
        task_id = int(json_data.get('taskId', '-1'))
        exploit_task: ExploitTask = ExploitTask.objects.get(id=task_id)

        layer = channels.layers.get_channel_layer()
        async_to_sync(layer.group_send)("waiting_results", {
            "type": "exception.occurred",
            "text": json.dumps({
                "learning_task_id": exploit_task.id,
                "exception": json_data.get('exceptionText', "Some exception has been occurred")
            })
        })
        exploit_task.delete()
        return HttpResponse("Exception handled")

def __get_ip_address(request) -> str:
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
        port = user_ip_address.split(',')[1]
    else:
        ip = request.META.get('REMOTE_ADDR')
        port = request.META.get('REMOTE_PORT')
    return ip, port
