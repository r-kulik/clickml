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
            scoring = "roc_auc_ovr"
            classifier_name = trial.suggest_categorical("classifier",
                                                        ["DecisionTree", "LogisticRegression", "GradientBoostingClassifier"])

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

            elif classifier_name == "GradientBoostingClassifier":
                param = {
                    "verbosity": 0,
                    "objective": trial.suggest_categorical('objective', ['reg:linear', 'reg:logistic', 'binary:logistic']),
                    "eval_metric": trial.suggest_categorical("eval_metric", ["rmse", "logloss", "error"]),
                    "booster": trial.suggest_categorical("booster", ['gbtree', 'gblinear', 'dart']),
                    "lambda": trial.suggest_float("lambda", 1e-8, 1.0, log=True),
                    "alpha": trial.suggest_float("alpha", 1e-8, 1.0, log=True),
                    "n_estimators": trial.suggest_int("n_estimators", 10, 600),
                    'random_state': 42
                }
                if param["booster"] == "gbtree" or param["booster"] == "dart":
                    param["max_depth"] = trial.suggest_int("max_depth", 1, 4)
                    param["eta"] = trial.suggest_float("eta", 1e-8, 1.0, log=True)
                    param["gamma"] = trial.suggest_float("gamma", 1e-8, 1.0, log=True)
                    param["grow_policy"] = trial.suggest_categorical("grow_policy", ["depthwise", "lossguide"])
                if param["booster"] == "gblinear":
                    param["sample_type"] = trial.suggest_categorical("sample_type", ["uniform", "weighted"])
                    param["normalize_type"] = trial.suggest_categorical("normalize_type", ["tree", "forest"])
                    param["rate_drop"] = trial.suggest_float("rate_drop", 1e-8, 1.0, log=True)
                    param["skip_drop"] = trial.suggest_float("skip_drop", 1e-8, 1.0, log=True)
                model = ModelsFunctions.GradientBoostingClassifier(param)

        elif self.task.task_type == "regression":
            scoring = "r2"
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
                    'eta': trial.suggest_float('eta', 0.2, 1.0),
                    'gamma': trial.suggest_float('gamma', 0, 25),
                    'learning_rate': trial.suggest_float('learning_rate', 0, 0.05),
                    'colsample_bytree': trial.suggest_float('colsample_bytree', 0.1, 1),
                    'colsample_bynode': trial.suggest_float('colsample_bynode', 0.1, 1),
                    'n_estimators': trial.suggest_int('n_estimators', 400, 1000),
                    'min_child_weight': trial.suggest_int('min_child_weight', 8, 600),
                    'max_depth': trial.suggest_int('max_depth', 2, 10),
                    'subsample': trial.suggest_float('subsample', 0.3, 1.0),
                    'random_state': 42
                }
        try:
            if y.nunique() == 2:
                scoring = "f1"
            accuracy = model.accuracy(x, y, scoring=scoring)
            model.fit(x, y)
            model.save(trial.number, self.task)
        except Exception as e:
            print(e)
            return 0

        config = {"deletedColumns": self.deletedColumns, "imputer_strategy": imputer_strategy,
                  "target_variable": self.task.target_variable}

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
