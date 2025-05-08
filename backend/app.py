from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import PyPDF2
import docx
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import shutil
from datetime import datetime
from config import Config

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": Config.CORS_ORIGINS}})
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_FILE_SIZE

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def clean_text(text):
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def calculate_keyword_score(text):
    # Define important keywords for different sections
    keywords = {
        'skills': ['python', 'java', 'javascript', 'sql', 'machine learning', 'data analysis'],
        'experience': ['experience', 'worked', 'developed', 'implemented', 'managed'],
        'education': ['education', 'degree', 'university', 'college', 'bachelor', 'master'],
        'achievements': ['achievement', 'award', 'certification', 'recognition']
    }
    
    text = text.lower()
    scores = {}
    for category, words in keywords.items():
        scores[category] = sum(1 for word in words if word in text)
    
    return scores

def score_resume(text):
    # Clean the text
    text = clean_text(text)
    
    # Calculate basic metrics
    word_count = len(text.split())
    keyword_scores = calculate_keyword_score(text)
    
    # Calculate section scores
    section_scores = {
        'length': min(word_count / 100, 3.0),  # Max 3 points for length
        'skills': min(keyword_scores['skills'] * 0.5, 2.0),  # Max 2 points for skills
        'experience': min(keyword_scores['experience'] * 0.5, 2.0),  # Max 2 points for experience
        'education': min(keyword_scores['education'] * 0.5, 1.5),  # Max 1.5 points for education
        'achievements': min(keyword_scores['achievements'] * 0.5, 1.5)  # Max 1.5 points for achievements
    }
    
    total_score = sum(section_scores.values())
    return {
        'total_score': round(total_score, 2),
        'section_scores': section_scores
    }

def extract_text_from_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.txt':
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    elif ext == '.pdf':
        text = ''
        with open(filepath, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ''
        return text
    elif ext == '.docx':
        doc = docx.Document(filepath)
        return '\n'.join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type")

def cleanup_old_files():
    # Clean up files older than 1 hour
    now = datetime.now()
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(filepath):
            file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            if (now - file_time).total_seconds() > 3600:  # 1 hour
                os.remove(filepath)

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Please upload {", ".join(Config.ALLOWED_EXTENSIONS)} files.'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(filepath)
        text = extract_text_from_file(filepath)
        score_result = score_resume(text)
        cleanup_old_files()  # Clean up old files after successful processing
        return jsonify(score_result)
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
