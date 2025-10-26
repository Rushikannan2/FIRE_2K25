# CryptoQ Sentiment Analyzer

A Django web application for hierarchical sentiment analysis using a 3-level AI model with ensemble averaging.

## Features

- **3-Level Hierarchical Analysis**:
  - Level 1: NOISE, OBJECTIVE, SUBJECTIVE
  - Level 2: NEUTRAL, NEGATIVE, POSITIVE (only if Level 1 = SUBJECTIVE)
  - Level 3: NEUTRAL_SENTIMENT, QUESTION, ADVERTISEMENT, MISCELLANEOUS (only if Level 2 = NEUTRAL)

- **Ensemble Averaging**: Uses 5-fold ensemble models for each level
- **Web Interface**: Beautiful, responsive Django web interface
- **API Support**: RESTful API for programmatic access
- **Analysis History**: Track and view previous analyses
- **Fallback Analysis**: Rule-based analysis when models are unavailable

## Setup Instructions

### 1. Install Dependencies

```bash
# Activate your virtual environment
# Windows:
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser
```

### 3. Model Files

Place your pre-trained model files in the `models/` directory:

```
models/
├── level1_fold1.pth
├── level1_fold2.pth
├── level1_fold3.pth
├── level1_fold4.pth
├── level1_fold5.pth
├── level2_fold1.pth
├── level2_fold2.pth
├── level2_fold3.pth
├── level2_fold4.pth
├── level2_fold5.pth
├── level3_fold1.pth
├── level3_fold2.pth
├── level3_fold3.pth
├── level3_fold4.pth
└── level3_fold5.pth
```

### 4. Run the Application

```bash
# Start the development server
python manage.py runserver

# The application will be available at http://127.0.0.1:8000/
```

### 5. Test the System

```bash
# Test with sample text
python manage.py test_sentiment --text "This is amazing! I love this cryptocurrency."

# Test with different models directory
python manage.py test_sentiment --text "What is Bitcoin?" --models-dir "path/to/models"
```

## Usage

### Web Interface

1. Navigate to `http://127.0.0.1:8000/`
2. Enter any text in the text area
3. Click "Analyze Sentiment"
4. View the hierarchical classification results

### API Usage

```python
import requests

# Analyze sentiment via API
response = requests.post('http://127.0.0.1:8000/api/analyze/', 
                        json={'text': 'This is great!'})
result = response.json()
print(result['classification'])
```

### Example Classifications

- **"Bitcoin is amazing!"** → `SUBJECTIVE → POSITIVE`
- **"What is cryptocurrency?"** → `SUBJECTIVE → NEUTRAL → QUESTION`
- **"The price is $50,000"** → `OBJECTIVE`
- **"Buy now! Limited offer!"** → `SUBJECTIVE → NEUTRAL → ADVERTISEMENT`
- **""** → `NOISE`

## Project Structure

```
CryptoQWeb/
├── sentiment/
│   ├── models.py          # Django models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin interface
│   ├── ai_analyzer.py     # Core AI logic
│   └── templates/
│       └── sentiment/
│           ├── base.html
│           ├── home.html
│           ├── history.html
│           └── detail.html
├── models/                # Pre-trained model files
├── requirements.txt       # Python dependencies
└── manage.py             # Django management script
```

## Configuration

### Model Paths

Update the model paths in `sentiment/views.py` if your models are in a different location:

```python
analyzer = SentimentAnalyzer(models_dir="path/to/your/models")
```

### Database

The application uses SQLite by default. To use a different database, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Troubleshooting

### Models Not Found

If the models are not found, the system will automatically fall back to rule-based analysis. Check:

1. Model files are in the correct directory
2. File names match the expected pattern
3. Files are not corrupted

### Performance Issues

For production deployment:

1. Use a production WSGI server (e.g., Gunicorn)
2. Configure proper database settings
3. Set up static file serving
4. Consider model caching for better performance

## License

This project is part of the CryptoQ sentiment analysis system.
