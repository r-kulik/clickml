from .BasePageContext import BasePageContext
from .models import MLMODEL, LearningTask


class CreateNewModelContext(BasePageContext):



    def __init__(self, request, **kwargs) -> None:
        super().__init__(request, **kwargs)
        self.request = request
        self.forbidden_project_names: list[str] = []
        self.updateForbiddenProjectNames()

    def updateForbiddenProjectNames(self) -> None:
        ml_models: list[MLMODEL] = MLMODEL.objects.filter(
            user=self.request.user
        )
        for ml_model in ml_models:
            self.forbidden_project_names.append(
                ml_model.project_name
            )

        learning_tasks: list[LearningTask] = LearningTask.objects.filter(
            user=self.request.user
        )
        for learning_task in learning_tasks:
            self.forbidden_project_names.append(
                learning_task.project_name
            )
