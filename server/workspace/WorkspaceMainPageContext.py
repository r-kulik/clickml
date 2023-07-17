import datetime

from .models import ModelOnCreation, MLMODEL, LearningTask
from .BasePageContext import BasePageContext


class MlModelContext:
    model_id: int
    name: str
    creation_time: datetime.datetime

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)


class LearningTaskContext:
    learning_task_id: int
    name: str
    progress_value_element_id: str
    metric_value_element_id: str
    learning_model_id_value_element_id: str

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
        self.ml_model_contexts: list[MlModelContext] = []
        self.learning_task_contexts: list[LearningTaskContext] = []

    def loadInformationAboutNewModel(self) -> None:
        self.task_type = self.request.POST.get('task_type', 'undefined')
        self.target_variable = self.request.POST.get('target_variable', 'undefined')

    def addInfoFromTemporaryTable(self) -> None:
        information_object: ModelOnCreation = ModelOnCreation.objects.filter(username=self.username)[0]
        print(information_object.project_name)
        self.currently_created_model_dataset_file_name = information_object.dataset_file_name
        self.currently_created_model_project_name = information_object.project_name

    def loadInformationAboutExistingModels(self) -> None:
        MLMODELS: list[MLMODEL] = MLMODEL.objects.filter(user=self.request.user).order_by("-creation_time")
        print(f"I found {len(MLMODELS)} ml_models for given user")
        for ml_model in MLMODELS:
            self.ml_model_contexts.append(
                MlModelContext(
                    name=ml_model.project_name,
                    model_id = ml_model.id,
                    creation_time = ml_model.creation_time
                )
            )

    def loadInformationAboutLearningModels(self) -> None:
        learning_tasks: list[LearningTask] = LearningTask.objects.filter(user=self.request.user)
        for learning_task in learning_tasks:
            self.learning_task_contexts.append(
                LearningTaskContext(
                    learning_task_id = learning_task.id,
                    name = learning_task.project_name,
                    progress_value_element_id = f"progress_value_element_{learning_task.id}",
                    metric_value_element_id = f"metric_value_element_id_{learning_task.id}",
                    learning_model_id_value_element_id = f"learning_model_id_value_element_id_{learning_task.id}"
                )
            )
