import pandas as pd
import logging


class Task:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
        self.is_correct = True
        self.__description = self.get_description_from_sever()
        self.user_name = self.__description["user_name"]
        self.project_name = self.__description["project_name"]
        self.file_name = self.__description["file_name"]
        self.purpose = self.__description["purpose"]
        self.task_type = self.__description["task_type"]
        self.target_variable = self.__description["target_variable"]
        self.df = self.get_data_frame()

    def get_data_frame(self) -> pd.DataFrame:
        file = self.__get_file_from_server()
        file_extension = file.split(".")[-1]
        df = None

        if file_extension == "csv":
            df = pd.read_csv(file)

        elif file_extension == "xlsx":
            df = pd.read_excel

        else:
            logging.debug("Wrong file format")
            self.is_correct = False
        return df

    def __get_file_from_server(self) -> str:
        return "{}/{}/tmp/{}".format(self.user_name, self.project_name, self.file_name)
        # todo add getting file through web

    def get_description_from_sever(self) -> dict:
        # todo add receiving json file with descriptions
        return {"user_name": "bulkin", "project_name": "rep", "file_name" : "titanic.csv", "purpose" : "learning",
                "task_type": "class", "target_variable": "survived"}
    """
    dict:
    "user_name" : str
    "project_name" : str
    "file name" : str
    "task_type" : str
    "target_variable" : str
    """