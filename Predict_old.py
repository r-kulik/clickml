import numpy as np
from WorkWithTask import Task
import pickle
import json
from Imputers import Imputer

CONST_FREQ = 0.01


class PredictOld:
    def __init__(self, task: Task) -> None:
        self.task = task

    def predict(self) -> np.ndarray:
        # import all files (pickle and json) to program from user_name/project_name
        with open("task_{}/encoder_best.pickle".format(self.task.task_id),
                  "rb") as enc:
            encoder = pickle.load(enc)

        with open("task_{}/scaler_best.pickle".format(self.task.task_id),
                  "rb") as scal:
            scaler = pickle.load(scal)

        with open("task_{}/model_best.pickle".format(self.task.task_id),
                  "rb") as mod:
            model = pickle.load(mod)

        with open("task_{}/config_best.json".format(self.task.task_id)) as file:
            config = json.load(file)

        # get values from config_best.json
        deleted_columns = config["deletedColumns"]
        imputer_strategy = config["imputer_strategy"]

        # delete columns
        for i in self.task.df:
            if i in deleted_columns:
                self.task.df = self.task.df.drop(i, axis=1)

        # preprocessing
        imputer_strategy = Imputer(imputer_strategy)
        self.task.df = imputer_strategy.fit(self.task.df)

        self.task.df = encoder.transform(self.task.df)
        self.task.df = scaler.transform(self.task.df)

        # predict using best model
        result = model.predict(self.task.df)

        return result
