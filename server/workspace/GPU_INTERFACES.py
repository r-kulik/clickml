import datetime

from django.http import HttpResponse, HttpRequest, FileResponse

from .models import WorkingGpuRemoteServer, UploadTokens


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


def __get_ip_address(request) -> str:
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
