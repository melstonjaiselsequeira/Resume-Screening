# Smart Resume Screening System

A complete, production-ready AI/ML system to screen and rank candidate resumes against a Job Description using Natural Language Processing (NLP).

## Features
- **Resume Upload System**: Supports multiple PDF and DOCX files.
- **NLP Preprocessing**: Tokenization, Lemmatization, and Stopword removal via spaCy.
- **Feature Extraction & Matching**: TF-IDF and Cosine Similarity.
- **Automated Ranking**: Generates match scores (%) and ranks candidates.
- **Data Persistence**: Uses SQLite to log processed resumes and job descriptions.
- **Modern UI**: Clean, responsive frontend interface.

## Tech Stack
- **Backend**: Python, FastAPI
- **Frontend**: HTML, CSS, Vanilla JS
- **NLP & ML**: spaCy, scikit-learn
- **Parsing**: PyPDF2, python-docx
- **Database**: SQLite

---

## 🚀 Setup Instructions

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Clone/Setup the Project
Navigate to the project root folder (`resume-screening/`).

### 3. Backend Setup
Open a terminal in the project root and run the following commands:

#### Create a virtual environment (Optional but recommended)
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux
```

#### Install dependencies
Navigate to the backend directory:
```bash
cd backend
pip install -r requirements.txt
```

#### Download the spaCy English language model
```bash
python -m spacy download en_core_web_sm
```

#### Run the server
```bash
python app.py
```
*The FastAPI backend will start running at `http://localhost:8000`.*

### 4. Frontend Setup
The frontend consists of static files. You can simply open `frontend/index.html` in any web browser.
Alternatively, you can serve it using Python's built-in HTTP server:
```bash
cd ../frontend
python -m http.server 5500
```
Then visit `http://localhost:5500` in your browser.

---

## 🧪 How to Test
1. Create a dummy Job Description text (e.g., "Looking for a Python Developer with React experience").
2. Create some sample PDF or DOCX resumes.
3. Open the Frontend UI (`index.html`).
4. Paste the Job Description into the text area.
5. Upload the test resumes.
6. Click "Screen Resumes". The system will process them and display a ranked list.

---

## 📊 Bonus: Upgrading and Scaling

### Accuracy Improvement Suggestions
1. **Semantic Search via Embeddings**: Instead of TF-IDF, use dense embeddings (like SentenceTransformers `all-MiniLM-L6-v2`) to capture contextual meaning better.
2. **Named Entity Recognition (NER)**: Use spaCy's NER to extract specific skills, years of experience, and education levels, weighting these entities higher in the similarity score.
3. **Synonym Handling**: TF-IDF relies on exact word matches. Incorporating a domain-specific synonym dictionary can boost recall.

### Upgrading to BERT
To switch from TF-IDF to BERT for lightweight, highly accurate embeddings:
1. `pip install sentence-transformers`
2. Update `backend/model.py`:
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('all-MiniLM-L6-v2')
   
   # Instead of TfidfVectorizer:
   jd_embedding = model.encode(processed_jd)
   resume_embeddings = model.encode(processed_resumes)
   # Then compute cosine similarity using sklearn or scipy
   ```

### Deployment Strategy
- **Backend (Render / Railway / AWS)**:
  - Dockerize the application. Write a `Dockerfile` that installs requirements and the spacy model, then runs `uvicorn app:app --host 0.0.0.0 --port $PORT`.
  - Push to GitHub and connect the repository to Render/Railway for automatic builds.
- **Frontend (Vercel / Netlify / GitHub Pages)**:
  - Since it's plain HTML/CSS/JS, drag and drop the `frontend` folder into Netlify, or deploy via Vercel. Ensure `script.js` points to your deployed backend URL instead of `localhost:8000`.
- **Database**:
  - Migrate from SQLite to PostgreSQL (e.g., Supabase or RDS) for concurrent read/write handling in production.
