#  PDF AI Assistant

An AI-powered PDF assistant that allows users to upload PDF documents, generate concise summaries, and ask questions based on the document content using a locally hosted LLM through Ollama.

## Features

-  Upload PDF files
-  Extract text from PDFs
-  Generate AI-powered summaries
-  Ask questions about the uploaded document
-  Powered by Ollama (Llama 3.2:1B)

## Tech Stack

- Python
- Streamlit
- Ollama
- PyMuPDF (fitz)
- Requests

## Installation

1. Clone the repository

```bash
git clone https://github.com/BhumikaShankar/AI-PDF-Summarizer.git
cd PDF-AI-Assistant
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Start Ollama

```bash
ollama run llama3.2:1b
```

4. Run the application

```bash
streamlit run app.py
```

## Usage

- Upload a PDF document.
- Click **Summarize PDF** to generate a summary.
- Ask questions related to the uploaded document.

