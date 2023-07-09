from django.template.response import TemplateResponse

from django.http import HttpRequest, HttpResponse

from .ModelCreationSettingsContext import ModelCreationSettingsContext


class WorkspaceMainPageContext:
    def __init__(self, request) -> None:
        self.request = request
        self.username = self.request.user.get_username()


class CreateNewModelContext:

    def __init__(self, request) -> None:
        self.request = request
        self.username = self.request.user.get_username()

# Create your views here.

def main(request: HttpRequest) -> HttpResponse:
    workspaceContext = WorkspaceMainPageContext(request)

    return TemplateResponse(
        request,
        "workspace_template.html",
        context={'context': workspaceContext}
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
        # print(file.read())
        return TemplateResponse(
            request,
            "model_settings.html",
            context={'context': creationContext}
        )
    return "<p> Error <p>"