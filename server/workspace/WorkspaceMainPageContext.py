from .models import ModelOnCreation


class WorkspaceMainPageContext:

    def __init__(self, request) -> None:
        self.request = request
        self.username = self.request.user.get_username()
        self.task_type = 'undefined'
        self.target_variable = 'undefined'
        self.currently_created_model_dataset_file = None
        self.currently_created_model_project_name = "undefined"

    def loadInformationAboutNewModel(self) -> None:
        self.task_type = self.request.POST.get('task_type', 'undefined')
        self.target_variable = self.request.POST.get('target_variable', 'undefined')

    def addInfoFromTemporaryTable(self) -> None:
        information_object: ModelOnCreation = ModelOnCreation.objects.filter(username=self.username)[0]
        print(information_object.dataset_file)
        print(information_object.project_name)
        self.currently_created_model_dataset_file = information_object.dataset_file
        self.currently_created_model_project_name = information_object.project_name
