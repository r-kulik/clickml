from django.http import HttpRequest
import pandas as pd


class ModelCreationSettingsContext:
    dataset_column_names: list[str] = []

    def __init__(self, request: HttpRequest) -> None:
        self.request = request
        self.username = self.request.user.get_username()
        self.dataset_file = self.request.FILES['dataset_source_file']
        self.project_name = self.request.POST.get('project_name', 'Unnamed Project')
        self.analyzeDataSetColumnNames()

    def analyzeDataSetColumnNames(self) -> None:
        dataframe: pd.DataFrame = pd.read_csv(self.dataset_file)
        for column in dataframe.columns:
            self.dataset_column_names.append(column)
