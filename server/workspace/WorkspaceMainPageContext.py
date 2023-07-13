from .models import ModelOnCreation
from .BasePageContext import BasePageContext


class WorkspaceMainPageContext(BasePageContext):

    def __init__(self, request) -> None:
        super().__init__(request)
        self.task_type = 'undefined'
        self.target_variable = 'undefined'
        self.currently_created_model_dataset_file_name = None
        self.currently_created_model_project_name = "undefined"
        self.is_workspace = True

    def loadInformationAboutNewModel(self) -> None:
        self.task_type = self.request.POST.get('task_type', 'undefined')
        self.target_variable = self.request.POST.get('target_variable', 'undefined')

    def addInfoFromTemporaryTable(self) -> None:
        information_object: ModelOnCreation = ModelOnCreation.objects.filter(username=self.username)[0]
        print(information_object.project_name)
        self.currently_created_model_dataset_file_name = information_object.dataset_file_name
        self.currently_created_model_project_name = information_object.project_name
