import pytest
import os
import json
from app import app, allowed_file, score_resume, extract_text_from_file

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_allowed_file():
    assert allowed_file('test.pdf') == True
    assert allowed_file('test.txt') == True
    assert allowed_file('test.docx') == True
    assert allowed_file('test.exe') == False
    assert allowed_file('test') == False

def test_score_resume():
    # Test with a sample resume text
    text = """
    John Doe
    Software Engineer
    
    Skills:
    - Python
    - JavaScript
    - SQL
    
    Experience:
    - Worked at Company A
    - Developed web applications
    
    Education:
    - Bachelor's in Computer Science
    
    Achievements:
    - Won coding competition
    """
    
    result = score_resume(text)
    assert 'total_score' in result
    assert 'section_scores' in result
    assert isinstance(result['total_score'], float)
    assert isinstance(result['section_scores'], dict)

def test_upload_endpoint_no_file(client):
    response = client.post('/upload')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_upload_endpoint_invalid_file_type(client):
    data = {
        'resume': (b'fake content', 'test.exe')
    }
    response = client.post('/upload', data=data)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_cleanup_old_files():
    # This test would need to be implemented with proper file creation and cleanup
    pass 