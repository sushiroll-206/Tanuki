import spacy
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import json
import os

nlp = spacy.load("en_core_web_sm")

# Skill categories with representative keywords
with open(os.path.join(os.path.dirname(__file__), 'skills.json'), 'r') as f:
    SKILL_CATEGORIES = json.load(f)

CATEGORY_WEIGHTS = {
    "languages": 0.3,
    "frameworks": 0.25,
    "tools": 0.2,
    "degrees": 0.15,
    "certs": 0.1
}

# Given text, uses spacy to clean text to extract keywords
def clean_text_with_spacy(text):
    doc = nlp(text)
    return {
        token.lemma_.lower() # Lemmatize converts "running" -> "run", "developed" -> "develop"
        for token in doc
        if token.is_alpha and not token.is_stop
    }

def extract_skills(text, categories):
    text = text.lower()
    extracted = {cat: [] for cat in categories}
    for cat, terms in categories.items():
        for term in terms:
            if term in text:
                extracted[cat].append(term)
    return extracted

def category_scores(resume_skills, jd_skills):
    scores = {}
    for cat in jd_skills:
        if not jd_skills[cat]:
            scores[cat] = 0.0
            continue
        matched = set(resume_skills[cat]) & set(jd_skills[cat])
        match_pct = len(matched) / len(jd_skills[cat])
        scores[cat] = round(match_pct * 100, 2)
    return scores

def weighted_skill_score(scores):
    total_score = 0.0
    for cat, pct in scores.items():
        total_score += (pct / 100) * CATEGORY_WEIGHTS[cat]
    return round(total_score * 100, 2)

# Basic NLP pipeline for keyword matching
def match_keywords(resume_text, jd_text):
    # Keyword overlap
    vectorizer = CountVectorizer(stop_words='english')
    docs = [resume_text, jd_text]
    X = vectorizer.fit_transform(docs)
    resume_vec, jd_vec = X.toarray()
    overlap = np.minimum(resume_vec, jd_vec).sum()
    total = jd_vec.sum()
    keyword_overlap_score = round((overlap / total) * 100, 2) if total > 0 else 0.0

    # NLP cleaning for keywords
    resume_keywords = clean_text_with_spacy(resume_text)
    jd_keywords = clean_text_with_spacy(jd_text)
    missing_keywords = list(jd_keywords - resume_keywords)

    # Skill-based scoring
    resume_skills = extract_skills(resume_text, SKILL_CATEGORIES)
    jd_skills = extract_skills(jd_text, SKILL_CATEGORIES)
    per_category_scores = category_scores(resume_skills, jd_skills)
    skill_score = weighted_skill_score(per_category_scores)

    # Final weighted score
    final_score = round((keyword_overlap_score * 0.3) + (skill_score * 0.7), 2)

    # ### Output
    # print("🧠 Resume Keywords:", sorted(resume_keywords))
    # print("🧠 JD Keywords:", sorted(jd_keywords))

    # print("✅ Extracted Resume Skills:", resume_skills)
    # print("✅ Extracted JD Skills:", jd_skills)


    return {
        "score": final_score,
        "keyword_score": keyword_overlap_score,
        "skill_score": skill_score,
        "category_scores": per_category_scores,
        "missing_keywords": missing_keywords[:20],
        "missing_skills": {
            cat: list(set(jd_skills[cat]) - set(resume_skills[cat]))
            for cat in jd_skills
        }
    }