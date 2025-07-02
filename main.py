
import streamlit as st
from datetime import date
from agent import run_agentic_research
from fpdf import FPDF
import base64
import unicodedata
from utils import generate_section

# Set page configuration
st.set_page_config(page_title="📘 Agentic Research Assistant", layout="centered")

# Page title and subtitle
st.markdown("<h1 style='text-align: center;'>📘 Agentic Research Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Your AI-powered academic report generator</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Clean Text Utility ---
def clean_text(text):
    text = unicodedata.normalize('NFKD', text)
    return text.replace("’", "'").replace("“", '"').replace("”", '"').encode("latin-1", "ignore").decode("latin-1")

# --- Section Header ---
st.markdown("### ✍️ Report Information")
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Report Title", "The Role of AI in Education")
        author = st.text_input("Author", "Ms. Jawaria Tariq")
    with col2:
        institution = st.text_input("Institution", "Virtual University")
        date_value = st.date_input("Report Date", value=date.today())

    subtitle = st.text_input("Subtitle (optional)", "Trends, Opportunities and Concerns in 2024")

# --- Research Topic Section ---
st.markdown("### 🔍 Research Topic")
query = st.text_area("Enter your research topic here:", "How is artificial intelligence innovation creating ethical challenges in 2024?")

# --- Generate Sections using Gemini or LLaMA backend ---
def generate_detailed_sections_from_summary(summary):
    section_prompts = {
        "Abstract": f"Summarize this report into a clear, concise academic abstract (max 4-5 sentences):\n\n{summary}",
        "Introduction": f"Write a brief and clear Introduction (no more than 2 short paragraph) explaining the purpose of the report:\n\n{summary}",
        "Methodology": f"Write a short Methodology section (under 200 words) explaining the approach used:\n\n{summary}",
        "Findings / Results": f"Write 3-5 concise bullet points summarizing the main findings or results:\n\n{summary}",
        "Discussion / Analysis": f"Write a professional Discussion (max 150 words) based on key issues:\n\n{summary}",
        "Conclusion": f"Write a short conclusion (2-3 sentences max):\n\n{summary}",
    }
    output = {}
    for section, prompt in section_prompts.items():
        output[section] = generate_section(prompt)
    return output

# --- PDF Generation ---
class PDF(FPDF):
    def header(self):
        if self.page_no() > 2:
            self.set_font("Arial", "I", 9)
            self.set_text_color(120)
            self.cell(0, 10, "Agentic Research Report", 0, 1, "R")
            self.ln(3)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-15)
            self.set_font("Arial", "I", 9)
            self.set_text_color(120)
            self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def generate_full_report_pdf(metadata, sections, sources, filename="formatted_report.pdf"):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Cover Page
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 15, clean_text(metadata["title"]), ln=True, align="C")
    if metadata.get("subtitle"):
        pdf.set_font("Arial", "I", 14)
        pdf.cell(0, 10, clean_text(metadata["subtitle"]), ln=True, align="C")
    pdf.ln(30)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Author: {clean_text(metadata['author'])}", ln=True, align="C")
    pdf.cell(0, 10, f"Institution: {clean_text(metadata['institution'])}", ln=True, align="C")
    pdf.cell(0, 10, f"Date: {clean_text(metadata['date'])}", ln=True, align="C")

    # Table of Contents
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "Table of Contents", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    for i, item in enumerate(list(sections.keys()) + ["References"], 1):
        pdf.cell(0, 8, f"{i}. {clean_text(item)}", ln=True)

    # Content
    pdf.add_page()
    for section, content in sections.items():
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, clean_text(section), ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        pdf.set_font("Arial", "", 11)
        for para in clean_text(content).split("\n\n"):
            pdf.multi_cell(0, 9, para)
            pdf.ln(1)
        pdf.ln(2)

    # References
    if sources:
        pdf.ln(8)
        pdf.set_font("Arial", "B", 13)
        pdf.cell(0, 10, "References", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)
        pdf.set_font("Arial", "", 10)
        for i, url in enumerate(sources, 1):
            pdf.multi_cell(0, 8, f"{i}. {clean_text(url)}")
            pdf.ln(1)

    pdf.output(filename)
    return filename

# --- Session Storage ---
for key in ["report", "sources", "abstract", "introduction", "methodology", "findings_results", "discussion_analysis", "conclusion"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "sources" else []

# --- Button to run research ---
if st.button("🚀 Start Research"):
    with st.spinner("Running agentic research..."):
        result = run_agentic_research(query)
        st.session_state.report = result["summary"]
        st.session_state.sources = result["sources"]
        generated = generate_detailed_sections_from_summary(st.session_state.report)
        st.session_state.abstract = generated["Abstract"]
        st.session_state.introduction = generated["Introduction"]
        st.session_state.methodology = generated["Methodology"]
        st.session_state.findings_results = generated["Findings / Results"]
        st.session_state.discussion_analysis = generated["Discussion / Analysis"]
        st.session_state.conclusion = generated["Conclusion"]
        st.success("✅ Research completed!")

# --- Download Button ---
if st.session_state.report and st.session_state.sources:
    if st.button("📄 Download Formatted Report as PDF"):
        metadata = {
            "title": title,
            "subtitle": subtitle,
            "author": author,
            "institution": institution,
            "date": str(date_value)
        }
        sections = {
            "Abstract": st.session_state.abstract,
            "Introduction": st.session_state.introduction,
            "Methodology": st.session_state.methodology,
            "Findings / Results": st.session_state.findings_results,
            "Discussion / Analysis": st.session_state.discussion_analysis,
            "Conclusion": st.session_state.conclusion
        }
        file_path = generate_full_report_pdf(metadata, sections, st.session_state.sources)
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown(f'<a href="data:application/octet-stream;base64,{b64}" download="Formatted_Report.pdf">📥 Click here to download your PDF</a>', unsafe_allow_html=True)

# --- Display Sources Section ---
if st.session_state.sources:
    st.markdown("### 🔗 Sources")
    for i, src in enumerate(st.session_state.sources, 1):
        st.markdown(f"{i}. [{src}]({src})")
# --- Footer ---
st.markdown("---")  
st.markdown("<p style='text-align: center; color: grey;'>Powered by Agentic Research Assistant</p>", unsafe_allow_html=True)


