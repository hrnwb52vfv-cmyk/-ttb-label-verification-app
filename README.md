# AI-Powered Alcohol Label Verification App

A Flask prototype that helps alcohol label compliance agents verify whether label artwork matches submitted application information.

The app extracts text from uploaded label images using OCR, compares the text against expected application fields, and displays a simple review checklist for agents.

## Features

- Upload alcohol label image files
- Extract text from the label using OCR
- Compare label text against application fields
- Check brand name, class/type, alcohol content, net contents, and government warning
- Use fuzzy matching for reasonable capitalization and punctuation differences
- Use stricter checking for government warning language
- Simple, clean interface for non-technical users
- Docker support for easier setup
- Unit tests for validation logic

## Technology Used

- Python
- Flask
- pytesseract OCR
- Pillow
- RapidFuzz
- Docker
- Pytest

## Project Structure

```text
ttb-label-verification-app/
├── app.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── .gitignore
├── services/
│   ├── __init__.py
│   ├── ocr_service.py
│   ├── validation_service.py
│   └── warning_checker.py
├── templates/
│   ├── index.html
│   └── results.html
├── static/
│   ├── css/style.css
│   └── js/app.js
├── uploads/.gitkeep
├── sample_labels/README.md
└── tests/
    ├── test_validation.py
    └── test_warning.py
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ttb-label-verification-app.git
cd ttb-label-verification-app
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Tesseract OCR

This app uses `pytesseract`, which requires the Tesseract OCR engine.

Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr
```

Mac:

```bash
brew install tesseract
```

Windows:

Install Tesseract from the official installer and ensure it is added to your PATH.

### 6. Run the app

```bash
python app.py
```

Open your browser to:

```text
http://localhost:5000
```

## Docker Setup

Build and run with Docker:

```bash
docker build -t ttb-label-verification-app .
docker run -p 5000:5000 ttb-label-verification-app
```

Or use Docker Compose:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:5000
```

## How to Use

1. Upload a label image.
2. Enter the application information:
   - Brand name
   - Class/type
   - Alcohol content
   - Net contents
3. Click **Verify Label**.
4. Review the results checklist.

## Validation Approach

The app uses OCR to extract text from the uploaded label image. It then normalizes the text and compares it against expected application fields.

- Brand name and class/type use fuzzy matching to allow minor differences such as capitalization or punctuation.
- Alcohol content and net contents use normalized text matching.
- Government warning is checked strictly because the warning statement must meet regulatory requirements.

## Assumptions

- This is a standalone proof-of-concept and does not integrate with COLA.
- Uploaded files are processed locally and are not intended for long-term storage.
- The prototype focuses on common distilled spirits label checks.
- Final approval or rejection should still be made by a trained compliance agent.

## Trade-Offs and Limitations

- OCR quality depends on the quality of the uploaded image.
- Angled images, glare, low lighting, or blurry labels may reduce accuracy.
- Batch upload is not included in this prototype but is a recommended future improvement.
- The app does not perform full beverage-type-specific regulatory review.

## Future Improvements

- Batch upload processing for large importer submissions
- Image preprocessing for glare, rotation, and low-light correction
- Beverage-specific validation rules for beer, wine, and distilled spirits
- Confidence scoring for each field
- Exportable PDF or CSV review reports
- Authentication and role-based access for production use
- Future integration path with COLA or other government systems

## Running Tests

```bash
pytest
```

## Submission Notes

This prototype was designed to demonstrate practical engineering judgment, clean organization, usability, and attention to stakeholder requirements. It prioritizes a working core workflow over unnecessary complexity.
