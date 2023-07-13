import sys
import traceback

import uvicorn
from fastapi import FastAPI
import requests
import threading
import APICONFIG
import run_main
import logging

from JsTask import APILearnTask

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

app = FastAPI()
response = requests.get(f'http://{APICONFIG.site_host}/enter_as_gpu_machine')
logging.info('connection request was sent')
if response.status_code != 200:
    sys.exit()


@app.post("/register_learn_task")
async def register_learn_task(json_file: APILearnTask):
    print(f"json_file.target_variable = {json_file.target_variable}")
    try:
        learning_task_thread = threading.Thread(
            target=register_task,
            args=[json_file]
        )
        learning_task_thread.start()
        return "OK"
    except Exception as _:
        logging.info(traceback.format_exc())
        return "EXC"


@app.get('/')
def index():
    return "Hello, world!"


def register_task(task) -> None:
    response = requests.get(
        f'http://{APICONFIG.site_host}/get_dataset_file?UPLOAD_TOKEN={task.source_file_upload_token}'
    )
    logging.info("responce with the file had arrived")
    if response.text == "some exception has occured":
        raise FileNotFoundError
    file_address = f"tmp/{task.source_file_upload_token}.csv"
    with open(file_address, 'wb') as file:
        file.write(response.content)
    run_main.run_app(task, purpose="learn")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)
