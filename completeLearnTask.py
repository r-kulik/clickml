import json
import sys

import requests
from APICONFIG import site_host
from JsTask import APILearnTask


def completeLearnTask(task: APILearnTask) -> int:
    response = requests.post(
        url=f'http://{site_host}/complete_learning_task_and_get_files',
        json={
            'task_id': task.task_id
        }
    )
    if response.status_code != 200:
        print('response code is not 200')
        return -1

    responce_data = json.loads(response.text)
    folder_name=f"task_{task.task_id}"
    result = uploadFile(
        responce_data.get('upload_valid_token'),
        responce_data.get('ml_model_id'),
        f"{folder_name}/config_best.json",
        'json_config'
    )
    if result == -1:
        sys.exit() #TODO: убрать системный выход и заменить на обработку ошибки




def uploadFile(token: str, model_id: int, filename:str, filetype: str):
    response = requests.post(
        url=f'http://{site_host}/upload_model_configuration_file',
        json={
            'token': token,
            'model_id': model_id,
            'filetype': filetype
        },
        files={'file': open(filename)}
    )
    if response.status_code != 200:
        print(response.text)
        return -1
    return 0