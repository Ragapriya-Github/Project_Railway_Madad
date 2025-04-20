import time
import random
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# Set up the Gemini API
genai.configure(api_key="YOUR_API_KEY_HERE")

# Initialize FastAPI app
app = FastAPI()

# Complaint model to handle the request body
class ComplaintRequest(BaseModel):
    complaint: str

# Simulated API function (Replace with actual API call)
def classify_complaint_with_api(complaint):
    # Simulating an API failure due to quota limits (randomly)
    if random.random() < 0.3:  # 30% chance of failure
        return "API_ERROR"

    # Simulating API-based classification
    api_responses = {
        "train is late": "Service Delay",
        "train is not on time": "Punctuality",
        "water leakage": "Infrastructure",
        "fight in train": "Safety",
        "seats are torn": "Maintenance",
        "staff was rude": "Staff Behavior"
    }

    return api_responses.get(complaint.lower(), "General Inquiry")

# Fallback rule-based classification
def classify_complaint_fallback(complaint):
    keywords = {
        "late": "Punctuality",
        "delay": "Punctuality",
        "water": "Infrastructure",
        "leak": "Infrastructure",
        "fight": "Safety",
        "accident": "Safety",
        "dirty": "Cleanliness",
        "rude": "Staff Behavior",
        "broken": "Maintenance",
        "torn": "Maintenance"
    }

    for key, category in keywords.items():
        if key in complaint.lower():
            return category

    return "General Inquiry"

# Define route for classification
@app.post("/classify_complaint/")
def classify_complaint(request: ComplaintRequest):
    complaint = request.complaint.strip()
    
    # Try API classification
    category = classify_complaint_with_api(complaint)

    # If API fails, use fallback method
    if category == "API_ERROR":
        category = classify_complaint_fallback(complaint)
        return {"complaint": complaint, "category": category}
    else:
        return {"complaint": complaint, "category": category}

# Root endpoint for testing purposes
@app.get("/")
def read_root():
    return {"message": "Welcome to the Railway Complaint Classification API"}
