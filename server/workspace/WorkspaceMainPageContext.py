import datetime

from .models import ModelOnCreation, MLMODEL
from .BasePageContext import BasePageContext


class MlModelContext:
    model_id: int
    name: str
    creation_time: datetime.datetime

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


class WorkspaceMainPageContext(BasePageContext):

    def __init__(self, request) -> None:
        super().__init__(request)
        self.task_type = 'undefined'
        self.target_variable = 'undefined'
        self.currently_created_model_dataset_file_name = None
        self.currently_created_model_project_name = "undefined"
        self.is_workspace = True
        self.ml_model_contexts= []

    def loadInformationAboutNewModel(self) -> None:
        self.task_type = self.request.POST.get('task_type', 'undefined')
        self.target_variable = self.request.POST.get('target_variable', 'undefined')

    def addInfoFromTemporaryTable(self) -> None:
        information_object: ModelOnCreation = ModelOnCreation.objects.filter(username=self.username)[0]
        print(information_object.project_name)
        self.currently_created_model_dataset_file_name = information_object.dataset_file_name
        self.currently_created_model_project_name = information_object.project_name

    def loadInformationAboutExistingModels(self) -> None:
        MLMODELS: list[MLMODEL] = MLMODEL.objects.filter(user=self.request.user, ready_to_use=1)
        print(f"I found {len(MLMODELS)} ml_models for given user")
        for ml_model in MLMODELS:
            self.ml_model_contexts.append(
                MlModelContext(
                    name=ml_model.project_name,
                    model_id = ml_model.id,
                    creation_time = ml_model.creation_time
                )
            )
