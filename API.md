# ResumeRanker API Documentation

## Base URL
```
https://resumeranker-89kg.onrender.com
```

## Endpoints

### Upload Resume
Upload a resume file for analysis and scoring.

**URL:** `/upload`

**Method:** `POST`

**Content-Type:** `multipart/form-data`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| resume | File | The resume file to analyze (supported formats: .txt, .pdf, .docx) |

**Success Response:**
```json
{
    "total_score": 7.5,
    "section_scores": {
        "length": 2.5,
        "skills": 2.0,
        "experience": 1.5,
        "education": 1.0,
        "achievements": 0.5
    }
}
```

**Error Responses:**
```json
{
    "error": "No file uploaded"
}
```
Status: 400

```json
{
    "error": "No file selected"
}
```
Status: 400

```json
{
    "error": "File type not allowed. Please upload .txt, .pdf, or .docx files."
}
```
Status: 400

```json
{
    "error": "Error message"
}
```
Status: 500

## Scoring System

The resume scoring system evaluates resumes based on several criteria:

1. **Length (0-3 points)**
   - Based on word count
   - Maximum 3 points for optimal length

2. **Skills (0-2 points)**
   - Presence of technical skills
   - Maximum 2 points for comprehensive skill set

3. **Experience (0-2 points)**
   - Work experience descriptions
   - Maximum 2 points for detailed experience

4. **Education (0-1.5 points)**
   - Educational background
   - Maximum 1.5 points for relevant education

5. **Achievements (0-1.5 points)**
   - Professional achievements and awards
   - Maximum 1.5 points for significant achievements

**Total Score Range:** 0-10 points

## Rate Limiting
- Maximum file size: 5MB
- Supported file types: .txt, .pdf, .docx

## CORS
The API supports CORS for the following origins:
- http://localhost:3000
- https://resumeranker7.netlify.app

## Error Handling
All error responses include a JSON object with an "error" field containing a descriptive message. 