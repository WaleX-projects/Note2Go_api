# Note2Go_api

Note2Go Backend is a Django REST API that powers the Note2Go mobile app.  
It handles OCR note processing, PDF generation, AI-powered study tools, and secure authentication.

---

## Features

- JWT Authentication (Login & Register)
- Upload notebook images
- OCR text extraction
- Edit & save OCR text
- Generate clean PDFs
- AI-powered:
  - Text cleaning & formatting
  - Subject detection
  - Summaries
  - Flashcards
- Search notes by text
- Filter notes by subject

---

## AI Integration

- Google Gemini API
- Used for:
  - Formatting OCR text
  - Detecting subject
  - Generating summaries & flashcards

---

## Tech Stack

- Python 3.9+
- Django
- Django REST Framework
- SimpleJWT
- Tesseract OCR
- Google Gemini API
- SQLite / PostgreSQL
- Pillow (Image processing)
- ReportLab (PDF generation)

---

## 📦 API Endpoints

### Auth
POST /api/auth/login/
POST /api/auth/register/

### Notes
GET /api/notes/
POST /api/notes/
GET /api/notes/?search=
GET /api/notes/?subject=

### AI Actions
POST /api/notes/{id}/ai_format/
POST /api/notes/{id}/detect_subject/
POST /api/notes/{id}/generate_study/


### PDF
GET /media/pdfs/{file}.pdf



---

## Setup Instructions

### Clone Repository
```bash
git clone https://github.com/yourusername/note2go-backend.git
cd note2go_ai

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
### Set Enviromental variables
```bash
SECRET_KEY=your-secret-key
DEBUG=True
GEMINI_API_KEY=your-gemini-key
ALLOWED_HOSTS=your_allowed_host
AI_MODEL=gemini_ai_model
```
### Project Status

Core features complete
Future improvements:
 -Background tasks (Celery)
 -PDF themes
 -Multi-language OCR (--d)
 -AI caching


### Author
 -Built for students, by students.
 -Designed to make studying smarter and faster.