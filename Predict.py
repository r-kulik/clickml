import numpy as np
import pandas as pd

from WorkWithTask import Task
import pickle
import json
from Imputers import Imputer

CONST_FREQ = 0.01


class Predict:
    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        self.df = pd.read_csv(f"task_{task_id}/df.csv")
        self.col_name = self.df.columns

    def predict(self) -> None:

        # import all files (pickle and json) to program from user_name/project_name
        with open("task_{}/encoder_best.pickle".format(self.task_id),
                  "rb") as enc:
            encoder = pickle.load(enc)

        with open("task_{}/scaler_best.pickle".format(self.task_id),
                  "rb") as scal:
            scaler = pickle.load(scal)

        with open("task_{}/model_best.pickle".format(self.task_id),
                  "rb") as mod:
            model = pickle.load(mod)

        with open("task_{}/config_best.json".format(self.task_id)) as file:
            config = json.load(file)

        # get values from config_best.json
        deleted_columns = config["deletedColumns"]
        imputer_strategy = config["imputer_strategy"]
        target = config["target_variable"]

        self.df = self.df.drop(target, axis=1)

        # delete columns
        for i in self.df:
            if i in deleted_columns:
                self.df = self.df.drop(i, axis=1)

        # preprocessing
        imputer_strategy = Imputer(imputer_strategy)
        self.df = imputer_strategy.fit(self.df)

        self.df = encoder.transform(self.df)

        self.df = scaler.transform(self.df)

        # predict using best model
        out = model.predict(self.df)
        out = pd.DataFrame(out)
        print(out)
        # save to file best.csv
        result = pd.read_csv(f"task_{self.task_id}/df.csv")
        result[target] = out

        result.to_csv(f"task_{self.task_id}/best.csv")
