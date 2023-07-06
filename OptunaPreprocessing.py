import numpy as np
import pandas as pd
import optuna
import os
import pickle
import json
from Imputers import Imputer
from Encoder import Encoding
from Scalers import Scaler
import ModelsFunctions
from WorkWithTask import Task


# todo add COMMENTS. Not forget. Not only in this file
CONST_FREQ = 0.01


class OptunaWork:
    def __init__(self, task: Task):
        self.task = task

    def objective(self, trial):
        x = self.task.df.drop(self.task.target_variable, axis=1)
        y = self.task.df[self.task.target_variable]
        deletedColumns = []
        for i in x:  # только для строк или объектов
            if type(x[i]) == "object":
                print(x[i])
                counts = x[i].value_counts()
                if counts[counts.idxmax()] / len(x[i]) < CONST_FREQ and x[i].dtype == object:
                    x = x.drop(i, axis=1)
                    self.deletedColumns[trial.number].append(i)

        imputer_strategy = trial.suggest_categorical("imputer", ["mean", "most_frequent"])
        imputer = Imputer(imputer_strategy)
        x = imputer.fit(x)

        encoder = Encoding()
        x = encoder.fit(x)
        encoder.save(trial.number, self.task)

        scaler_type = trial.suggest_categorical("scaler", ["standard", "robust", "minmax"])
        scaler = Scaler(scaler_type)
        x = scaler.fit_transform(x)
        scaler.save(trial.number, self.task)

        model = ModelsFunctions.Model()
        if self.task.task_type == "classification":
            classifier_name = trial.suggest_categorical("classifier",
                                                        ["DecisionTree", "LogisticRegression"])
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
            regressor_name = trial.suggest_categorical("regressor_name", ["LinearRegression", "PolynomialRegression"])
            if regressor_name == "LinearRegression":
                model = ModelsFunctions.LinearRegressionModel()
            elif regressor_name == "PolynomialRegression":
                degree = trial.suggest_int("degree", 2, 8)
                model = ModelsFunctions.PolynomialRegressionModel(degree)
        accuracy = 0
        try:
            accuracy = model.accuracy(x, y)
            model.fit(x, y)
            model.save(trial.number, self.task)
        except Exception as e:
            print(e)

        config = {"deletedColumns": deletedColumns, "imputer_strategy": imputer_strategy}

        with open("{}/{}/config_{}.json".format(self.task.user_name, self.task.project_name, trial.number),
                  "w") as fout:
            json.dump(config, fout)

        return accuracy

    def optuna_study(self):
        study = optuna.create_study(direction="maximize")
        study.optimize(self.objective, n_trials=100)

        os.rename("{}/{}/config_{}.json".format(self.task.user_name, self.task.project_name, study.best_trial.number),
                  "{}/{}/config_best.json".format(self.task.user_name, self.task.project_name))
        os.rename(
            "{}/{}/encoder_{}.pickle".format(self.task.user_name, self.task.project_name, study.best_trial.number),
            "{}/{}/encoder_best.pickle".format(self.task.user_name, self.task.project_name))
        os.rename("{}/{}/scaler_{}.pickle".format(self.task.user_name, self.task.project_name, study.best_trial.number),
                  "{}/{}/scaler_best.pickle".format(self.task.user_name, self.task.project_name))
        os.rename("{}/{}/model_{}.pickle".format(self.task.user_name, self.task.project_name, study.best_trial.number),
                  "{}/{}/model_best.pickle".format(self.task.user_name, self.task.project_name))

        dirs = os.listdir("{}/{}".format(self.task.user_name, self.task.project_name))
        try:
            for i in dirs:
                if "best" not in i:
                    os.remove("{}/{}/{}".format(self.task.user_name, self.task.project_name, i))
        except Exception as e:
            print(e)

        study.best_trial.number
