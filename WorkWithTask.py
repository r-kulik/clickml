import pandas as pd


class Task:
    def __init__(self):
        self.description = self.get_description_from_sever()
        self.user_name = self.description["user_name"]
        self.project_name = self.description["project_name"]
        self.purpose = self.description["purpose"]
        self.task_type = self.description["task_type"]
        self.target_variable = self.description["target_variable"]
        self.df = self.get_data_frame()

    def get_data_frame(self) -> pd.DataFrame:
        file = self.__get_file_from_server()
        file_extension = file.split(".")[-1]

        if file_extension == "csv":
            df = pd.read_csv(file)

        # todo add processing of another file extension
        return df

    def __get_file_from_server(self) -> str:
        return "1.csv"
        # todo add getting file through web

    def get_description_from_sever(self) -> dict:
        # todo add receiving json file with descriptions
        return {}
    """
    dict:
    "user_name" : str
    "project_name" : str
    "purpose" : str("learning / using")
    "task_type" : str
    "target_variable" : str
    """