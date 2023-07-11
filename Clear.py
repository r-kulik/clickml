from WorkWithTask import Task
import os


def clear_files_after_learning(task: Task):
    os.remove(f"tmp/{task.source_file_upload_token}.csv")

    for i in os.listdir(f"task_{task.task_id}"):
        os.remove(f"task_{task.task_id}/{i}")

    os.rmdir(f"task_{task.task_id}")