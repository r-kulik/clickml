import datetime

import requests
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models
import secrets

import json

from . import ViewResultsContext, UseModelContext
from .WorkspaceMainPageContext import WorkspaceMainPageContext
from .models import LearningTask, ExploitTask, MLMODEL


class TaskRegister:
    learning_task: LearningTask = None
    exploit_task: ExploitTask = None
    purpose: str

    def __init__(self) -> None:
        pass

    @staticmethod
    def fromWorkspaceMainPageContext(workspaceMainPageContext: WorkspaceMainPageContext):
        task_register = TaskRegister()

        task_register.learning_task = LearningTask(
            user=User.objects.get(username=workspaceMainPageContext.username),
            project_name=workspaceMainPageContext.currently_created_model_project_name,
            task_type=workspaceMainPageContext.task_type,
            target_variable=workspaceMainPageContext.target_variable,
            dataset_source_file_name=workspaceMainPageContext.currently_created_model_dataset_file_name,
            GPU_SERVER_IP="",
            success=0,
            request_time=datetime.datetime.now()
        )
        # print(f"\n\nAt the moment of creating TaskRegisterObject, target_variable={task_register.learning_task.target_variable}")
        task_register.purpose = "learn"
        return task_register

    def registerLearningTask(self) -> int:
        self.learning_task.GPU_server_IP = ""
        self.learning_task.save()

    @staticmethod
    def fromUseModelContext(useModelContext: UseModelContext):
        task_register = TaskRegister()
        task_register.purpose = 'use'
        print(useModelContext.model_id)
        task_register.exploit_task = ExploitTask(
            user=useModelContext.request.user,
            ml_model=MLMODEL.objects.get(id=useModelContext.model_id),
            csv_file_name=useModelContext.exploit_file_name,
            GPU_SERVER_IP="",
            success=False,
            result_file_name="/",
            request_time=datetime.datetime.now()
        )
        task_register.exploit_task.save()
        useModelContext.exploit_task_id = task_register.exploit_task.id

        return task_register

    def registerExploitTask(self) -> int:
        self.exploit_task.save()
        return 0
