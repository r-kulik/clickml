import datetime
import traceback

from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse

from django.http import HttpRequest, HttpResponse, response, FileResponse, HttpResponseBase

from .BasePageContext import BasePageContext
from .ModelCreationSettingsContext import ModelCreationSettingsContext
from .TaskRegister import TaskRegister
from .ViewResultsContext import ViewResultsContext
from .UseModelContext import UseModelContext
from .WorkspaceMainPageContext import WorkspaceMainPageContext
from .models import ModelOnCreation,  MLMODEL, ExploitTask

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
                    'error_text': traceback.format_exc(),
                    'extended': True
                }
            )

    return wrapper


@errorHandler
def main(request: HttpRequest) -> HttpResponse:
    # (closed to_do): сделать редирект после POSt на GET, чтобы при обновлении страницы не отправлялась поторная задача обучения
    workspaceMainPageContext = WorkspaceMainPageContext(request)
    if request.method == 'POST':
        workspaceMainPageContext.addInfoFromTemporaryTable()
        workspaceMainPageContext.loadInformationAboutNewModel()
        task_register: TaskRegister = TaskRegister.fromWorkspaceMainPageContext(workspaceMainPageContext)
        task_registration_result = task_register.registerLearningTask()  # 0 - OK, -1 - Exception
        return redirect('/workspace')

    workspaceMainPageContext.loadInformationAboutExistingModels()
    workspaceMainPageContext.loadInformationAboutLearningModels()
    return TemplateResponse(
        request,
        "workspace_template.html",
        context={'context': workspaceMainPageContext}
    )



@errorHandler
def createNewModel(request) -> HttpResponse:
    createNewModelContext = CreateNewModelContext(request, is_workspace=True)
    # closed: сделать скрипт, который проверяет уникальность имени проекта: предотвратить регистрацию проектов с существующим именем
    # closed: запретить пользователю оставлять пустое название или не загружать файл. Сделать это через JS
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

@errorHandler
def useMlModel(request: HttpRequest) -> HttpResponse:
    model_id = int(request.GET.get("model_id", "-1"))
    model: MLMODEL = MLMODEL.objects.get(id=model_id)
    if request.user != model.user:
        return TemplateResponse(
            request,
            "unauthorized_access.html"
        )
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

    #TODO: устроить такой же обещанный редирект, как и на /workspace
    if request.method == 'POST':
        viewResultsContext = ViewResultsContext(request, is_workspace=True)
        task_register = TaskRegister.fromUseModelContext(viewResultsContext)
        task_register.registerExploitTask()
        return TemplateResponse(
            request,
            "view_results.html",
            context={'context': viewResultsContext}
        )



def downloadResults(request: HttpRequest) -> HttpResponseBase:
    #TODO устроить проверку доступа
    if request.method == "GET":
        exploit_task_id = request.GET.get("task_id", -1)

        print(exploit_task_id)
        exploit_task: ExploitTask = ExploitTask.objects.get(id=exploit_task_id)
        if request.user != exploit_task.user:
            return TemplateResponse(
                request,
                "unauthorized_access.html"
            )
        with open('result.csv', 'wb') as file:
            file.write(
                default_storage.open(
                    exploit_task.result_file_name
                ).read()
            )
        exploit_task.delete()
        return FileResponse(open('result.csv', 'rb'))


def returnYandexVerification(request) -> HttpResponse:
    return HttpResponse(
        """<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    </head>
    <body>Verification: 6e171de854288ea5</body>
</html>"""
    )