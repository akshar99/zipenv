![image](https://github.com/user-attachments/assets/cbc5d48e-7585-43a0-8d43-52e4b0460153)

# FastAPI Backend for Zipping Files

## Overview
This FastAPI backend compresses multiple uploaded files into a ZIP archive and returns it for download. It avoids writing files to disk by using in-memory operations, making it efficient and secure.

---

## Key Components

### 1. Imports
- `FastAPI`: The core framework for building the API.
- `CORSMiddleware`: Enables cross-origin requests (critical for frontend-backend communication).
- `StreamingResponse`: Streams binary data (like ZIP files) directly to the client.
- `zipfile` and `io`: Handle ZIP creation and in-memory byte streams.
- `List[UploadFile]`: Type hint for accepting multiple uploaded files.

### 2. CORS Configuration
- Allows requests from **any domain** (`allow_origins=["*"]`) for development simplicity.
- In production, replace `"*"` with specific frontend domains (e.g., `["https://your-frontend.com"]`).

### 3. API Endpoint (`/zip-file/`)
- **Input**: A list of files sent via a POST request.
- **Process**:
  - Creates an in-memory buffer (`io.BytesIO`) to store the ZIP file.
  - Uses `zipfile.ZipFile` to write files directly to the buffer.
  - `writestr` adds files to the ZIP without needing physical files on disk.
- **Output**: A ZIP file streamed back to the client with headers forcing a download.

---

## Why This Design?

### In-Memory Processing
- No temporary files are saved to disk, reducing I/O overhead and improving security.
- Uses Python’s `io.BytesIO` for efficient memory usage.

### StreamingResponse
- Sends the ZIP file in chunks, minimizing memory usage for large files.

### CORS
- Required for frontend-backend communication when they’re hosted on different domains/ports.

---

## Security Notes

### File Size Limits
FastAPI defaults to 1 MB file upload limits. For larger files, add:
```python
from fastapi import File
@app.post("/zip-file/")
async def zip_files(files: List[UploadFile] = File(..., description="Files", max_size=100_000_000)):  # 100 MB
