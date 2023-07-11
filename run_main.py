from WorkWithTask import Task
from OptunaPreprocessing import OptunaWork
from JsTask import APILearnTask

from sklearn import metrics


def print_clf_metrics(y_actual, y_pred):
    print(f'Testing accuracy = {metrics.accuracy_score(y_actual, y_pred)}')
    print(f'Testing precision = {metrics.precision_score(y_actual, y_pred)}')
    print(f'Testing recall = {metrics.recall_score(y_actual, y_pred)}')
    print(f'Testing F1-score = {metrics.f1_score(y_actual, y_pred)}')


def run_app(js_task: APILearnTask):
    task = Task(js_task)

    if task.is_correct:
        OptunaWork(task, 200).optuna_study()
