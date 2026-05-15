# Our fast api server
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel #this is data dictionary model that says am accepting data if it contains a string called "text" (the raw notes)
from fastapi.middleware.cors import CORSMiddleware
from processor import generate_ba_docs
import uvicorn

# 1. Initialize the API
app = FastAPI(title="Auto-Scribe Multimodal API")

# 2. Setup CORS (Cross-Origin Resource Sharing)
# This is CRITICAL. It tells the backend: "It's okay to accept requests from my React app."
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, we would limit this to your website URL
    allow_methods=["*"],
    allow_headers=["*"],
)

# NEW: Updated Data Model to handle Files
class NoteRequest(BaseModel):
    text: str = ""           # For raw text notes
    file_data: str = ""      # For Base64 encoded Image or Audio
    mime_type: str = "text/plain" # Tells us if it's text, png, jpeg, or mp3

@app.get("/")
def read_root():
    return {"status": "online", "message": "Multimodal BA Scribe is Ready"}

@app.post("/process-requirements")
async def process_notes(request: NoteRequest):
    try:
        # LOGIC: If file_data is provided, use it. Otherwise, use text.
        if request.file_data:
            print(f"Processing File: {request.mime_type}")
            result = generate_ba_docs(request.file_data, mime_type=request.mime_type)
        elif request.text:
            print("Processing Raw Text")
            result = generate_ba_docs(request.text, mime_type="text/plain")
        else:
            raise HTTPException(status_code=400, detail="No input provided (Text or File required)")

        return {"status": "success", "data": result}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port=int(os.environ.get("PORT", 8000))
    unvicorn.run(app, host="0.0.0", port=port)