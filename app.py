import streamlit as st
from matcher.keyword_matcher import match_keywords
from matcher.parser import extract_text_from_pdf
import os

st.title("🔍 Resume & Job Description Matcher")

st.markdown("Upload your resume and the job description to check for keyword alignment and get improvement tips.")

resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])
jd_input = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if resume_file and jd_input:
        resume_text = extract_text_from_pdf(resume_file)
        result = match_keywords(resume_text, jd_input)
        st.markdown(f"### Match Score: {result['score']}%")
        st.markdown("**Missing Keywords:**")
        st.write(result['missing_keywords'])
    else:
        st.error("Please upload a resume and paste a job description.")