import os
import shutil
import time
import traceback
from typing import Optional
from run_main import run_app
import cpuinfo
from sklearnex import patch_sklearn

import requests
from APICONFIG import site_host
from WorkWithTask import Task

from MessageSending import send_error_message


class ServerWrongResponseException(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self) -> str:
        return f"SERVER WRONG RESPONCE \n {self.response.text}"


def main() -> None:
    if "Intel" in cpuinfo.get_cpu_info()["brand_raw"]:
        patch_sklearn()

    counter = 0
    while True:
        counter += 1
        time.sleep(2)
        try:
            if counter == 5:
                counter = 0
                task = get_learn_task()
            else:
                task = get_exploit_task()
        except:
            continue

        try:
            if task is not None:
                run_app(task)
        except Exception as e:
            send_error_message(e, task.task_id, task.purpose)


def get_learn_task() -> Optional[Task]:
    response = requests.get(url=f"http://{site_host}/get_learning_task")
    if response.status_code != 200:
        raise ServerWrongResponseException(response)
    if response.text == "NO TASKS":
        return None

    task_id = response.headers["Taskid"]

    try:

        if not os.path.exists(os.path.join(os.curdir, f"task_{task_id}")):
            os.mkdir(f"task_{task_id}")

        with open(f"task_{task_id}/df.csv", "wb") as f:
            f.write(response.content)

        task = Task(task_id,
                    "learn",
                    response.headers["Tasktype"],
                    response.headers["Targetvariable"],
                    f"task_{task_id}/df.csv")
    except Exception as e:
        send_error_message(e, int(task_id), "learn")
        return None

    return task


def get_exploit_task() -> Optional[Task]:
    response = requests.get(url=f"http://{site_host}/get_exploit_task")
    if response.status_code != 200:
        raise ServerWrongResponseException(response)
    if response.text == "NO TASKS":
        return None

    task_id = response.headers["Taskid"]
    try:

        zip_file_response = requests.get(
            url=f"http://{site_host}/get_exploit_task_model_files",
            params={
                "task_id": task_id
            }
        )

        if not os.path.exists(os.path.join(os.curdir, f"task_{task_id}")):
            os.mkdir(f"task_{task_id}")

        with open(f"task_{task_id}/task_{task_id}.csv", "wb") as f:
            f.write(response.content)
        with open(f"task_{task_id}/task.zip", "wb") as f:
            f.write(zip_file_response.content)

        shutil.unpack_archive(f"task_{task_id}/task.zip", f"task_{task_id}")

        task = Task(task_id,
                    "use",
                    None,
                    None,
                    f"task_{task_id}/task_{task_id}.csv")
    except Exception as e:
        send_error_message(e, int(task_id), "use")
        return None

    return task


if __name__ == "__main__":
    main()