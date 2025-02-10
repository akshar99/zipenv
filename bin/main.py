# Import necessary modules and classes
from fastapi import FastAPI, File, UploadFile  # FastAPI core components
from fastapi.middleware.cors import CORSMiddleware  # CORS middleware for cross-origin requests
from fastapi.responses import StreamingResponse  # For streaming binary responses (e.g., zip files)
import zipfile  # For creating ZIP archives
import io  # For in-memory byte stream handling
from typing import List  # Type hints for Python < 3.9 compatibility

# Initialize the FastAPI application
app = FastAPI()

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the API to accept requests from frontends on different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (simplified for development)
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define the POST endpoint for zipping files
@app.post("/zip-file/")
async def zip_files(files: List[UploadFile]):
    """
    Accepts a list of uploaded files, compresses them into a ZIP archive in memory,
    and returns the ZIP file as a downloadable response.
    """
    
    # Create an in-memory byte stream to hold the ZIP file
    buffer = io.BytesIO()

    # Create a ZIP archive using the buffer (not a physical file)
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Loop through each uploaded file
        for file in files:
            # Read the content of the uploaded file as bytes
            file_content = await file.read()
            
            # Write the file content to the ZIP archive
            # `writestr` writes data directly to the ZIP without needing a physical file
            zipf.writestr(file.filename, file_content)
    
    # Reset the buffer's position to the start so it can be read from the beginning
    buffer.seek(0)

    # Return the ZIP file as a streaming response
    return StreamingResponse(
        buffer,  # The in-memory buffer containing the ZIP data
        media_type="application/zip",  # MIME type for ZIP files
        headers={
            "Content-Disposition": "attachment; filename=compressed.zip"  # Force download
        }
    )