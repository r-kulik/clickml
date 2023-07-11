from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
import pandas as pd
import pickle
from WorkWithTask import Task


class Scaler:
    def __init__(self, scaler_type: str):
        if scaler_type == "standard":
            self.__scaler = StandardScaler()
        elif scaler_type == "robust":
            self.__scaler = RobustScaler()
        elif scaler_type == "minmax":
            self.__scaler = MinMaxScaler()

    def fit(self, x):
        return self.__scaler.fit(x)

    def transform(self, x: pd.DataFrame) -> pd.DataFrame:
        return self.__scaler.transform(x)

    def fit_transform(self, x: pd.DataFrame) -> pd.DataFrame:
        return self.__scaler.fit_transform(x)

    def save(self, trial_number: int, task: Task):
        with open("task_{}/scaler_{}.pickle".format(task.task_id, trial_number),
                  "wb") as fout:
            pickle.dump(self, fout)

