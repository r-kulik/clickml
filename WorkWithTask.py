import pandas as pd
import logging
import os


class Task:
    def __init__(self):
        # configuration logging in file
        logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

        # var for correctness all elements, can be changed only on False (for cases with exception)
        self.is_correct = True

        # variables for work with task in all program
        self.__description = self.__get_description_from_sever()
        self.user_name = self.__description["user_name"]
        self.project_name = self.__description["project_name"]
        self.file_name = self.__description["file_name"]
        self.purpose = self.__description["purpose"]
        self.task_type = self.__description["task_type"]
        self.target_variable = self.__description["target_variable"]
        self.df = self.__get_data_frame()

    def __get_data_frame(self) -> pd.DataFrame:

        file = self.__get_file_from_server()
        df = None

        # check file extension
        file_extension = file.split(".")[-1]

        if file_extension == "csv":
            df = pd.read_csv(file)

        elif file_extension == "xlsx":
            df = pd.read_excel

        else:
            # exception: logging and changing is_correct
            logging.debug("Wrong file format")
            self.is_correct = False

        return df

    def __get_file_from_server(self) -> str:

        # if there is no folder of user create it
        if self.user_name not in os.listdir(path='.'):
            os.mkdir(self.user_name)

        # if there is no folder of project create it
        if self.project_name not in os.listdir(path=self.user_name):
            os.mkdir("{}/{}".format(self.user_name, self.project_name))

        # if there is no tmp in project create it
        if "tmp" not in os.listdir(path=self.user_name + "/" + self.project_name):
            os.mkdir("{}/{}/tpm".format(self.user_name, self.project_name))

        # todo add getting file through web in format user_name/project_name/tmp/example.csv (directory already exist)

        return "{}/{}/tmp/{}".format(self.user_name, self.project_name, self.file_name)

    def __get_description_from_sever(self) -> dict:

        # todo add receiving json file with descriptions

        # just example for testing
        return {"user_name": "bulkina", "project_name": "repkal", "file_name": "titanic.csv", "purpose": "learning",
                "task_type": "class", "target_variable": "survived"}

    # form of json(dict) file
    """
    dict:
    "user_name" : str
    "project_name" : str
    "file name" : str
    "task_type" : str
    "target_variable" : str
    """
