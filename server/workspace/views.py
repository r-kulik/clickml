import datetime
import traceback

from django.shortcuts import render
from django.template.response import TemplateResponse

from django.http import HttpRequest, HttpResponse, response, FileResponse

from .BasePageContext import BasePageContext
from .ModelCreationSettingsContext import ModelCreationSettingsContext
from .TaskRegister import TaskRegister
from .ViewResultsContext import ViewResultsContext
from .UseModelContext import UseModelContext
from .WorkspaceMainPageContext import WorkspaceMainPageContext
from .models import ModelOnCreation, WorkingGpuRemoteServer, MLMODEL

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
    # TODO: сделать редирект после POSt на GET, чтобы при обновлении страницы не отправлялась поторная задача обучения
    workspaceMainPageContext = WorkspaceMainPageContext(request)
    workspaceMainPageContext.loadInformationAboutExistingModels()
    if request.method == 'POST':
        workspaceMainPageContext.addInfoFromTemporaryTable()
        workspaceMainPageContext.loadInformationAboutNewModel()
        task_register: TaskRegister = TaskRegister.fromWorkspaceMainPageContext(workspaceMainPageContext)
        task_registration_result = task_register.registerLearningTask()  # 0 - OK, -1 - Exception
    return TemplateResponse(
        request,
        "workspace_template.html",
        context={'context': workspaceMainPageContext}
    )



@errorHandler
def createNewModel(request) -> HttpResponse:
    createNewModelContext = CreateNewModelContext(request, is_workspace=True)
    # TODO: сделать скрипт, который проверяет уникальность имени проекта: предотвратить регистрацию проектов с существующим именем
    # TODO: запретить пользователю оставлять пустое название или не загружать файл. Сделать это через JS
    return TemplateResponse(
        request,
        "create_new_model.html",
        context={'context': createNewModelContext}
    )


@errorHandler
def modelCreationSettings(request: HttpRequest) -> HttpResponse:
    #TODO: сделать так, чтоб пользователь обязательно выбрал тип задачи и целевую переменную
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

@errorHandler
def useMlModel(request: HttpRequest) -> HttpResponse:
    model_id = int(request.GET.get("model_id", "-1"))
    #TODO: проверка доступа
    useModelContext = UseModelContext(
        request,
        model_id,
        is_workspace=True
    )

    return TemplateResponse(
        request,
        "use_model.html",
        context={'context': useModelContext}
    )


@errorHandler
def viewResults(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        viewResultsContext = ViewResultsContext(request)
        task_register = TaskRegister.fromUseModelContext(viewResultsContext)
        task_register.registerExploitTask()

        return TemplateResponse(
            request,
            "view_results.html",
            context={'context': viewResultsContext}
        )
