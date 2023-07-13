import secrets

from django.core.files.storage import default_storage

from .BasePageContext import BasePageContext


class ViewResultsContext(BasePageContext):

    def __init__(self, request, **kwargs):
        super().__init__(request, **kwargs)
        self.exploit_file_name = default_storage.save(
            f"exploit_dataset_files/{secrets.token_urlsafe()}.csv",
            request.FILES['exploit_file']
        )
        self.model_id = request.POST.get('model_id')
        self.exploit_task_id = 0



