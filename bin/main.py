from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import zipfile
import io
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.post("/zip-file/")
async def zip_files(files: List[UploadFile]):
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            file_content = await file.read()
            zipf.writestr(file.filename, file_content)
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="application/zip",
                                 headers={"Content-Disposition": "attachment; filename=compressed.zip"})
    

    