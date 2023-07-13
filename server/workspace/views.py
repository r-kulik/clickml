import datetime
import traceback

from django.shortcuts import render
from django.template.response import TemplateResponse


from django.http import HttpRequest, HttpResponse, response, FileResponse

from .BasePageContext import BasePageContext
from .ModelCreationSettingsContext import ModelCreationSettingsContext
from .TaskRegister import TaskRegister
from .WorkspaceMainPageContext import WorkspaceMainPageContext
from .models import ModelOnCreation, WorkingGpuRemoteServer

from .CreateNewModelContext import CreateNewModelContext

# Create your views here.


def errorHandler(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            return TemplateResponse(
                *args,
                "error_message.html",
                context={
                    'error': str(e),
                    'context': BasePageContext(*args, *kwargs, is_workspace=True),
                    'error_text': traceback.format_exc()
                }
            )
    return wrapper

@errorHandler
def main(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        workspaceMainPageContext = WorkspaceMainPageContext(request)
        workspaceMainPageContext.loadInformationAboutNewModel()
        workspaceMainPageContext.addInfoFromTemporaryTable()

        task_register: TaskRegister = TaskRegister.fromWorkspaceMainPageContext(workspaceMainPageContext)
        task_registrarion_result = task_register.registerLearningTask() #0 - OK, -1 - Exception
        print(task_registrarion_result)
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


@errorHandler
def createNewModel(request) -> HttpResponse:
    createNewModelContext = CreateNewModelContext(request, is_workspace=True)

    return TemplateResponse(
        request,
        "create_new_model.html",
        context={'context': createNewModelContext}
    )


@errorHandler
def modelCreationSettings(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        creationContext = ModelCreationSettingsContext(request, is_workspace=True)
        temporary_information = ModelOnCreation(
            username=creationContext.username,
            project_name=creationContext.project_name,
            dataset_file_name=creationContext.dataset_file_name
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


