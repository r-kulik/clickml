import pandas as pd
import logging
from JsTask import APILearnTask
import os


class Task:
    def __init__(self, js_task: APILearnTask):
        # configuration logging in file
        logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")

        # var for correctness all elements, can be changed only on False (for cases with exception)
        self.is_correct = True

        # variables for work with task in all program
        self.task_id = js_task.task_id
        self.task_type = js_task.task_type
        self.target_variable = js_task.target_variable
        self.source_file_upload_token = js_task.source_file_upload_token
        self.df = self.__get_data_frame()
        self.__create_dir()

    def __get_data_frame(self) -> pd.DataFrame:
        df = None

        try:
            df = pd.read_csv(f"tmp/{self.source_file_upload_token}.csv")
        except:
            self.is_correct = False
            logging.warning("Problems with wile getting")
        return df

    def __create_dir(self) -> None:
        if self.task_id not in os.listdir(path='.'):
            os.mkdir(f"task_{self.task_id}")
