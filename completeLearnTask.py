import requests
from APICONFIG import site_host
import shutil
from WorkWithTask import Task
from Clear import clear_files_after_learning


def complete_learn_task(task: Task) -> int:

    shutil.make_archive(f"task_{task.task_id}_zip/task_{task.task_id}", "zip", f"task_{task.task_id}")


    response = requests.post(
        url=f'http://{site_host}/complete_learning_task',
        headers={
            'taskid': str(task.task_id)
        },
        files={"file": open(f"task_{task.task_id}_zip/task_{task.task_id}.zip", 'rb')}
    )
    if response.status_code != 200:
        print('response code is not 200')
        return -1

    clear_files_after_learning(task)
    return 0





