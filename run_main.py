import traceback

import pandas as pd

from Predict_old import PredictOld
from Test import *

from WorkWithTask import Task
from OptunaPreprocessing import OptunaWork
from JsTask import APILearnTask
from Predict import Predict
from Predict_old import PredictOld

from sklearn import metrics

from completeLearnTask import complete_learn_task
from  completeExploitTask import complete_exploit_task
from Clear import *

import cpuinfo
from sklearnex import patch_sklearn
import ChooseBest


def print_clf_metrics(y_actual, y_pred):
    print(f'Testing accuracy = {metrics.accuracy_score(y_actual, y_pred)}')
    print(f'Testing precision = {metrics.precision_score(y_actual, y_pred)}')
    print(f'Testing recall = {metrics.recall_score(y_actual, y_pred)}')
    print(f'Testing F1-score = {metrics.f1_score(y_actual, y_pred)}')


def print_reg_metrics(y_actual, y_pred):
    print(f'Testing MSE = {metrics.mean_squared_error(y_actual, y_pred)}')
    print(f'Testing R2 = {metrics.r2_score(y_actual, y_pred)}')


def run_app(purpose: str, js_task: APILearnTask = None, task_id: int = None) -> None:
    if "Intel" in cpuinfo.get_cpu_info()["brand_raw"]:
        patch_sklearn()

    if purpose == "learn":
        task = Task(js_task)
        OptunaWork(task, 100).optuna_study()
        complete_learn_task(js_task.task_id)
        clear_files_after_learning(task)
    if purpose == "use":
        Predict(task_id).predict()
        #complete_exploit_task(task_id)
        clear_files_after_using(task_id)


# for test only
def run_test(scenario: int):
    task = choose_scenario(scenario)

    if "Intel" in cpuinfo.get_cpu_info()["brand_raw"]:
        patch_sklearn()

    if task.purpose == "learn":
        OptunaWork(task, 200).optuna_study()

    if task.purpose == "use":
        ChooseBest.choose_best(task, 1)
        true_y = task.df[task.target_variable]
        task.df = task.df.drop(task.target_variable, axis=1)
        a = PredictOld(task)
        b = a.predict()
        if task.task_type == "classification":
            print_clf_metrics(true_y, b)
        else:
            print_reg_metrics(true_y, b)


if __name__ == "__main__":
    run_test(8)

    """
    0 - cars - class
    1 - titanic - class
    2 - diamonds - multy class
    3 - california - regression
    4 - use cars
    5 - use california
    6 - use pokemon
    7 - learn pokemon
    8 - use titanic
    """
