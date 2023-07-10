import datetime

from django.shortcuts import render
from django.template.response import TemplateResponse


from django.http import HttpRequest, HttpResponse, response

from .ModelCreationSettingsContext import ModelCreationSettingsContext
from .TaskRegister import TaskRegister
from .WorkspaceMainPageContext import WorkspaceMainPageContext
from .models import ModelOnCreation, WorkingGpuRemoteServer


class CreateNewModelContext:

    def __init__(self, request) -> None:
        self.request = request
        self.username = self.request.user.get_username()

# Create your views here.

def main(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        workspaceMainPageContext = WorkspaceMainPageContext(request)
        workspaceMainPageContext.loadInformationAboutNewModel()
        workspaceMainPageContext.addInfoFromTemporaryTable()

        task_register = TaskRegister.fromWorkspaceMainPageContext(workspaceMainPageContext)
        task_register.registerLearningTask()

        return TemplateResponse(
            request,
            "workspace_template.html",
            context={'context': workspaceMainPageContext}
        )

    return TemplateResponse(
        request,
        "workspace_template.html",
        context={'context': WorkspaceMainPageContext(request)}
    )


def createNewModel(request) -> HttpResponse:
    createNewModelContext = CreateNewModelContext(request)

    return TemplateResponse(
        request,
        "create_new_model.html"
    )


def modelCreationSettings(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        creationContext = ModelCreationSettingsContext(request)
        temporary_information = ModelOnCreation(
            username=creationContext.username,
            project_name=creationContext.project_name,
            dataset_file=creationContext.dataset_file
        )
        temporary_information.deletePreviousIfExists()
        temporary_information.save()
        # print(file.read())
        return TemplateResponse(
            request,
            "model_settings.html",
            context={'context': creationContext}
        )
    return "<p> Error <p>"


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


def __get_ip_address(request) -> str:
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
