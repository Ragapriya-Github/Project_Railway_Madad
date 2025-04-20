import time
import random
from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
import uvicorn

# Set up the Gemini API
genai.configure(api_key="AIzaSyDPaTFb1E9-3XFKdFEiZxIXw1ojsnDLPjw")

# Initialize FastAPI app
app = FastAPI()

# Complaint model to handle the request body
class ComplaintRequest(BaseModel):
    complaint: str

# Simulated API function (Replace with actual API call)
def classify_complaint_with_api(complaint):
    # Simulate random API failure
    if random.random() < 0.3:
        return "API_ERROR"

    keywords = {
        "garbage": "Cleanliness",
        "dirty": "Cleanliness",
        "toilet": "Cleanliness",
        "broken": "Damage",
        "seat": "Damage",
        "window": "Damage",
        "facility": "Damage",
        "staff": "Staff",
        "rude": "Staff",
        "service": "Staff",
        "ac": "Electrical Issues",
        "fan": "Electrical Issues",
        "charging": "Electrical Issues",
        "light": "Electrical Issues"
    }

    matched_categories = set()

    for key, category in keywords.items():
        if key in complaint.lower():
            matched_categories.add(category)

    return list(matched_categories) if matched_categories else ["Others"]
    
# Fallback rule-based classification
def classify_complaint_fallback(complaint):
    keywords = {
        "garbage": "Cleanliness",
        "dirty": "Cleanliness",
        "toilet": "Cleanliness",
        "broken": "Damage",
        "seat": "Damage",
        "window": "Damage",
        "facility": "Damage",
        "staff": "Staff",
        "rude": "Staff",
        "service": "Staff",
        "ac": "Electrical Issues",
        "fan": "Electrical Issues",
        "charging": "Electrical Issues",
        "light": "Electrical Issues"
    }

    matched_categories = set()

    for key, category in keywords.items():
        if key in complaint.lower():
            matched_categories.add(category)

    return list(matched_categories) if matched_categories else ["Others"]
    
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
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
