import uuid

from fastapi import FastAPI
from fastapi.responses import FileResponse
from models import (
    StartUploadPayload,
    StartUploadResponse,
    CompleteUploadPayload,
    CompleteUploadResponse,
)
from upload_client import UploadClient

app = FastAPI()
client = UploadClient()


@app.get("/")
async def index():
    return FileResponse("index.html")


@app.get("/styles.css")
async def styles():
    return FileResponse("styles.css")


@app.post("/start-upload")
async def start_upload(payload: StartUploadPayload) -> StartUploadResponse:
    return client.get_presigned_multipart(
        f"{uuid.uuid4()}/{payload.file_name}",
        payload.content_type,
        payload.file_size,
    )


@app.post("/complete-upload")
async def complete_upload(payload: CompleteUploadPayload) -> CompleteUploadResponse:
    result = client.complete_multipart_upload(
        key=payload.key, upload_id=payload.upload_id, etags_string=payload.etags
    )
    return CompleteUploadResponse(url=result)
