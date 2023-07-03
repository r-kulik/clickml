import pandas as pd


class Task:
    def __init__(self):
        self.__description = self.get_description_from_sever()
        self.user_name = self.__description["user_name"]
        self.project_name = self.__description["project_name"]
        self.purpose = self.__description["purpose"]
        self.task_type = self.__description["task_type"]
        self.target_variable = self.__description["target_variable"]
        self.df = self.get_data_frame()

    def get_data_frame(self) -> pd.DataFrame:
        file = self.__get_file_from_server()
        file_extension = file.split(".")[-1]

        if file_extension == "csv":
            df = pd.read_csv(file)

        # todo add processing of another file extension
        return df

    def __get_file_from_server(self) -> str:
        return "{}/{}/tmp/titanic.csv".format(self.user_name, self.project_name)
        # todo add getting file through web

    def get_description_from_sever(self) -> dict:
        # todo add receiving json file with descriptions
        return {"user_name": "bulkin", "project_name": "rep", "purpose" : "learning",
                "task_type": "class", "target_variable": "survived"}
    """
    dict:
    "user_name" : str
    "project_name" : str
    "task_type" : str
    "target_variable" : str
    """