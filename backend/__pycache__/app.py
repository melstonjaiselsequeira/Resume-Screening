from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from typing import List
import uvicorn

from parser import extract_text
from model import calculate_similarity
from utils import init_db, save_resume, update_resume_score, clear_resumes

app = FastAPI(title="Smart Resume Screening API")

# Setup CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'uploads'))
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Initialize database
init_db()

@app.post("/api/screen")
async def screen_resumes(job_description: str = Form(...), files: List[UploadFile] = File(...)):
    # Clear previous run data
    clear_resumes()
    
    resumes_data = []
    
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse text
        parsed_text = extract_text(file_path)
        
        # Simple extraction for candidate name (using filename without extension)
        candidate_name = os.path.splitext(file.filename)[0].replace('_', ' ').replace('-', ' ').title()
        
        # Save to DB
        resume_id = save_resume(file.filename, candidate_name, parsed_text)
        
        resumes_data.append({
            'id': resume_id,
            'filename': file.filename,
            'candidate_name': candidate_name,
            'text': parsed_text
        })
        
    # Calculate similarity
    scored_resumes = calculate_similarity(job_description, resumes_data)
    
    # Update DB and format response
    results = []
    for r in scored_resumes:
        update_resume_score(r['id'], r['score'], r['rank'])
        results.append({
            'rank': r['rank'],
            'candidate_name': r['candidate_name'],
            'score': r['score'],
            'filename': r['filename']
        })
        
    return {"message": "Success", "results": results}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    