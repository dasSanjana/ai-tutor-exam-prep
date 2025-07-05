# ai-tutor-exam-prep

An AI-powered tutor web app built using Streamlit, LangChain, and Ollama (Mistral model). It helps students prepare for academic exams , technical exams and interviews.

---

## 🚀 Features

- 📄 Upload syllabus (.txt or .pdf)
- ❓ Ask topic-based questions
- 📋 Generate summaries and explanations
- 🧠 Auto-generate MCQs (1–100)
- 📥 Download response as PDF

---

## 🧠 Technologies Used

- [Streamlit](https://streamlit.io/) – Frontend
- [LangChain](https://www.langchain.com/) – RAG framework
- [ChromaDB](https://www.trychroma.com/) – Local vector database
- [Ollama](https://ollama.com) – Runs open-source models like `mistral`
- [FPDF](https://pyfpdf.github.io/fpdf2/) – Generate PDFs

---

## 🛠️ Setup Instructions

###  1. Clone this Repo

```bash
git clone https://github.com/dasSanjana/ai-tutor-exam-prep.git
cd ai-tutor-exam-prep

```
###  2. Create Virtual 
python3 -m venv venv
source venv/bin/activate  # macOS/Linux

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Start Ollama + Pull Model
ollama run mistral

### 5. Run the App
streamlit run main.py

