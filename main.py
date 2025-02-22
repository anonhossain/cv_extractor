from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import shutil
import pandas as pd
from cv_processor import CVProcessor

app = FastAPI()

# Temporary folder to store uploaded files and generated CSVs
UPLOAD_FOLDER = "./uploaded_cvs"
CSV_FOLDER = "./generated_csvs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CSV_FOLDER, exist_ok=True)

# Initialize CVProcessor
processor = CVProcessor(folder_path=UPLOAD_FOLDER)


@app.get("/")
def read_root():
    return {"message": "Welcome to the CV Processor API!"}


@app.post("/cv-extractor/")
async def upload_and_generate_csv(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    # Validate and save PDF files
    saved_files = []
    for file in files:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}. Only PDFs are allowed.")
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file_path)

    # Process each CV and collect data
    processed_data = []
    for file_path in saved_files:
        try:
            candidate_data = processor.process_cv(file_path)
            processed_data.append(candidate_data)
        except Exception as e:
            return {"error": f"Failed to process {os.path.basename(file_path)}: {str(e)}"}

    # Generate CSV
    csv_file_path = os.path.join(CSV_FOLDER, "processed_cvs.csv")
    df = pd.DataFrame(processed_data)
    df.to_csv(csv_file_path, index=False)

    # Return the CSV file as a response
    return FileResponse(csv_file_path, media_type="text/csv", filename="processed_cvs.csv")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
