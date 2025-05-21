import spacy
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

nlp = spacy.load("en_core_web_sm")

# Basic NLP pipeline for keyword matching
def match_keywords(resume_text, jd_text):
    vectorizer = CountVectorizer(stop_words='english')
    docs = [resume_text, jd_text]
    X = vectorizer.fit_transform(docs)
    resume_vec, jd_vec = X.toarray()
    
    overlap = np.minimum(resume_vec, jd_vec).sum()
    total = jd_vec.sum()
    
    jd_keywords = set(vectorizer.get_feature_names_out())
    resume_keywords = set(resume_text.lower().split())
    missing_keywords = list(jd_keywords - resume_keywords)

    return {
        "score": round((overlap / total) * 100, 2),
        "missing_keywords": missing_keywords[:20]
    }