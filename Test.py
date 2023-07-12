import pandas as pd
import os


class T:
    def __init__(self, ar: dict):
        # fill this field
        self.purpose = ar["purpose"]  # or use
        self.task_type = ar["task_type"]  # or classification
        self.target_variable = ar["target_variable"]  # input by your self
        self.file_name = ar["file_name"]  # input by your self

        # don't touch
        self.df = pd.read_csv(f"{self.file_name}.csv")
        self.task_id = 19
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
            "file_name": "tmp/titanic"
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
    scenario = T(ar)
    return scenario
