from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
from helper.config import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseSignal
import aiofiles
from pathlib import Path
import os
import logging

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),
    app_settings: Settings = Depends(get_settings)
):
   # validate the file propreties
    Data_Controller = DataController()
    is_valid, result_signal =Data_Controller.validate_upload_file(file=file)

    if not is_valid:
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal.value}
        )

    
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = Data_Controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    
    #safe_file_name = Path(file.filename).name
    #file_path = os.path.join(project_dir_path, safe_file_name)

    try:

     async with aiofiles.open(file_path, "wb") as f:
         while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
    except Exception as e:

        logger.error(f"Error while uploading file : {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value}
        )  

    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
        "file_id": file_id}
    )
