import numpy as np
import pandas as pd
import optuna
import pickle
from Imputers import Imputer
from Encoder import Encoding

CONST_FREQ = 0.01


class OptunaPreprocessing:
    def __init__(self, task_type: str):
        self.task_type = task_type

    def objective(self, trial, x: pd.DataFrame, y):
        deletedColumns = []
        for i in x:  # только для строк или объектов
            if x[i].dtype() == "object":
                counts = x[i].value_counts()
                if counts[counts.idxmax()] / len(x[i]) < CONST_FREQ and x[i].dtype == object:
                    x = x.drop(i, axis=1)
                    self.deletedColumns[trial.number].append(i)

        imputer_type = trial.suggest_categorical("imputer", ["mean", "most_frequent"])
        imputer = Imputer(imputer_type)
        x = imputer.fit(x)

        encoder = Encoding(trial.number)


