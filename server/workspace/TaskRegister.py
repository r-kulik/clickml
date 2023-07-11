import requests
from django.contrib.auth.models import User
from django.db import models
import secrets

import json

from .WorkspaceMainPageContext import WorkspaceMainPageContext
from .models import LearningTask, UploadTokens, WorkingGpuRemoteServer


class TaskRegister:
    learning_task: LearningTask = None
    purpose: str

    def __init__(self) -> None:
        pass

    @staticmethod
    def fromWorkspaceMainPageContext(workspaceMainPageContext: WorkspaceMainPageContext):
        task_register = TaskRegister()
        file_tokens = UploadTokens.objects.filter(
            FILE_PATH=workspaceMainPageContext.currently_created_model_dataset_file
        )
        if len(file_tokens) > 0:
            for file_token in file_tokens: file_token.delete()
        token_note = UploadTokens(FILE_PATH=workspaceMainPageContext.currently_created_model_dataset_file,
                                  UPLOAD_TOKEN=secrets.token_urlsafe())
        token_note.save()
        #  print(workspaceMainPageContext.username)
        task_register.learning_task = LearningTask(
            user=User.objects.filter(username=workspaceMainPageContext.username)[0],
            project_name=workspaceMainPageContext.currently_created_model_project_name,
            task_type=workspaceMainPageContext.task_type,
            target_variable=workspaceMainPageContext.target_variable,
            upload_token=token_note.UPLOAD_TOKEN,
            GPU_server_IP="",
            success=0
        )
        task_register.purpose = "learn"
        return task_register

    def registerLearningTask(self) -> int:

        GPU_SERVER_IP = WorkingGpuRemoteServer.objects.order_by('LAST_REQUEST')[0].IP_ADDRESS
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

        # TODO: защитить систему от падения в результате выключения работы GPU-машины (переключение на следующую
        #  машину. лист ожидания при необходимости)

        return response
