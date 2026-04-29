# 🧠 How It Works: Smart Resume Screening System

This document explains the inner workings of the Smart Resume Screening System and provides a step-by-step guide on how to prepare and deploy it for public use.

---

## ⚙️ Part 1: How the System Works

The application follows a standard AI/ML pipeline for text processing and matching. Here is the step-by-step lifecycle of a request:

### 1. Data Ingestion (Frontend -> Backend)
- **User Action:** You upload resumes (PDF/DOCX) and paste a Job Description on the frontend interface.
- **Transport:** The frontend sends these files to the FastAPI backend via a `multipart/form-data` POST request.
- **Temporary Storage:** The backend temporarily saves the uploaded files into the `uploads/` folder to process them.

### 2. Text Extraction (`parser.py`)
- The system determines the file type (.pdf or .docx).
- **PDFs:** Uses `PyPDF2` to read page by page and extract raw text.
- **DOCX:** Uses `python-docx` to read paragraphs and extract raw text.

### 3. NLP Preprocessing (`model.py`)
Raw text is messy. It contains stop words ("and", "the", "is"), punctuation, and formatting inconsistencies.
- **Cleaning:** We use Regular Expressions (`re`) to remove emails, URLs, and non-alphanumeric characters. We also convert everything to lowercase.
- **spaCy Processing:** 
  - **Tokenization:** Splits the text into individual words.
  - **Stopword Removal:** Removes common but uninformative words.
  - **Lemmatization:** Converts words to their base form (e.g., "running" becomes "run", "better" becomes "good"). This ensures that variations of a skill match properly.

### 4. Feature Extraction & Matching (`model.py`)
Computers don't understand words; they understand numbers.
- **TF-IDF (Term Frequency - Inverse Document Frequency):** This algorithm assigns a mathematical weight to each word.
  - *Term Frequency:* How often a word appears in a resume.
  - *Inverse Document Frequency:* Decreases the weight of words that appear in *every* resume (like "teamwork") and increases the weight of rare, specific words (like "FastAPI" or "Kubernetes").
- **Cosine Similarity:** Once the Job Description and Resumes are converted into numerical vectors (arrays of numbers), we calculate the "angle" between them. 
  - A score of `1.0` (100%) means they point in the exact same direction (perfect match).
  - A score of `0.0` (0%) means they have nothing in common.

### 5. Storage & Display (`utils.py` & `script.js`)
- **Database:** The parsed text and scores are logged into a local `SQLite` database (`database/resume_screening.db`) for record-keeping.
- **Response:** The backend sorts the resumes by score descending, assigns a rank, and sends the JSON payload back to the frontend.
- **UI Render:** JavaScript reads the JSON and dynamically generates the HTML table to display the Top Candidates.

---

## 🌍 Part 2: How to Make it for Public Use (Deployment)

If you want to share this tool with the public, you need to move it from your local machine (`localhost`) to the cloud. Here is the roadmap:

### Step 1: Prepare the Code for Production
Before deploying, make the following changes to ensure security and scalability:

1. **Update CORS:** In `backend/app.py`, change `allow_origins=["*"]` to your actual frontend domain (e.g., `["https://my-resume-app.vercel.app"]`). This prevents unauthorized websites from calling your API.
2. **Change the Database:** SQLite is great for local testing but locks the file during writes. For public use, migrate to a production database like **PostgreSQL**.
3. **Add File Limits:** Prevent malicious users from uploading 1GB PDFs. You can enforce file size limits natively in FastAPI.
4. **Auto-Cleanup:** Ensure the `uploads/` folder is cleared automatically after processing so your server's disk space doesn't fill up.

### Step 2: Host the Backend (API)
The backend needs a server that supports Python. Good options are **Render**, **Railway**, or **AWS/DigitalOcean**.

**Recommended: Deploying on Render (Free/Low Cost)**
1. Create a `requirements.txt` (Already done!).
2. Push your entire `backend` folder to a GitHub repository.
3. Go to [Render.com](https://render.com), create a new **Web Service**, and connect your GitHub repo.
4. **Build Command:** `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
5. **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Render will provision a server and give you a public URL like `https://smart-resume-api.onrender.com`.

### Step 3: Host the Frontend (UI)
The frontend consists of static files (HTML, CSS, JS). This is incredibly easy and usually free to host.

**Recommended: Deploying on Vercel or Netlify**
1. In `frontend/script.js`, change the API endpoint on line 33:
   *From:* `const response = await fetch('http://localhost:8000/api/screen', ...)`
   *To:* `const response = await fetch('https://smart-resume-api.onrender.com/api/screen', ...)` *(Replace with your actual backend URL from Step 2)*.
2. Go to [Vercel](https://vercel.com) or [Netlify](https://netlify.com).
3. Drag and drop your `frontend` folder into their deployment page.
4. You will instantly get a public URL (e.g., `https://smart-resume-scanner.vercel.app`).

### Step 4: Add Production Features (Optional but Recommended)
Once public, consider adding:
- **Authentication:** Add user login via Auth0, Firebase, or Clerk so only authorized recruiters can upload resumes.
- **Advanced NLP:** Swap out TF-IDF for HuggingFace `sentence-transformers` (e.g., `all-MiniLM-L6-v2`) for significantly better, context-aware semantic matching.
- **Cloud Storage:** Instead of saving files to the local `uploads/` folder, stream them directly to AWS S3.
