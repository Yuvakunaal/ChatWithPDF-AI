# PDF Query Assistant with OCR

![AI-Powered](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=ai) ![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green?style=for-the-badge&logo=fastapi) ![Ollama-Mistral](https://img.shields.io/badge/Ollama-Mistral-informational?style=for-the-badge) ![OCR-Enabled](https://img.shields.io/badge/OCR-Enabled-orange?style=for-the-badge&logo=ocr)

PDF Query Assistant is an intelligent web application that allows users to extract information from PDF documents using natural language queries. It supports both text-based and scanned PDFs through OCR technology, powered by the Mistral AI model via Ollama.

## 🚀 Features

- 📄 **PDF Upload & Processing**: Upload PDF documents via drag-and-drop or file browser.
- 🔍 **Dual Extraction Methods**

  - Text extraction from standard PDFs using PyMuPDF.
  - OCR processing for scanned PDFs using Tesseract.

- 🤖 **AI-Powered Querying**: Ask natural language questions about your PDF content using the Mistral model.

- 📱 **Responsive Design**: Clean, professional interface with dark mode support.

- ⚡ **Real-time Processing**: Instant responses to your PDF queries.

- 📊 **Content Analysis**: Extract insights, summaries, and specific information from documents.

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **AI Processing**: Ollama with Mistral model
- **PDF Processing**: PyMuPDF (fitz)
- **OCR Engine**: Tesseract OCR
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: Uvicorn ASGI server

## 🛠️ Installation & Setup

### Clone the Repository

```bash
git clone https://github.com/Yuvakunaal/ChatWithPDF-AI.git
cd ChatWithPDF-AI
```

### Install Python Dependencies

```bash
pip install fastapi uvicorn pymupdf ollama pydantic python-multipart pillow pytesseract
```

### Install Tesseract OCR

- Windows: Download from UB-Mannheim/tesseract
- macOS: `bash brew install tesseract`
- Linux (Ubuntu/Debian): `bash sudo apt install tesseract-ocr`
- Linux (Fedora): `bash sudo dnf install tesseract`

### Download Ollama

- Visit the [Ollama website](https://ollama.ai) and download the application.
- Open your terminal and run:
  ```bash
  ollama pull mistral:instruct
  ```
- The Ollama model is now downloaded on your system.

### Run the Application

```bash
uvicorn app:app --reload
```

**Open Browser** : Navigate to http://127.0.0.1:8000/

# 🎯 How It Works

**Upload PDF**: Drag and drop or select a PDF file.

**Automatic Processing**:

- The system first attempts standard text extraction.
- If text content is minimal (scanned PDF), it automatically uses OCR.

**Ask Questions**: Type natural language questions about the document.

**Get Answers**: AI analyzes the PDF content and provides accurate responses.

# 🔮 Usage Examples

Ask questions like:

- "What is this document about?"
- "Summarize the main points."
- "List all the key findings."
- "What are the recommendations in section 3?"
- "Extract all dates mentioned in the document."
- "Who are the authors of this paper?"

The application analyzes the PDF content and provides precise answers based solely on the document information.

# 🌟 Advanced Features

- 🤖 **Intelligent Context Handling**: AI understands document structure and references specific sections.
- 📄 **Scanned PDF Support**: Automatic OCR processing for image-based PDFs.
- 🔒 **Privacy-Focused**: All processing happens locally on your machine.
- ⚡ **Performance Optimized**: Efficient text extraction and query processing.
- 📱 **Mobile Responsive**: Works seamlessly on desktop and mobile devices.

# 👨‍💻 Developer

Kunaal – AI, Python, and Web Development Enthusiast

# 🙏 Acknowledgments

- Ollama for enabling local AI model integration.
- FastAPI for providing a high-performance backend framework.
- PyMuPDF and Tesseract for PDF processing capabilities.
- The open-source community for the libraries and tools used.

> ⭐ If you find this project useful, please consider starring the repository!
