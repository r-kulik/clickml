import sys
import traceback

import fastapi
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import threading
from WorkWithTask import registerTask
import APICONFIG


class APILearnTask(BaseModel):
    task_id: int
    task_type: str
    target_variable: str
    source_file_upload_token: str


class TestUserModel(BaseModel):
    user: str

app = FastAPI()
response = requests.get(f'http://{APICONFIG.site_host}/enter_as_gpu_machine')
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
        print(traceback.format_exc())
        return "EXC"


@app.get('/')
def index():
    return "Hello, world!"


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)


