from fastapi import FastAPI
from starlette.responses import FileResponse
import uuid

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


@app.post("/start-upload")
async def start_upload(payload: StartUploadPayload) -> StartUploadResponse:
    return client.get_presigned_multipart(
        f"{uuid.uuid4()}/{payload.file_name}",
        payload.content_type,
        payload.file_size,
        # chunk_size=500 * 1024,
    )


@app.post("/complete-upload")
async def complete_upload(payload: CompleteUploadPayload) -> CompleteUploadResponse:
    result = client.complete_multipart_upload(
        payload.key, payload.upload_id, payload.etags
    )
    print(result)
    return CompleteUploadResponse(url="https://test.com")
