import numpy as np
import pandas as pd
import sklearn.datasets
import sklearn.ensemble
import sklearn.model_selection
import sklearn.svm
import optuna
import pickle
from optuna.samplers import TPESampler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


class Model:
    def fit(self, x, y):
        pass

    def predict(self, x):
        pass

    def accuracy(self, x, y):
        pass

    def save(self, trial_number: int):
        with open("{}.pickle".format(trial_number), "wb") as fout:
            pickle.dump(self, fout)
        return 0


class LinearRegressionModel(Model):
    def __init__(self):
        self.lrg = LinearRegression()

    def fit(self, x, y):
        return self.lrg.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.lrg, x, y, n_jobs=-1, cv=5)
        return score.mean()

    def predict(self, x):
        return self.lrg.predict(x)


class PolynomialRegressionModel(Model):
    def __init__(self, degree, x, y):
        self.polynomial_features = PolynomialFeatures(degree=degree)
        self.linear_regression = LinearRegression()
        self.pipeline = Pipeline([("polynomial_features", self.polynomial_features),
                                  ("linear_regression", self.linear_regression)])

    def fit(self, x, y):
        return self.pipeline.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.pipeline, x, y, n_jobs=-1, cv=5)
        return score.mean()

    def predict(self, x):
        return self.pipeline.predict(x)


class LogisticRegressionModel(Model):
    def __init__(self, penalty, solver, c, x, y):
        self.lr = LogisticRegression(max_iter=1000, penalty=penalty, solver=solver, C=c)

    def fit(self, x, y):
        return self.lr.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.lr, x, y, n_jobs=-1, cv=5)
        return score.mean()

    def predict(self, x):
        return self.lr.predict(x)


class KNeighborsClassifierModel(Model):
    def __init__(self, n_neighbors, weights, metric, x, y):
        self.knn = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, metric=metric)

    def fit(self, x, y):
        return self.knn.fit(x, y)

    def accuracy(self, x, y):
        score = sklearn.model_selection.cross_val_score(self.knn, x, y, n_jobs=-1, cv=5)
        return score.mean()

    def predict(self, x):
        return self.knn.predict(x)
