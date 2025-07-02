# import streamlit as st
# from agent import run_agentic_research
# from fpdf import FPDF
# import base64
# import unicodedata
# from utils import generate_section, generate_detailed_sections_from_summary

# # ------------------- Session State Initialization -------------------
# for key in ["report", "sources", "abstract", "introduction", "methodology", "findings_results", "discussion_analysis", "conclusion"]:
#     if key not in st.session_state:
#         st.session_state[key] = "" if key != "sources" else []

# # ------------------- Streamlit UI Layout -------------------
# st.set_page_config(page_title="Agentic Research Assistant", layout="centered")
# st.title("Agentic Research Assistant")
# st.subheader("Your AI-powered academic report generator")

# title = st.text_input("Report Title", "Impact of AI on Education")
# subtitle = st.text_input("Subtitle (optional)", "")
# author = st.text_input("Author Name", "Jawaria Tariq")
# institution = st.text_input("Institution / Organization", "Virtual University")
# date = st.date_input("Report Date")
# query = st.text_area("Topic", "How does AI impact student learning in classrooms?")

# # ------------------- Unicode Cleaner -------------------
# def clean_text(text):
#     text = unicodedata.normalize('NFKD', text)
#     text = text.replace('’', "'").replace('“', '"').replace('”', '"')
#     return text.encode('latin-1', 'ignore').decode('latin-1')

# # ------------------- PDF Generator -------------------
# class PDF(FPDF):
#     def header(self):
#         if self.page_no() > 2:
#             self.set_font("Arial", "I", 9)
#             self.set_text_color(120)
#             self.cell(0, 10, "Agentic Research Report", 0, 1, "R")
#             self.ln(3)

#     def footer(self):
#         if self.page_no() > 1:
#             self.set_y(-15)
#             self.set_font("Arial", "I", 9)
#             self.set_text_color(120)
#             self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

# def generate_full_report_pdf(metadata, sections, sources, filename="formatted_report.pdf"):
#     pdf = PDF()
#     pdf.set_auto_page_break(auto=True, margin=15)

#     # Cover Page
#     pdf.add_page()
#     pdf.set_font("Arial", "B", 24)
#     pdf.set_text_color(0)
#     pdf.cell(0, 15, clean_text(metadata["title"]), ln=True, align="C")

#     if metadata.get("subtitle"):
#         pdf.set_font("Arial", "I", 14)
#         pdf.set_text_color(80)
#         pdf.cell(0, 10, clean_text(metadata["subtitle"]), ln=True, align="C")

#     pdf.ln(30)
#     pdf.set_font("Arial", "", 12)
#     pdf.set_text_color(50)
#     pdf.cell(0, 10, f"Author: {clean_text(metadata['author'])}", ln=True, align="C")
#     pdf.cell(0, 10, f"Institution: {clean_text(metadata['institution'])}", ln=True, align="C")
#     pdf.cell(0, 10, f"Date: {clean_text(metadata['date'])}", ln=True, align="C")

#     # Table of Contents
#     pdf.add_page()
#     pdf.set_font("Arial", "B", 18)
#     pdf.set_text_color(0)
#     pdf.cell(0, 10, "Table of Contents", ln=True)
#     pdf.ln(5)
#     pdf.set_font("Arial", "", 12)
#     toc_items = list(sections.keys()) + ["References"]
#     for i, item in enumerate(toc_items, start=1):
#         pdf.cell(0, 8, f"{i}. {clean_text(item)}", ln=True)

#     # Content Sections
#     for heading, content in sections.items():
#         pdf.add_page()
#         pdf.set_font("Arial", "B", 16)
#         pdf.set_text_color(0)
#         pdf.cell(0, 10, clean_text(heading), ln=True)
#         pdf.set_draw_color(150)
#         pdf.line(10, pdf.get_y(), 200, pdf.get_y())
#         pdf.ln(5)

#         pdf.set_font("Arial", "", 12)
#         pdf.set_text_color(30)
#         for para in clean_text(content).split("\n\n"):
#             pdf.multi_cell(0, 10, para)
#             pdf.ln(2)

#     # References
#     if sources:
#         pdf.add_page()
#         pdf.set_font("Arial", "B", 16)
#         pdf.set_text_color(0)
#         pdf.cell(0, 10, "References", ln=True)
#         pdf.line(10, pdf.get_y(), 200, pdf.get_y())
#         pdf.ln(5)

#         pdf.set_font("Arial", "", 11)
#         pdf.set_text_color(40)
#         for i, url in enumerate(sources, 1):
#             pdf.multi_cell(0, 8, f"{i}. {clean_text(url)}")
#             pdf.ln(1)

#     pdf.output(filename)
#     return filename

# # ------------------- Run Research & Generate Sections -------------------
# if st.button("Start Research"):
#     with st.spinner("Running agentic research..."):
#         result = run_agentic_research(query)
#         st.session_state.report = result["summary"]
#         st.session_state.sources = result["sources"]

#         detailed_sections = generate_detailed_sections_from_summary(st.session_state.report)

#         st.session_state.abstract = detailed_sections.get("Abstract", "")
#         st.session_state.introduction = detailed_sections.get("Introduction", "")
#         st.session_state.methodology = detailed_sections.get("Methodology", "")
#         st.session_state.findings_results = detailed_sections.get("Findings / Results", "")
#         st.session_state.discussion_analysis = detailed_sections.get("Discussion / Analysis", "")
#         st.session_state.conclusion = detailed_sections.get("Conclusion", "")

#         st.success("Research completed! You can now download your formatted report.")
#         st.markdown(st.session_state.report, unsafe_allow_html=True)

# # ------------------- Download Button -------------------
# if st.session_state.report and st.session_state.sources:
#     if st.button("Download Formatted Report"):
#         metadata = {
#             "title": title,
#             "subtitle": subtitle,
#             "author": author,
#             "institution": institution,
#             "date": str(date)
#         }

#         sections = {
#             "Abstract": st.session_state.abstract,
#             "Introduction": st.session_state.introduction,
#             "Methodology": st.session_state.methodology,
#             "Findings / Results": st.session_state.findings_results,
#             "Discussion / Analysis": st.session_state.discussion_analysis,
#             "Conclusion": st.session_state.conclusion
#         }

#         pdf_path = generate_full_report_pdf(metadata, sections, st.session_state.sources)
#         with open(pdf_path, "rb") as f:
#             base64_pdf = base64.b64encode(f.read()).decode("utf-8")
#         download_link = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="Formatted_Report.pdf">Click here to download your PDF</a>'
#         st.markdown(download_link, unsafe_allow_html=True)

# # ------------------- Display Sources -------------------
# if st.session_state.sources:
#     st.subheader("Sources")
#     for i, source in enumerate(st.session_state.sources, 1):
#         st.markdown(f"{i}. [{source}]({source})")


import streamlit as st
from agent import run_agentic_research
from fpdf import FPDF
import base64
import unicodedata
from utils import generate_section

# --- NEW: Concise and professional section generation ---
def generate_detailed_sections_from_summary(summary):
    section_prompts = {
        "Abstract": f"Summarize this report into a clear, concise academic abstract (max 4-5 sentences):\n\n{summary}",
        "Introduction": f"Write a brief and clear Introduction (no more than 1 short paragraph) explaining the purpose of the report:\n\n{summary}",
        "Methodology": f"Write a short Methodology section (under 150 words) explaining the approach used, without repeating the summary:\n\n{summary}",
        "Findings / Results": f"Write 2-3 concise bullet points summarizing the main findings or results from this summary:\n\n{summary}",
        "Discussion / Analysis": f"Write a brief, professional Discussion (max 150 words) based on the key issues raised in the report:\n\n{summary}",
        "Conclusion": f"Write a short conclusion (2-3 sentences max) summarizing the key insight or takeaway of this report:\n\n{summary}"
    }

    generated_sections = {}
    for section, prompt in section_prompts.items():
        try:
            response = generate_section(prompt)
            generated_sections[section] = response.strip()
        except Exception as e:
            generated_sections[section] = f"⚠️ Error generating {section}: {e}"

    return generated_sections

# ------------------- Session State Initialization -------------------
for key in ["report", "sources", "abstract", "introduction", "methodology", "findings_results", "discussion_analysis", "conclusion"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key != "sources" else []

# ------------------- Streamlit UI Layout -------------------
st.set_page_config(page_title="Agentic Research Assistant", layout="centered")
st.title("Agentic Research Assistant")
st.subheader("Your AI-powered academic report generator")

title = st.text_input("Report Title", "Impact of AI on Education")
subtitle = st.text_input("Subtitle (optional)", "")
author = st.text_input("Author Name", "Jawaria Tariq")
institution = st.text_input("Institution / Organization", "Virtual University")
date = st.date_input("Report Date")
query = st.text_area("Topic", "How does AI impact student learning in classrooms?")

# ------------------- Unicode Cleaner -------------------
def clean_text(text):
    text = unicodedata.normalize('NFKD', text)
    text = text.replace('’', "'").replace('“', '"').replace('”', '"')
    return text.encode('latin-1', 'ignore').decode('latin-1')

# ------------------- PDF Generator -------------------
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
    pdf.set_text_color(0)
    pdf.cell(0, 15, clean_text(metadata["title"]), ln=True, align="C")

    if metadata.get("subtitle"):
        pdf.set_font("Arial", "I", 14)
        pdf.set_text_color(80)
        pdf.cell(0, 10, clean_text(metadata["subtitle"]), ln=True, align="C")

    pdf.ln(30)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(50)
    pdf.cell(0, 10, f"Author: {clean_text(metadata['author'])}", ln=True, align="C")
    pdf.cell(0, 10, f"Institution: {clean_text(metadata['institution'])}", ln=True, align="C")
    pdf.cell(0, 10, f"Date: {clean_text(metadata['date'])}", ln=True, align="C")

    # Table of Contents
    pdf.add_page()
    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(0)
    pdf.cell(0, 10, "Table of Contents", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    toc_items = list(sections.keys()) + ["References"]
    for i, item in enumerate(toc_items, start=1):
        pdf.cell(0, 8, f"{i}. {clean_text(item)}", ln=True)

    # Content Sections
    pdf.add_page()
    for i, (heading, content) in enumerate(sections.items()):
        pdf.set_font("Arial", "B", 13)
        pdf.set_text_color(0)
        pdf.cell(0, 10, clean_text(heading), ln=True)
        pdf.set_draw_color(150)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

        pdf.set_font("Arial", "", 11)
        pdf.set_text_color(40)
        for para in clean_text(content).split("\n\n"):
            pdf.multi_cell(0, 9, para)
            pdf.ln(1)

        pdf.ln(2)

    # References
    if sources:
        pdf.ln(8)
        pdf.set_font("Arial", "B", 13)
        pdf.set_text_color(0)
        pdf.cell(0, 10, "References", ln=True)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(4)

        pdf.set_font("Arial", "", 10)
        pdf.set_text_color(40)
        for i, url in enumerate(sources, 1):
            pdf.multi_cell(0, 8, f"{i}. {clean_text(url)}")
            pdf.ln(1)

    pdf.output(filename)
    return filename

# ------------------- Run Research & Generate Sections -------------------
if st.button("Start Research"):
    with st.spinner("Running agentic research..."):
        result = run_agentic_research(query)
        st.session_state.report = result["summary"]
        st.session_state.sources = result["sources"]

        detailed_sections = generate_detailed_sections_from_summary(st.session_state.report)

        st.session_state.abstract = detailed_sections.get("Abstract", "")
        st.session_state.introduction = detailed_sections.get("Introduction", "")
        st.session_state.methodology = detailed_sections.get("Methodology", "")
        st.session_state.findings_results = detailed_sections.get("Findings / Results", "")
        st.session_state.discussion_analysis = detailed_sections.get("Discussion / Analysis", "")
        st.session_state.conclusion = detailed_sections.get("Conclusion", "")

        st.success("Research completed! You can now download your formatted report.")
        st.markdown(st.session_state.report, unsafe_allow_html=True)

# ------------------- Download Button -------------------
if st.session_state.report and st.session_state.sources:
    if st.button("Download Formatted Report"):
        metadata = {
            "title": title,
            "subtitle": subtitle,
            "author": author,
            "institution": institution,
            "date": str(date)
        }

        sections = {
            "Abstract": st.session_state.abstract,
            "Introduction": st.session_state.introduction,
            "Methodology": st.session_state.methodology,
            "Findings / Results": st.session_state.findings_results,
            "Discussion / Analysis": st.session_state.discussion_analysis,
            "Conclusion": st.session_state.conclusion
        }

        pdf_path = generate_full_report_pdf(metadata, sections, st.session_state.sources)
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
        download_link = f'<a href="data:application/octet-stream;base64,{base64_pdf}" download="Formatted_Report.pdf">Click here to download your PDF</a>'
        st.markdown(download_link, unsafe_allow_html=True)

# ------------------- Display Sources -------------------
if st.session_state.sources:
    st.subheader("Sources")
    for i, source in enumerate(st.session_state.sources, 1):
        st.markdown(f"{i}. [{source}]({source})")
