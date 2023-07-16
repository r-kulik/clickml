from WorkWithTask import Task
import os


def clear_files_after_learning(task: Task):
    for i in os.listdir(f"task_{task.task_id}"):
        os.remove(f"task_{task.task_id}/{i}")

    for i in os.listdir(f"task_{task.task_id}_zip"):
        os.remove(f"task_{task.task_id}_zip/{i}")

    os.rmdir(f"task_{task.task_id}")
    os.rmdir(f"task_{task.task_id}_zip")


def clear_files_after_using(task: Task):
    for i in os.listdir(f"task_{task.task_id}"):
        os.remove(f"task_{task.task_id}/{i}")

    os.rmdir(f"task_{task.task_id}")

def clear_files_after_error(task_id):
    for i in os.listdir(f"task_{task_id}"):
        os.remove(f"task_{task_id}/{i}")

    os.rmdir(f"task_{task_id}")
