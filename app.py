from fastapi import FastAPI, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import fitz  # PyMuPDF
from ollama_model import ollama_call
import uuid
import tempfile
import os
from PIL import Image
import pytesseract
import io
import base64

app = FastAPI(title="PDF Query Assistant with OCR")

# Store uploaded files in memory (for demo purposes)
uploaded_files = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/templates", StaticFiles(directory="templates"), name="templates")

class QueryRequest(BaseModel):
    file_id: str
    user_query: str

def extract_text_from_pdf(file_content):
    """Extract text from PDF using PyMuPDF (for text-based PDFs)"""
    doc = fitz.open(stream=file_content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_scanned_pdf(file_content):
    """Extract text from scanned PDF using OCR"""
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(file_content)
        tmp_path = tmp_file.name
    
    try:
        # Open the PDF and extract images from each page
        doc = fitz.open(tmp_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # Get the pixmap of the page (image)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Higher resolution for better OCR
            img_data = pix.tobytes("png")
            
            # Convert to PIL Image
            image = Image.open(io.BytesIO(img_data))
            
            # Use Tesseract to do OCR on the image
            page_text = pytesseract.image_to_string(image, lang='eng')
            text += f"\n--- Page {page_num + 1} ---\n" + page_text + "\n"
        
        return text, True  # Return text and flag indicating OCR was used
    finally:
        # Clean up the temporary file
        os.unlink(tmp_path)

def extract_file_content(file_content):
    """Extract text from PDF, trying standard method first and OCR as fallback"""
    # First try standard text extraction
    text = extract_text_from_pdf(file_content)
    
    # If little or no text was extracted, try OCR
    if len(text.strip()) < 50:  # Threshold for considering it a scanned PDF
        print("Using OCR for text extraction (scanned PDF detected)")
        ocr_text, used_ocr = extract_text_from_scanned_pdf(file_content)
        return ocr_text, True
    
    return text, False

@app.get("/")
async def home():
    return FileResponse("templates/index.html")

@app.get("/about")
async def about():
    return FileResponse("templates/about.html")

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile):
    try:
        # Check if file is a PDF
        if not file.filename.lower().endswith('.pdf'):
            return JSONResponse(
                content={"error": "File must be a PDF"}, 
                status_code=400
            )
        
        # Read the file content
        file_content = await file.read()
        
        # Generate a unique ID for this file
        file_id = str(uuid.uuid4())
        
        # Extract content
        pdf_content, used_ocr = extract_file_content(file_content)
        
        # Store content with ID
        uploaded_files[file_id] = {
            "filename": file.filename,
            "content": pdf_content
        }
        
        return JSONResponse(
            content={
                "file_id": file_id, 
                "filename": file.filename,
                "used_ocr": used_ocr,
                "message": "PDF uploaded and processed successfully"
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to process PDF: {str(e)}"}, 
            status_code=500
        )

@app.post("/query-pdf")
async def query_pdf(request: QueryRequest):
    try:
        # Retrieve stored file content
        if request.file_id not in uploaded_files:
            raise HTTPException(status_code=404, detail="File not found")
        
        pdf_content = uploaded_files[request.file_id]["content"]
        answer = ollama_call(pdf_content, request.user_query)
        return JSONResponse(content={"answer": answer})
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)}, 
            status_code=500
        )

# Add a new endpoint to check if OCR is available
@app.get("/health/ocr")
async def check_ocr_health():
    try:
        # Test if Tesseract is installed and working
        pytesseract.get_tesseract_version()
        return JSONResponse(
            content={"status": "OK", "message": "OCR is available"}
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "Error", "message": f"OCR not available: {str(e)}"},
            status_code=503
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8020)