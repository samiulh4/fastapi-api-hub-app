from pydantic import BaseModel
from typing import Literal

class FileResponse(BaseModel):
    file_id: str
    file_name: str
    file_url: str
    file_status: Literal["active", "inactive"]