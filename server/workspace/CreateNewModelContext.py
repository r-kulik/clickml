from .BasePageContext import BasePageContext

class CreateNewModelContext(BasePageContext):

    def __init__(self, request, **kwargs) -> None:
        super().__init__(request, **kwargs)