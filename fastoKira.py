#fastoKira.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
from services.flowchart_generator import parse_code_to_flowchart
from services.codeparse34 import parse_python_code
from services.Analyzekira34 import analyze_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # explicitly allow your React frontend
    allow_credentials=True,                    # enable credentials if needed (cookies, auth)
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-analyze/")
async def upload_and_analyze(file: UploadFile = File(...)):
    file_location = f"temp/{file.filename}"
    os.makedirs("temp", exist_ok=True)
    
    # Save uploadedfile
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Read raw code for flowchart generation
    with open(file_location, "r", encoding="utf-8") as f:
        raw_code = f.read()

    # Parse the code
    code_data = parse_python_code(file_location)

    # Analyze the code
    results = analyze_code(code_data)

    # Generate Mermaid flowchart
    flowchart_mermaid = parse_code_to_flowchart(raw_code)

    # Return all data
    return {
        "filename": file.filename,
        "analysis": results,
        "flowchart": flowchart_mermaid
    }
