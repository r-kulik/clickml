import requests
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import models
import secrets

import json

from . import ViewResultsContext, UseModelContext
from .WorkspaceMainPageContext import WorkspaceMainPageContext
from .errors import NoRunningGPUMachineException
from .models import LearningTask, UploadTokens, WorkingGpuRemoteServer, ExploitTask, MLMODEL


class TaskRegister:
    learning_task: LearningTask = None
    exploit_task: ExploitTask = None
    purpose: str

    def __init__(self) -> None:
        pass

    @staticmethod
    def fromWorkspaceMainPageContext(workspaceMainPageContext: WorkspaceMainPageContext):
        task_register = TaskRegister()
        file_tokens = UploadTokens.objects.filter(
            FILE_PATH=workspaceMainPageContext.currently_created_model_dataset_file_name
        )
        if len(file_tokens) > 0:
            for file_token in file_tokens: file_token.delete()
        token_note = UploadTokens(FILE_PATH=workspaceMainPageContext.currently_created_model_dataset_file_name,
                                  UPLOAD_TOKEN=secrets.token_urlsafe())
        token_note.save()

        task_register.learning_task = LearningTask(
            user=User.objects.get(username=workspaceMainPageContext.username),
            project_name=workspaceMainPageContext.currently_created_model_project_name,
            task_type=workspaceMainPageContext.task_type,
            target_variable=workspaceMainPageContext.target_variable,
            upload_token=token_note.UPLOAD_TOKEN,
            GPU_server_IP="",
            success=0
        )
        # print(f"\n\nAt the moment of creating TaskRegisterObject, target_variable={task_register.learning_task.target_variable}")
        task_register.purpose = "learn"
        return task_register

    def registerLearningTask(self) -> int:
        try:
            GPU_SERVER_IP = WorkingGpuRemoteServer.objects.order_by('LAST_REQUEST')[0].IP_ADDRESS
        except IndexError:
            raise NoRunningGPUMachineException()
        self.learning_task.GPU_server_IP = GPU_SERVER_IP
        self.learning_task.save()
        requestBody = {
            'task_id': self.learning_task.id,
            'task_type': self.learning_task.task_type,
            'target_variable': self.learning_task.target_variable,
            'source_file_upload_token': self.learning_task.upload_token
        }
        # print(json.dumps(requestBody))
        response = requests.post(
            url=f"http://{GPU_SERVER_IP}/register_learn_task",
            json=requestBody
        )
        print(response.text)
        if response.text == "OK":
            return 0
        else:
            return -1

        return response

    @staticmethod
    def fromUseModelContext(useModelContext: UseModelContext):
        task_register = TaskRegister()
        task_register.purpose= 'use'
        print(useModelContext.model_id)
        task_register.exploit_task = ExploitTask(
            user=useModelContext.request.user,
            ml_model=MLMODEL.objects.get(id=useModelContext.model_id),
            csv_file_name=useModelContext.exploit_file_name,
            GPU_SERVER_IP="",
            success=False
        )
        task_register.exploit_task.save()
        useModelContext.exploit_task_id = task_register.exploit_task.id
        return task_register

    def registerExploitTask(self) -> int:
        try:
            GPU_SERVER_IP = WorkingGpuRemoteServer.objects.order_by('LAST_REQUEST')[0].IP_ADDRESS
        except IndexError:
            raise NoRunningGPUMachineException()
        self.exploit_task.GPU_SERVER_IP = GPU_SERVER_IP
        self.exploit_task.save()

        response = requests.post(
            url=f"http://{GPU_SERVER_IP}/register_exploit_task",
            files={
                "exploit_file": (
                    f"{secrets.token_urlsafe()}.csv",
                    default_storage.open(self.exploit_task.csv_file_name)
                ),
                "json_config_file": (
                    f"{secrets.token_urlsafe()}.json",
                    default_storage.open(self.exploit_task.ml_model.config_best_json_file)
                ),
                "encoder_file": (
                    f"{secrets.token_urlsafe()}.pickle",
                    default_storage.open(self.exploit_task.ml_model.encoder_best_file)
                ),
                "scaler_file": (
                    f"{secrets.token_urlsafe()}.pickle",
                    default_storage.open(self.exploit_task.ml_model.scaler_best_file)
                ),
                "model_file": (
                    f"{secrets.token_urlsafe()}.pickle",
                    default_storage.open(self.exploit_task.ml_model.model_best_file)
                ),
                "task_id": (
                    f"task_id.txt",
                    f"{self.exploit_task.id}"
                )
            }
        )

        if response.text == "OK":
            return 0
        return -1

