import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    if not text:
        return ""
    
    # Remove emails, urls, non-alphanumeric chars
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    
    # Tokenization, Lemmatization, Stopword removal
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_space]
    
    return " ".join(tokens)

def calculate_similarity(job_desc, resumes):
    """
    job_desc: str
    resumes: list of dicts [{'id': 1, 'text': '...'}]
    returns: list of dicts with 'score' added
    """
    if not resumes or not job_desc:
        for r in resumes:
            r['score'] = 0.0
        return resumes
    
    # Preprocess texts
    processed_jd = preprocess_text(job_desc)
    processed_resumes = [preprocess_text(r['text']) for r in resumes]
    
    # TF-IDF
    vectorizer = TfidfVectorizer()
    all_texts = [processed_jd] + processed_resumes
    
    try:
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        # Cosine similarity of jd with all resumes
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        
        for i, r in enumerate(resumes):
            r['score'] = round(float(cosine_sim[i]) * 100, 2)
    except ValueError:
        # In case all texts are empty
        for r in resumes:
            r['score'] = 0.0
            
    # Sort by score descending
    resumes.sort(key=lambda x: x['score'], reverse=True)
    
    # Assign rank
    for i, r in enumerate(resumes):
        r['rank'] = i + 1
        
    return resumes
