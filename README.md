# 📄 CV Processor API

## Oveview

The CV Processor API is a FastAPI-based service that extracts candidate details (name, email, phone, references) from uploaded PDF resumes and generates a CSV file containing structured information.

It also includes a Jupyter Notebook (processor.ipynb) for testing the functionality in a console environment.

## 📂 Project Structure

📁 cv-processor-api/
│── main.py # FastAPI application for file upload and processing
│── cv_processor.py # CV extraction and processing logic
│── processor.ipynb # Jupyter Notebook for testing the processor
│── requirements.txt # Dependencies
│── README.md # Project documentation
│── uploaded_cvs/ # Directory for storing uploaded CVs (auto-created)
│── generated_csvs/ # Directory for storing generated CSVs (auto-created)

## API Endpoints:

### Upload CVs and Extract Data

URL: POST /cv-extractor/
Description: Upload multiple PDF resumes, extract candidate information, and generate a CSV file.

## 🏗️ How It Works

-> Uploads PDF resumes to uploaded_cvs/.
-> Extracts candidate name (from filename), email, phone number, and references.
-> Formats & validates extracted data.
-> Generates a CSV file containing structured data.
-> Returns the CSV file as a downloadable response.

## Testing in Console

Open processor.ipynb, which contains the python files of:

-> Uploading CV
-> Extracting candidate details
-> Saving the results in EXCEL

## Dependencies

The project requires the following libraries:
fastapi
uvicorn
pandas
pdfminer.six
openpyxl

Install them using pip:
pip install -r requirements.txt
