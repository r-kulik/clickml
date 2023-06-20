from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
import pandas as pd
import numpy as np


def imputer_mean(x_column):
    imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
    return imputer.fit_transform(x_column)


def imputer_most_frequent(x_column):
    imputer = SimpleImputer(missing_values=np.nan, strategy='most_frequent')
    return imputer.fit_transform(x_column)


def standard_scaler(x):
    scaler = StandardScaler()
    return pd.DataFrame(scaler.fit_transform(x), columns=x.columns)


def robust_scaler(x):
    scaler = RobustScaler()
    return pd.DataFrame(scaler.fit_transform(x), columns=x.columns)


def minmax_scaler(x):
    scaler = MinMaxScaler()
    return pd.DataFrame(scaler.fit_transform(x), columns=x.columns)
