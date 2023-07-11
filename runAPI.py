import sys
import traceback

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import threading
import APICONFIG
import run_main
import logging

logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

class APILearnTask(BaseModel):
    task_id: int
    task_type: str
    target_variable: str
    source_file_upload_token: str


app = FastAPI()
response = requests.get(f'http://{APICONFIG.site_host}/enter_as_gpu_machine')
logging.info('connection request was sent')
if response.status_code != 200:
    sys.exit()


@app.post("/register_learn_task")
async def registerLearnTask(jsonFile: APILearnTask):
    try:
        learning_task_thread = threading.Thread(
            target=registerTask,
            args=[jsonFile]
        )
        learning_task_thread.start()
        return "OK"
    except Exception as e:
        logging.info(traceback.format_exc())
        return "EXC"


@app.get('/')
def index():
    return "Hello, world!"


def registerTask(task) -> None:
    response = requests.get(
        f'http://{APICONFIG.site_host}/get_dataset_file?UPLOAD_TOKEN={task.source_file_upload_token}'
    )
    logging.info("responce with the file had arrived")
    if response.text == "some exception has occured":
        raise FileNotFoundError
    file_address = f"tmp/{task.source_file_upload_token}.csv"
    with open(file_address, 'wb') as file:
        file.write(response.content)
    run_main.run_app(task)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)
