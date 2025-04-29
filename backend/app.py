from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
import PyPDF2
import docx

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def score_resume(text):
    return min(round(len(text.split()) / 10, 2), 10.0)

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

@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['resume']
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        text = extract_text_from_file(filepath)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    score = score_resume(text)
    return jsonify({'score': score})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
