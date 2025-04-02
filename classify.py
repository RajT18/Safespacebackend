from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow all origins (for development, restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PicPurify API details
PICPURIFY_URL = "https://www.picpurify.com/analyse/1.1"
API_KEY = os.getenv("PICPURIFY_API_KEY")  # Load API key from .env file

@app.post("/classify")
async def classify_image(file: UploadFile = File(...)):
    try:
        # Check if API key is missing
        if not API_KEY:
            return {"error": "Missing API key. Set PICPURIFY_API_KEY in environment variables."}

        # Read the uploaded file
        file_content = await file.read()

        # Prepare data for PicPurify
        img_data = {
            "file_image": (file.filename, file_content)
        }
        payload = {
            "API_KEY": API_KEY,
            "task": "porn_moderation,drug_moderation,gore_moderation"
        }

        # Send request to PicPurify
        response = requests.post(PICPURIFY_URL, files=img_data, data=payload)

        # Handle response
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": "Failed to classify the image",
                "status_code": response.status_code,
                "details": response.text,
            }

    except Exception as e:
        return {"error": "An unexpected error occurred", "details": str(e)}
