import numpy as np
import pandas as pd
import sklearn.datasets
import sklearn.ensemble
import sklearn.model_selection
import optuna
import pickle
from sklearn.metrics import mean_squared_error
from optuna.samplers import TPESampler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingRegressor
from WorkWithTask import Task
from xgboost import XGBRegressor


class Model:
    def fit(self, x, y):
        pass

    def predict(self, x):
        pass

    def accuracy(self, x, y):
        pass

    def save(self, trial_number: int, task: Task):
        with open("task_{}/model_{}.pickle".format(task.task_id, trial_number),
                  "wb") as fout:
            pickle.dump(self, fout)
        return 0


class LinearRegressionModel(Model):
    def __init__(self):
        self.lrg = LinearRegression()

    def fit(self, x, y):
        return self.lrg.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.lrg, x, y, scoring='r2',
                                                        n_jobs=-1,
                                                        cv=5)
        return score.mean()

    def predict(self, x):
        return self.lrg.predict(x)


class PolynomialRegressionModel(Model):
    def __init__(self, degree):
        self.polynomial_features = PolynomialFeatures(degree=degree)
        self.linear_regression = LinearRegression()
        self.pipeline = Pipeline([("polynomial_features", self.polynomial_features),
                                  ("linear_regression", self.linear_regression)])

    def fit(self, x, y):
        return self.pipeline.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.pipeline, x, y, scoring='r2',
                                                        n_jobs=-1, cv=5)
        return score.mean()

    def predict(self, x):
        return self.pipeline.predict(x)


class GradientBoostingRegression(Model):
    def __init__(self, param):
        self.gbr = XGBRegressor(**param)

    def fit(self, x, y):
        return self.gbr.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.gbr, x, y, scoring="r2", n_jobs=-1,
                                                        cv=5)
        return score.mean()

    def predict(self, x):
        return self.gbr.predict(x)


class LogisticRegressionModel(Model):
    def __init__(self, penalty, solver, c):
        self.lr = LogisticRegression(max_iter=1000, penalty=penalty, solver=solver, C=c)

    def fit(self, x, y):
        return self.lr.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.lr, x, y, n_jobs=-1, cv=5)
        return score.mean()

    def predict(self, x):
        return self.lr.predict(x)


class KNeighborsClassifierModel(Model):
    def __init__(self, n_neighbors, weights, metric):
        self.knn = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, metric=metric)

    def fit(self, x, y):
        return self.knn.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.knn, x, y, n_jobs=-1, cv=5)
        return score.mean()

    def predict(self, x):
        return self.knn.predict(x)


class SVMModel(Model):
    def __init__(self, kernel, degree, c):
        self.svm = SVC(kernel=kernel, degree=degree, C=c)

    def fit(self, x, y):
        return self.svm.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.svm, x, y, n_jobs=-1, cv=5)
        return score.mean()

    def predict(self, x):
        return self.svm.predict(x)


class DecisionTree(Model):
    def __init__(self, criterion, splitter):
        self.tree = DecisionTreeClassifier(criterion=criterion, splitter=splitter)

    def fit(self, x, y):
        return self.tree.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.tree, x, y, n_jobs=-1, cv=5)
        return score.mean()

    def predict(self, x):
        return self.tree.predict(x)


class RandomForest(Model):
    def __init__(self, criterion):
        self.forest = RandomForestClassifier(criterion=criterion)

    def fit(self, x, y):
        return self.forest.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.forest, x, y, n_jobs=-1, cv=5)
        return score.mean()

    def predict(self, x):
        return self.forest.predict(x)
