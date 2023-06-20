import sklearn.datasets
import sklearn.ensemble
import sklearn.model_selection
import sklearn.svm
import pickle
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier


def linear_regression(x, y):
    lrg = LinearRegression()
    score = sklearn.model_selection.cross_val_score(lrg, x, y, n_jobs=-1, cv=5)
    accuracy = score.mean()
    return accuracy


def polynomial_regression(degree, x, y):
    polynomial_features = PolynomialFeatures(degree=degree)
    linear_regression = LinearRegression()
    pipeline = Pipeline([("polynomial_features", polynomial_features), ("linear_regression", linear_regression)])
    score = sklearn.model_selection.cross_val_score(pipeline, x, y, n_jobs=-1, cv=5)
    accuracy = score.mean()
    return accuracy


def logistic_regression(penalty, solver, C, x, y):
    lr = LogisticRegression(max_iter=1000, penalty=penalty, solver=solver, C=C)
    score = sklearn.model_selection.cross_val_score(lr, x, y, n_jobs=-1, cv=5)
    accuracy = score.mean()
    return accuracy

def KNeighbors(n_neighbors, weights, metric, x, y, trial):
    knn = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights, metric=metric)
    score = sklearn.model_selection.cross_val_score(knn, x, y, scoring="balanced_accuracy", n_jobs=-1, cv=5)
    knn = knn.fit(x, y)
    with open("trial_{}.pickle".format(trial.number), "wb") as fout:
            pickle.dump(knn, fout)
    '''n_neighbors':list(range(1, 15)),
              'weights':['uniform', 'distance'],
              'metric':['euclidean', 'manhattan', 'chebyshev', 'cosine']'''
    accuracy = score.mean()
    return accuracy
