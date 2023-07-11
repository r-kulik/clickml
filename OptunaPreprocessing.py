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
        if self.task.task_type == "classification":
            classifier_name = trial.suggest_categorical("classifier",
                                                        ["LogisticRegression", "DecisionTree"])
            if classifier_name == "LogisticRegression":
                solver = trial.suggest_categorical("solver", ['newton-cg', 'lbfgs', 'liblinear'])
                penalty = trial.suggest_categorical("penalty", ["l1", "l2", "none"])
                c = trial.suggest_float("C", 1e-3, 1e3, log=True)
                model = ModelsFunctions.LogisticRegressionModel(penalty, solver, c)
            elif classifier_name == "DecisionTree":
                criterion = trial.suggest_categorical("criterion", ["gini", "entropy"])
                splitter = trial.suggest_categorical("splitter", ["best", "random"])
                model = ModelsFunctions.DecisionTree(criterion, splitter)
            elif classifier_name == "randomForest":
                criterion = trial.suggest_categorical("criterion", ["gini", "entropy"])
                model = ModelsFunctions.RandomForest(criterion)

        elif self.task.task_type == "regression":
            regressor_name = trial.suggest_categorical("regressor_name",
                                                       ["LinearRegression", "PolynomialRegression", "GradientBoosting"])
            if regressor_name == "LinearRegression":
                model = ModelsFunctions.LinearRegressionModel()
            elif regressor_name == "PolynomialRegression":
                degree = trial.suggest_int("degree", 2, 8)
                model = ModelsFunctions.PolynomialRegressionModel(degree)
            elif regressor_name == "GradientBoosting":
                degree = trial.suggest_int("degree", 2, 4)
                loss = 0
                learning_rate = 0
                n_estimators = 0
                criterion = 0
                max_depth = 0
                min_samples_leaf = 0
                model = ModelsFunctions.PolynomialRegressionModel(loss, learning_rate, n_estimators, criterion,
                                                                  max_depth, min_samples_leaf)
        accuracy = 0
        try:
            accuracy = model.accuracy(x, y)
            model.fit(x, y)
            model.save(trial.number, self.task)
        except Exception as e:
            print(e)

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
        study.optimize(self.objective, n_trials=self.n_trials)

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
