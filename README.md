# 📄 Resume Matcher App

A smart resume-job description matcher built using NLP techniques to help job seekers tailor their resumes for specific job postings. 
This project is transitioning into a full-featured, scalable web platform.

---

## 🚀 Features (Current)
- Upload one or more resumes
- Paste or fetch job descriptions (LinkedIn, Indeed, Lever)
- NLP-based keyword and skill matching
- Match scoring by keyword and skill category
- Highlighted JD view with skill matches
- Multi-resume comparison and ranking

---

## 🛠️ Tech Stack (Current)
- **Frontend**: Streamlit
- **NLP**: Python, spaCy
- **Backend Logic**: Python functions for parsing, scoring, and highlighting
- **PDF Parsing**: PyMuPDF
- **Job Scraping**: Selenium + BeautifulSoup (headless Chrome)

---

## 🔮 Future Plans

### ✅ Phase 1: Backend API
- Scaffold a **FastAPI** backend
- Expose APIs for:
  - Resume upload
  - JD parsing
  - Match scoring
  - User management (login, register)

### 🔐 Phase 2: User Authentication
- JWT based auth system
- Store resumes, jobs, and user profile data
- Secure file storage

### 💾 Phase 3: Persistent Database
- PostgreSQL or SQLite
- ORM: SQLAlchemy or Tortoise
- Models:
  - User
  - Resume
  - JobDescription
  - OptimizedResume

### 🧠 Phase 4: Resume Optimizer Engine
- Input: Skills, Experience, Target Role
- Output: Suggested or AI augmented resume variant
- Rule based & GPT assisted versions

### 🌐 Phase 5: Full Web Application
- Frontend: React or Next.js
- Responsive UI for editing, scoring, and exporting resumes
- Multilanguage support
- ATS score simulation + PDF resume export

### 💰 Optional Premium Features (Commercialization)
- Resume versioning
- AI Resume Assistant (Chat-style)
- PDF styling templates
- Stripe integration for paid tiers

---

## 📁 Project Structure
```
.
├── app.py                  # Streamlit frontend entry
├── run_app.py              # CLI launcher that auto-manages venv + deps
├── matcher/                # Keyword matching and skill parsing logic
├── requirements.txt
├── README.md
└── backend/                # (Planned) FastAPI backend modules
```