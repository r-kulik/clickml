import json
import sys

import requests
from APICONFIG import site_host
from JsTask import APILearnTask


def complete_learn_task(task: APILearnTask) -> int:
    print(
        f"""
        GOING TO COMPLETE TASSK {task.task_id}
        """
    )
    response = requests.post(
        url=f'http://{site_host}/complete_learning_task_and_get_files',
        headers={
            'taskid': str(task.task_id)
        }
    )
    if response.status_code != 200:
        print('response code is not 200')
        return -1

    responce_data = json.loads(response.text)
    folder_name = f"task_{task.task_id}"

    for filename_type_pair in [
        (f"{folder_name}/config_best.json", 'json'),
        (f"{folder_name}/encoder_best.pickle", "encoder"),
        (f"{folder_name}/scaler_best.pickle", "scaler"),
        (f"{folder_name}/model_best.pickle", "model")
    ]:

        result = upload_file(
            responce_data.get('upload_valid_token'),
            responce_data.get('ml_model_id'),
            filename_type_pair[0],
            filename_type_pair[1]
        )
        if result == -1:
            sys.exit()  # TODO: убрать системный выход и заменить на обработку ошибки


def upload_file(token: str, model_id: int, filename: str, filetype: str):
    response = requests.post(
        url=f'http://{site_host}/upload_model_configuration_file',
        headers={
            'token': token,
            'modelid': str(model_id),
            'filetype': filetype
        },
        files={
            'file': open(filename)
        }
    )
    if response.status_code != 200:
        # print(response.text)
        return -1
    return 0
