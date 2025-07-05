import streamlit as st
from rag_chain import (
    load_and_embed,
    get_retriever,
    answer_query,
    generate_summary,
    generate_mcqs,
    generate_explanation
)
from langchain_community.llms import Ollama
from fpdf import FPDF
import io
import os
import textwrap

# ---------------------------- Session Init ----------------------------
if "result" not in st.session_state:
    st.session_state["result"] = None


# ---------------------------- App Title ----------------------------
st.set_page_config(page_title="AI Tutor", layout="centered")
st.title("📘 AI Tutor")

# ---------------------------- Upload File ----------------------------
uploaded_file = st.file_uploader("Upload syllabus/notes (.txt or .pdf)", type=["txt", "pdf"])

if uploaded_file:
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Embedding your syllabus..."):
        load_and_embed(file_path)
        st.session_state["retriever"] = get_retriever()
        st.session_state["llm"] = Ollama(model="mistral")
        st.success("✅ File processed and ready!")

# ---------------------------- Main Interaction ----------------------------
if "retriever" in st.session_state:
    mode = st.selectbox("Choose mode:", ["Ask Question", "Get Summary", "Get MCQs", "Get Explanation"])
    topic = st.text_input("Enter your topic or question:")

    if mode == "Get MCQs":
        num_mcqs = st.number_input("How many MCQs would you like to generate?", min_value=1, max_value=100, value=3)
    else:
        num_mcqs = 3

    if st.button("Submit"):
        with st.spinner("Generating response..."):
            llm = st.session_state["llm"]
            retriever = st.session_state["retriever"]

            if mode == "Ask Question":
                st.session_state["result"] = answer_query(retriever, topic)
            elif mode == "Get Summary":
                st.session_state["result"] = generate_summary(topic)
            elif mode == "Get MCQs":
                st.session_state["result"] = generate_mcqs(topic, num_mcqs)
            elif mode == "Get Explanation":
                st.session_state["result"] = generate_explanation(topic)
            else:
                st.session_state["result"] = "❌ Invalid mode."

# ---------------------------- Display Result ----------------------------
if st.session_state["result"]:
    st.markdown("### 🧠 Result")
    st.write(st.session_state["result"])

    # PDF generation using Unicode-safe font
   

    def generate_pdf_bytes(text: str) -> bytes:
        """
        Generates a PDF from a string of multiple-choice questions.

        Args:
            text: A string containing the MCQs. It is assumed that questions
                are prefixed with a number (e.g., "1.") and options are
                prefixed with a letter (e.g., "a.").

        Returns:
            The PDF content as bytes.
        """
        pdf = FPDF()
        pdf.add_page()

        # It's crucial to add a Unicode-compatible font for broad character support.
        # Ensure 'DejaVuSans.ttf' is in a 'fonts' directory.
        try:
            font_path = os.path.join("fonts", "DejaVuSans.ttf")
            if not os.path.exists(font_path):
                # Fallback to a standard font if DejaVu is not available.
                st.warning("DejaVuSans.ttf not found. Using 'Arial'. Some characters may not render correctly.")
                pdf.set_font("Arial", size=12)
            else:
                pdf.add_font("DejaVu", "", font_path, uni=True)
                pdf.set_font("DejaVu", size=12)
        except Exception as e:
            st.error(f"Failed to load font: {e}")
            pdf.set_font("Arial", size=12)


        # Set margins to provide some spacing from the page edges.
        pdf.set_left_margin(10)
        pdf.set_right_margin(10)
        pdf.set_top_margin(10)

        # Process the input text to separate questions and options.
        lines = text.strip().split('\n')
        
        question_block = ""
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # This logic assumes questions start with a number (e.g., "1.", "2) ").
            # You may need to adjust the condition based on your exact text format.
            if line.split('.')[0].isdigit() and question_block:
                # Write the previous question block to the PDF.
                pdf.multi_cell(0, 10, question_block)
                pdf.ln(5) # Add a little space after the question.
                question_block = line
            else:
                if not question_block:
                    question_block = line
                else:
                    # Append options to the current question block.
                    question_block += "\n" + line


        # Add the last question block to the PDF.
        if question_block:
            pdf.multi_cell(0, 10, question_block)

        # Generate the PDF content in memory.
        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        return pdf_output.read()

    pdf_bytes = generate_pdf_bytes(st.session_state["result"])
    st.download_button(
        label="📄 Download Result as PDF",
        data=pdf_bytes,
        file_name="ai_tutor_response.pdf",
        mime="application/pdf"
    )
