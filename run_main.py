import threading
from Test import *
from WorkWithTask import Task
from OptunaPreprocessing import OptunaWork
from Predict import Predict
from completeLearnTask import complete_learn_task
from completeExploitTask import complete_exploit_task
from Clear import *


def run_app(task: Task) -> None:
    if task.purpose == "learn":
        OptunaWork(task, 100).optuna_study()
        complete_learn_task(task)
    if task.purpose == "use":
        Predict(task).predict()

        web_thread = threading.Thread(
            target=complete_exploit_task,
            args=[task]
        )
        web_thread.start()
