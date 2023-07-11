from pydantic import BaseModel


class APILearnTask(BaseModel):
    task_id: int
    task_type: str
    target_variable: str
    source_file_upload_token: str
