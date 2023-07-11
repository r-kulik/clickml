import numpy as np
from sklearn.impute import SimpleImputer


class Imputer:
    def __init__(self, strategy: str):
        self.strategy = strategy

    @staticmethod
    def imput(x_column, strategy):
        imputer = SimpleImputer(missing_values=np.nan, strategy=strategy)
        return imputer.fit_transform(x_column)

    def fit(self, x):
        if self.strategy == "mean":
            for i in x:
                if x[i].dtype == object:
                    x[i] = self.imput(x[i].values.reshape(-1, 1), "most_frequent")
                else:
                    x[i] = self.imput(x[i].values.reshape(-1, 1), "mean")
        elif self.strategy == "most_frequent":
            for i in x:
                x[i] = self.imput(x[i].values.reshape(-1, 1), "most_frequent")
        return x.copy()