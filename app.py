import streamlit as st
import fitz
import requests
import tempfile
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PDF AI Assistant",
    layout="wide"
)

# ---------------- FUNCTIONS ----------------
def extract_text(pdf_path):
    """Extract text from PDF"""
    text = ""

    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text("text")

        doc.close()

    except Exception as e:
        st.error(f"Error reading PDF: {e}")

    return text


def ask_ollama(prompt):
    """Send prompt to Ollama model"""
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False
            },
            timeout=180
        )

        return response.json()["response"]

    except Exception as e:
        return f"Error connecting to Ollama: {e}"


def summarize_text(text):
    """Generate summary"""
    prompt = f"""
You are a helpful assistant.

Summarize the following PDF content clearly.

Give output in this format:

1. Executive Summary
2. 5 Key Points
3. Important Insights
4. Final Conclusion

PDF Content:
{text[:100000]}
"""
    return ask_ollama(prompt)


def ask_question(text, question):
    """Ask question based on PDF"""
    prompt = f"""
Answer ONLY using the PDF content below.
If answer is not found, say: Not found in document.

PDF Content:
{text[:100000]}

Question:
{question}
"""
    return ask_ollama(prompt)


# ---------------- UI ----------------
st.title("📄 PDF AI Assistant")
st.write("Upload PDF → Summarize → Ask Questions")

# Sidebar
st.sidebar.header("Settings")
st.sidebar.write("Model: llama3.2:1b")
st.sidebar.write("Backend: Ollama")

uploaded_file = st.file_uploader("Upload PDF File", type="pdf")

if uploaded_file:

    # Save temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        temp_path = tmp_file.name

    # Extract text
    with st.spinner("Reading PDF..."):
        text = extract_text(temp_path)

    if text.strip() == "":
        st.error("No readable text found in PDF.")
    else:
        st.success("PDF Loaded Successfully!")

        col1, col2 = st.columns(2)

        # ---------- SUMMARY ----------
        with col1:
            st.subheader("📌 Generate Summary")

            if st.button("Summarize PDF"):
                with st.spinner("Generating summary..."):
                    summary = summarize_text(text)

                st.write(summary)

        # ---------- Q&A ----------
        with col2:
            st.subheader("❓ Ask Questions")

            question = st.text_input("Enter your question")

            if st.button("Ask PDF"):
                if question.strip() == "":
                    st.warning("Please enter a question.")
                else:
                    with st.spinner("Thinking..."):
                        answer = ask_question(text, question)

                    st.write(answer)

        # ---------- TEXT PREVIEW ----------
        with st.expander("📄 Extracted Text Preview"):
            st.write(text[:3000])

    # Delete temp file
    os.remove(temp_path)

else:
    st.info("Upload a PDF file to begin.")