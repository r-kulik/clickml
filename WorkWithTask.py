import pandas as pd


class Task:
    def __init__(self, task_id, purpose, task_type, target_variable, file_path):
        # variables for work with task in all program
        self.task_id = task_id
        self.purpose = purpose
        self.task_type = task_type
        self.target_variable = target_variable
        self.df = pd.read_csv(file_path)
