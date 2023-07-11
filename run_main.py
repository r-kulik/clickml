import pandas as pd
import os

from WorkWithTask import Task
from OptunaPreprocessing import OptunaWork
from JsTask import APILearnTask
from Predict import Predict

from sklearn import metrics

from completeLearnTask import completeLearnTask


def print_clf_metrics(y_actual, y_pred):
    print(f'Testing accuracy = {metrics.accuracy_score(y_actual, y_pred)}')
    print(f'Testing precision = {metrics.precision_score(y_actual, y_pred)}')
    print(f'Testing recall = {metrics.recall_score(y_actual, y_pred)}')
    print(f'Testing F1-score = {metrics.f1_score(y_actual, y_pred)}')


def run_app(js_task: APILearnTask):
    task = Task(js_task)

    if task.is_correct:
        OptunaWork(task, 2).optuna_study()
        completeLearnTask(js_task)



class T:
    def __init__(self):
        # fill this field
        self.purpose = "learn"  # or use
        self.task_type = "regression"  # or classification
        self.target_variable = "price"  # input by your self
        self.file_name = "tmp/california_train"  # input by your self

        # don't touch
        self.df = pd.read_csv(f"{self.file_name}.csv")
        self.task_id = 15
        self.__create_dir()

    def __create_dir(self) -> None:
        if self.task_id not in os.listdir(path='.'):
            os.mkdir(f"task_{self.task_id}")

# for test only
def run_test():
    task = T()

    if task.purpose == "learn":
        OptunaWork(task, 200).optuna_study()

    if task.purpose == "use":
        a = Predict(task)
        b = a.predict()
        print(b)


if __name__ == "__main__":
    run_test()



