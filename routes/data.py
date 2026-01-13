from fastapi import APIRouter, Depends, UploadFile, File, status
from fastapi.responses import JSONResponse
from helper.config import get_settings, Settings
from controllers import DataController, ProjectController, processController
from models import ResponseSignal
from .schemas.data import ProcessRequest
import aiofiles
import logging

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

# =========================
# Upload Endpoint
# =========================
@data_router.post("/upload/{project_id}", status_code=status.HTTP_201_CREATED)
async def upload_data(
    project_id: str,
    file: UploadFile = File(...),
    app_settings: Settings = Depends(get_settings)
):
    data_controller = DataController()

    is_valid, result_signal = data_controller.validate_upload_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal.value}
        )

    # Generate file path
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value}
        )

    return {
        "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
        "file_id": file_id
    }


# =========================
# Process Endpoint
# =========================
@data_router.post("/process/{project_id}")
async def process_endpoint(
    project_id: str,
    request: ProcessRequest
):
    file_id = request.file_id
    chunk_size = request.chunk_size
    overlap_size = request.overlap_size

    process_controller = processController(project_id=project_id)

    file_content = process_controller.get_file_content(file_id=file_id)
    if not file_content:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_NOT_FOUND.value}
        )

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    if not file_chunks:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILED.value}
        )

        

    return {
        "signal": ResponseSignal.PROCESSING_SUCCESS.value,
        "file_id": file_id,
        "chunks_count": len(file_chunks),
        "chunks": file_chunks
    }
