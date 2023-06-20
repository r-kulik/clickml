import pandas as pd


def get_data_frame() -> pd.DataFrame:
    file = get_file_from_server()
    file_extension = file.split(".")[-1]
    if file_extension == "csv":
        df = pd.read_csv(file)
    # todo add processing of another file extension
    return df


def get_file_from_server() -> str:
    return "1.csv"
    # todo add getting file through web
