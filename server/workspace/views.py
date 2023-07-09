from django.template.response import TemplateResponse

from django.http import HttpRequest, HttpResponse

from .ModelCreationSettingsContext import ModelCreationSettingsContext
from .ModelOnCreation import ModelOnCreation
from .WorkspaceMainPageContext import WorkspaceMainPageContext


class CreateNewModelContext:

    def __init__(self, request) -> None:
        self.request = request
        self.username = self.request.user.get_username()

# Create your views here.

def main(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        print('went to POST branch')
        workspaceMainPageContext = WorkspaceMainPageContext(request)
        workspaceMainPageContext.loadInformationAboutNewModel()
        workspaceMainPageContext.addInfoFromTemporaryTable()
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