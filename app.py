# ---------- app.py (Streamlit Frontend Entry Point) ----------
import streamlit as st
from matcher.keyword_matcher import match_keywords, extract_skills, SKILL_CATEGORIES
from matcher.parser import extract_text_from_pdf
import os
import re

# Web scraping tools
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="Resume Matcher", layout="wide")
st.title("🔍 Resume & Job Description Matcher")

st.markdown("Upload your resume and paste a job description or fetch one from LinkedIn to receive a skill match score and suggestions.")

resume_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

def fetch_job_description(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)  # wait for JS to load
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    # Try LinkedIn
    if "linkedin.com" in url:
        content = soup.find("div", class_="description__text")
        if content:
            return content.get_text("\n")
    # Try Indeed
    elif "indeed.com" in url:
        content = soup.find("div", id="jobDescriptionText")
        if content:
            return content.get_text("\n")
    # Try Lever
    elif "lever.co" in url:
        content = soup.find("div", class_="content")
        if content:
            return content.get_text("\n")

    return "Job description could not be fetched."

job_url = st.text_input("🔗 Optional: Paste a Job URL from LinkedIn, Indeed, or Lever")
if st.button("Fetch JD from URL") and job_url:
    with st.spinner("Fetching job description..."):
        jd_fetched = fetch_job_description(job_url).strip().replace('  ', ' ')
        st.session_state.jd_input = jd_fetched

jd_input = st.text_area("Paste Job Description", value=st.session_state.get("jd_input", ""))
st.session_state.jd_input = jd_input

if "result" not in st.session_state:
    st.session_state.result = None

if st.button("Analyze"):
    if resume_file and jd_input:
        resume_text = extract_text_from_pdf(resume_file)
        result = match_keywords(resume_text, jd_input)

        st.session_state.resume_text = resume_text
        st.session_state.jd_input = jd_input
        st.session_state.result = result

if st.session_state.result:
    result = st.session_state.result
    resume_text = st.session_state.resume_text
    jd_input = st.session_state.jd_input

    st.markdown(f"### ✅ Final Match Score: {result['score']}%")
    st.markdown(f"- **Keyword Match Score:** {result['keyword_score']}%")
    st.markdown(f"- **Skill Match Score:** {result['skill_score']}%")

    with st.expander("📊 Skill Category Breakdown"):
        for cat, score in result['category_scores'].items():
            st.write(f"**{cat.title()}**: {score}%")

    st.markdown("---")
    tabs = st.tabs(["🧠 Extracted Skills", "📄 Highlighted JD", "🧼 Missing Keywords"])

    with tabs[0]:
        st.markdown("### 🧠 Extracted Skills Comparison")
        resume_skills = extract_skills(resume_text, SKILL_CATEGORIES)
        jd_skills = extract_skills(jd_input, SKILL_CATEGORIES)

        # Filter resume skills to only include those also in JD
        resume_skills = {
            cat: [s for s in skills if s in jd_skills.get(cat, [])]
            for cat, skills in resume_skills.items()
        }

        tag_style = """
        <style>
            .tag-container {
                display: flex;
                flex-wrap: wrap;
                gap: 6px;
                margin-bottom: 1em;
            }
            .tag {
                border-radius: 12px;
                padding: 4px 10px;
                font-size: 14px;
                display: inline-block;
            }
            .tag.match { background-color: #d4edda; }
            .tag.missing { background-color: #f8d7da; }
        </style>
        """
        st.markdown(tag_style, unsafe_allow_html=True)

        show_matching = st.checkbox("Show Matching Skills", value=True, key="match_toggle")
        show_missing = st.checkbox("Show Missing Skills", value=True, key="miss_toggle")

        columns = st.columns(2)
        with columns[0]:
            st.subheader("📄 Resume Skills")
            for cat, skills in resume_skills.items():
                st.markdown(f"**{cat.title()}**")
                tags = []
                for skill in skills:
                    if skill in jd_skills.get(cat, []):
                        if show_matching:
                            tags.append(f"<span class='tag match'>{skill}</span>")
                    else:
                        if show_missing:
                            tags.append(f"<span class='tag missing'>{skill}</span>")
                if tags:
                    st.markdown("<div class='tag-container'>" + "".join(tags) + "</div>", unsafe_allow_html=True)

        with columns[1]:
            st.subheader("📋 JD Skills")
            for cat, skills in jd_skills.items():
                st.markdown(f"**{cat.title()}**")
                tags = []
                for skill in skills:
                    if skill in resume_skills.get(cat, []) and show_matching:
                        tags.append(f"<span class='tag match'>{skill}</span>")
                    elif skill not in resume_skills.get(cat, []) and show_missing:
                        tags.append(f"<span class='tag missing'>{skill}</span>")
                if tags:
                    st.markdown("<div class='tag-container'>" + "".join(tags) + "</div>", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("### 📄 Highlighted Job Description")
        all_jd_skills = set()
        for skills in jd_skills.values():
            all_jd_skills.update(skills)

        def highlight_skills_in_text(text, resume_skills_set, jd_skills_set):
            resume_skills_set = {s.lower() for s in resume_skills_set}
            jd_skills_set = {s.lower() for s in jd_skills_set}
            all_skills = sorted(jd_skills_set.union(resume_skills_set), key=len, reverse=True)

            def escape_phrase(s):
                return r'\b' + r'\s+'.join(re.escape(w) for w in s.split()) + r'\b'

            for skill in all_skills:
                pattern = re.compile(escape_phrase(skill), re.IGNORECASE)
                if skill in resume_skills_set:
                    text = pattern.sub(lambda m: f"<span style='background-color: #d4edda; color: black;'>{m.group(0)}</span>", text)
                elif skill in jd_skills_set:
                    text = pattern.sub(lambda m: f"<span style='background-color: #f8d7da; color: black;'>{m.group(0)}</span>", text)
            return text

        highlighted_jd = highlight_skills_in_text(jd_input, set().union(*resume_skills.values()), all_jd_skills)
        st.markdown("""
            <div style='line-height: 1.6; white-space: pre-wrap;'>
        """ + highlighted_jd + "</div>", unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("### 🧼 Missing Keywords")
        st.write(result['missing_keywords'])

elif resume_file or jd_input:
    st.info("Click the Analyze button to process your inputs.")