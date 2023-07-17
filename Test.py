import pandas as pd
import threading
from Predict_old import PredictOld
from WorkWithTask import Task
from OptunaPreprocessing import OptunaWork
from Predict_old import PredictOld
from sklearn import metrics
from Clear import *
import ChooseBest
import cpuinfo
from sklearnex import patch_sklearn


class T:
    def __init__(self, ar: dict):
        # fill this field
        self.purpose = ar["purpose"]  # or use
        self.task_type = ar["task_type"]  # or classification
        self.target_variable = ar["target_variable"]  # input by your self
        self.file_name = ar["file_name"]  # input by your self

        # don't touch
        self.df = pd.read_csv(f"{self.file_name}.csv")
        self.task_id = 21
        if self.purpose == "learn":
            self.__create_dir()

    def __create_dir(self) -> None:
        if self.task_id not in os.listdir(path='.'):
            os.mkdir(f"task_{self.task_id}")


def choose_scenario(num: int) -> T:
    ar = {}
    if num == 0:
        ar = {
            "purpose": "learn",
            "task_type": "classification",
            "target_variable": "Machine failure",
            "file_name": "tmp/cars_train"
        }

    if num == 1:
        ar = {
            "purpose": "learn",
            "task_type": "classification",
            "target_variable": "survived",
            "file_name": "tmp/titanic_train"
        }

    if num == 2:
        ar = {
            # Multiclass
            "purpose": "learn",
            "task_type": "classification",
            "target_variable": "cut",
            "file_name": "tmp/diamonds"
        }
    if num == 3:
        ar = {
            "purpose": "learn",
            "task_type": "regression",
            "target_variable": "price",
            "file_name": "tmp/california_train"
        }

    if num == 4:
        ar = {
            "purpose": "use",
            "task_type": "classification",
            "target_variable": "Machine failure",
            "file_name": "tmp/cars_test"
        }

    if num == 5:
        ar = {
            "purpose": "use",
            "task_type": "regression",
            "target_variable": "price",
            "file_name": "tmp/california_test"
        }

    if num == 6:
        ar = {
            "purpose": "use",
            "task_type": "classification",
            "target_variable": "is_legendary",
            "file_name": "tmp/pokemon_test"
        }

    if num == 7:
        ar = {
            "purpose": "learn",
            "task_type": "classification",
            "target_variable": "is_legendary",
            "file_name": "tmp/pokemon_train"
        }

    if num == 8:
        ar = {
            "purpose": "use",
            "task_type": "classification",
            "target_variable": "survived",
            "file_name": "tmp/titanic_test"
        }
    scenario = T(ar)
    return scenario


def print_clf_metrics(y_actual, y_pred):
    print(f'Testing accuracy = {metrics.accuracy_score(y_actual, y_pred)}')
    print(f'Testing precision = {metrics.precision_score(y_actual, y_pred)}')
    print(f'Testing recall = {metrics.recall_score(y_actual, y_pred)}')
    print(f'Testing F1-score = {metrics.f1_score(y_actual, y_pred)}')


def print_reg_metrics(y_actual, y_pred):
    print(f'Testing MSE = {metrics.mean_squared_error(y_actual, y_pred)}')
    print(f'Testing R2 = {metrics.r2_score(y_actual, y_pred)}')


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
