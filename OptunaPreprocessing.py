import numpy as np
import pandas as pd
import optuna
import os
import pickle
import json
import os
import optuna
import ModelsFunctions
from DataSending import send_percent
from Encoder import Encoding
from Imputers import Imputer
from Scalers import Scaler
from WorkWithTask import Task
import cpuinfo

# todo add COMMENTS. Not forget. Not only in this file
CONST_FREQ = 0.01


class OptunaWork:
    def __init__(self, task: Task, n_trials: int):
        self.n_trials = n_trials
        self.counter = 0
        self.task = task
        self.current_trial = 0

    def objective(self, trial):
        x = self.task.df.drop(self.task.target_variable, axis=1)
        y = self.task.df[self.task.target_variable]
        self.deletedColumns = []
        for i in x:  # только для строк или объектов
            if x[i].dtype == "object":
                counts = x[i].value_counts()
                if counts[counts.idxmax()] / len(x[i]) < CONST_FREQ and x[i].dtype == object:
                    x = x.drop(i, axis=1)
                    self.deletedColumns.append(i)

        imputer_strategy = trial.suggest_categorical("imputer", ["mean", "most_frequent"])
        imputer = Imputer(imputer_strategy)
        x = imputer.fit(x).copy()

        encoder = Encoding()
        x = encoder.fit(x).copy()
        encoder.save(trial.number, self.task)

        scaler_type = trial.suggest_categorical("scaler", ["standard", "robust", "minmax"])
        scaler = Scaler(scaler_type)
        x = scaler.fit_transform(x).copy()
        scaler.save(trial.number, self.task)

        model = ModelsFunctions.Model()

        # todo add SVM
        if self.task.task_type == "classification":
            classifier_name = trial.suggest_categorical("classifier",
                                                        ["DecisionTree", "LogisticRegression", "RandomForest"])

            if classifier_name == "LogisticRegression":
                solver = trial.suggest_categorical("solver", ['newton-cg', 'lbfgs', 'liblinear'])
                penalty = trial.suggest_categorical("penalty", ["l1", "l2"])
                c = trial.suggest_float("C", 1e-3, 1e3, log=True)
                model = ModelsFunctions.LogisticRegressionModel(penalty, solver, c)

            elif classifier_name == "DecisionTree":
                criterion = trial.suggest_categorical("criterion", ["gini", "entropy"])
                splitter = trial.suggest_categorical("splitter", ["best", "random"])
                model = ModelsFunctions.DecisionTree(criterion, splitter)

            elif classifier_name == "RandomForest":
                criterion = trial.suggest_categorical("criterion", ["gini", "entropy"])
                model = ModelsFunctions.RandomForest(criterion)

            elif classifier_name == "SVM":
                # todo fit parameters

                # "linear", "poly", "rbf", "sigmoid", "precomputed"
                kernel = trial.suggest_categorical("kernel", ["linear"])
                degree = trial.suggest_int("degree", 1, 5, log=True)
                c = trial.suggest_float("C", 0.001, 1, log=True)
                model = ModelsFunctions.SVMModel(kernel, degree, c)

        elif self.task.task_type == "regression":
            regressor_name = trial.suggest_categorical("regressor_name",
                                                       ["GradientBoosting"])
            if regressor_name == "LinearRegression":
                model = ModelsFunctions.LinearRegressionModel()
            elif regressor_name == "PolynomialRegression":
                degree = trial.suggest_int("degree", 2, 8)
                model = ModelsFunctions.PolynomialRegressionModel(degree)
            elif regressor_name == "GradientBoosting":
                param = {
                    'objective': 'reg:squarederror',
                    'sampling_method': 'uniform',
                    'lambda': trial.suggest_float('lambda', 7.0, 17.0, log=True),
                    'alpha': trial.suggest_float('alpha', 7.0, 17.0, log=True),
                    'eta': trial.suggest_categorical('eta', [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
                    'gamma': trial.suggest_categorical('gamma', [18, 19, 20, 21, 22, 23, 24, 25]),
                    'learning_rate': trial.suggest_categorical('learning_rate',
                                                               [0.008, 0.01, 0.012, 0.014, 0.016, 0.018, 0.02]),
                    'colsample_bytree': trial.suggest_categorical('colsample_bytree',
                                                                  [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
                    'colsample_bynode': trial.suggest_categorical('colsample_bynode',
                                                                  [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]),
                    'n_estimators': trial.suggest_int('n_estimators', 400, 1000),
                    'min_child_weight': trial.suggest_int('min_child_weight', 8, 600),
                    'max_depth': trial.suggest_categorical('max_depth', [3, 4, 5, 6, 7]),
                    'subsample': trial.suggest_categorical('subsample', [0.5, 0.6, 0.7, 0.8, 1.0]),
                    'random_state': 42
                }
                model = ModelsFunctions.GradientBoostingRegression(param)
        accuracy = 0
        try:
            accuracy = model.accuracy(x, y)
            model.fit(x, y)
            model.save(trial.number, self.task)
        except Exception as e:
            print(e)
            return 0

        config = {"deletedColumns": self.deletedColumns, "imputer_strategy": imputer_strategy}

        with open("task_{}/config_{}.json".format(self.task.task_id, trial.number),
                  "w") as fout:
            json.dump(config, fout)

        self.counter += 1

        if self.counter % 5 == 0:
            send_percent(self.counter, self.n_trials)

        return accuracy

    def optuna_study(self):
        study = optuna.create_study(direction="maximize")
        study.optimize(self.objective, n_trials=self.n_trials, gc_after_trial=True)

        for i in ["config_best.json", "encoder_best.pickle", "scaler_best.pickle", "model_best.pickle"]:
            if "{}".format(i) in os.listdir("task_{}".format(self.task.task_id)):
                os.remove("task_{}/{}".format(self.task.task_id, i))

        os.rename("task_{}/config_{}.json".format(self.task.task_id, study.best_trial.number),
                  "task_{}/config_best.json".format(self.task.task_id))
        os.rename(
            "task_{}/encoder_{}.pickle".format(self.task.task_id, study.best_trial.number),
            "task_{}/encoder_best.pickle".format(self.task.task_id))
        os.rename("task_{}/scaler_{}.pickle".format(self.task.task_id, study.best_trial.number),
                  "task_{}/scaler_best.pickle".format(self.task.task_id))
        os.rename("task_{}/model_{}.pickle".format(self.task.task_id, study.best_trial.number),
                  "task_{}/model_best.pickle".format(self.task.task_id))

        dirs = os.listdir("task_{}".format(self.task.task_id))
        try:
            for i in dirs:
                if "best" not in i:
                    os.remove("task_{}/{}".format(self.task.task_id, i))
        except Exception as e:
            print(e)
