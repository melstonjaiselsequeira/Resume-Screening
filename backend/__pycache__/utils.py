import sqlite3
import os

DB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database'))
DB_PATH = os.path.join(DB_DIR, 'resume_screening.db')

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            candidate_name TEXT,
            parsed_text TEXT,
            score REAL DEFAULT 0,
            rank INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    conn.close()

def save_job_description(description):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO job_descriptions (description) VALUES (?)', (description,))
    jd_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jd_id

def save_resume(filename, candidate_name, parsed_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO resumes (filename, candidate_name, parsed_text) VALUES (?, ?, ?)',
                   (filename, candidate_name, parsed_text))
    resume_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return resume_id

def update_resume_score(resume_id, score, rank):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE resumes SET score = ?, rank = ? WHERE id = ?', (score, rank, resume_id))
    conn.commit()
    conn.close()

def clear_resumes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM resumes')
    conn.commit()
    conn.close()
