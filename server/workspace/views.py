from django.template.response import TemplateResponse

from django.http import HttpRequest, HttpResponse


class WorkspaceMainPageContext:
    def __init__(self, request) -> None:
        self.request = request
        self.username = self.request.user.get_username()


# Create your views here.

def main(request) -> HttpResponse:
    workspaceContext = WorkspaceMainPageContext(request)

    return TemplateResponse(
        request,
        "workspace_template.html",
        context={'context': workspaceContext}
    )