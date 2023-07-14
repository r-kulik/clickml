from .BasePageContext import BasePageContext


class UseModelContext(BasePageContext):
    def __init__(self, request, model_id: int = -1, **kwargs):
        super().__init__(request, **kwargs)
        self.model_id = model_id