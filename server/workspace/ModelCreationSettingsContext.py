import secrets

from django.core.files.storage import default_storage
from django.http import HttpRequest
import pandas as pd


from .BasePageContext import BasePageContext
from .errors import WrongFileFormatException


class ModelCreationSettingsContext(BasePageContext):


    def __init__(self, request: HttpRequest, **kwargs) -> None:
        super().__init__(request, **kwargs)
        self.dataset_column_names: list[str] = []
        self.project_name = self.request.POST.get('project_name', 'Unnamed Project')
        self.dataset_file_name = default_storage.save(
            f"source_dataset_files/{secrets.token_urlsafe()}.csv",
            self.request.FILES['dataset_source_file']
        )

        self.analyzeDataSetColumnNames()

    def analyzeDataSetColumnNames(self) -> None:
        dataframe = None
        try:
            dataframe: pd.DataFrame = pd.read_csv(default_storage.open(self.dataset_file_name))
        except UnicodeDecodeError:
            raise WrongFileFormatException()
        for column in dataframe.columns:
            self.dataset_column_names.append(column)