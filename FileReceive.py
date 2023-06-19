from pandas import read_csv

def file_upload():
    df  = read_csv("1.csv")
    return df