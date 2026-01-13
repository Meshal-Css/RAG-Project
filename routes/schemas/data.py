from pydantic import BaseModel # the general structure of any schemes
from typing import Optional

class ProcessRequest(BaseModel):
    file_id : str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset : Optional[int] = 0