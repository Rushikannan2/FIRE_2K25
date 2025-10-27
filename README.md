# CryptoQ Sentiment Analyzer

A Django-based web application for hierarchical sentiment analysis of cryptocurrency-related social media content, featuring a 3-level classification system and interactive visualizations.

## 🎯 Features

- **3-Level Hierarchical Classification**
  - Level 1: NOISE, OBJECTIVE, SUBJECTIVE
  - Level 2: NEUTRAL, NEGATIVE, POSITIVE (for Subjective)
  - Level 3: NEUTRAL_SENTIMENT, QUESTION, ADVERTISEMENT, MISCELLANEOUS (for Neutral)

- **Interactive Visualizations**
  - Token Importance Heatmap
  - Sentiment-Weighted Word Cloud
  - Decision Flow Diagram

- **Real-time Analysis**
  - Instant sentiment analysis
  - Confidence scoring
  - Historical analysis tracking

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/CryptoQ-Sentiment-Analyzer.git
   cd CryptoQ-Sentiment-Analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   Open your browser to `http://localhost:8000`

## 🧠 Dataset Information

### Level 1 (3 classes)
- 0 → NOISE
- 1 → OBJECTIVE  
- 2 → SUBJECTIVE

### Level 2 (for SUBJECTIVE class only)
- 0 → NEUTRAL
- 1 → NEGATIVE
- 2 → POSITIVE

### Level 3 (for NEUTRAL subclass only)
- 0 → NEUTRAL_SENTIMENTS
- 1 → QUESTIONS
- 2 → ADVERTISEMENTS
- 3 → MISCELLANEOUS

## 🎨 Color Scheme

- **Noise**: #E74C3C (Red)
- **Objective**: #1ABC9C (Teal)
- **Positive**: #27AE60 (Green)
- **Negative**: #F1C40F (Yellow)
- **Neutral Sentiment**: #95A5A6 (Gray)
- **Question**: #3498DB (Blue)
- **Ads**: #2C3E50 (Dark Blue)
- **Miscellaneous**: #7F8C8D (Gray)

## 📁 Project Structure

```
CryptoQ-Sentiment-Analyzer/
├── CryptoQWeb/
│   ├── CryptoQWeb/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── sentiment/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templates/
│   │       └── sentiment/
│   ├── assets/
│   │   ├── FIRE.jpg
│   │   ├── CryptoQ.jpeg
│   │   └── IIITKottayam_Summer_Internship.jpg
│   ├── models/
│   │   └── *.pth (trained model files)
│   ├── manage.py
│   └── requirements.txt
├── README.md
└── render.yaml
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-render-app.onrender.com,localhost
```

### Settings

Key settings in `CryptoQWeb/settings.py`:
- Static files configuration
- Database settings
- Security settings for production

## 🚀 Deployment

### Render Deployment

1. **Connect to GitHub**
   - Push your code to GitHub
   - Connect your GitHub repository to Render

2. **Create Web Service**
   - Choose "Web Service" on Render
   - Connect your GitHub repository
   - Use the following settings:
     - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
     - **Start Command**: `python manage.py runserver 0.0.0.0:$PORT`
     - **Python Version**: 3.11

3. **Environment Variables**
   Set these in Render dashboard:
   ```
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=your-app-name.onrender.com
   ```

## 📊 Model Files

The application uses pre-trained PyTorch models stored in the `models/` directory:
- `level1_fold1.pth` through `level1_fold5.pth`
- `level2_fold1.pth` through `level2_fold5.pth`
- `level3_fold1.pth` through `level3_fold5.pth`

## 🛠️ Development

### Adding New Features

1. **Models**: Add new models in `sentiment/models.py`
2. **Views**: Add new views in `sentiment/views.py`
3. **Templates**: Add new templates in `sentiment/templates/sentiment/`
4. **URLs**: Update URL patterns in `sentiment/urls.py`

### Testing

```bash
python manage.py test
```

## 📝 API Endpoints

- `GET /` - Home page with analysis form
- `POST /analyze/` - Submit text for analysis
- `GET /detail/<id>/` - View detailed analysis results
- `GET /history/` - View analysis history
- `GET /about-author/` - About the author page
- `GET /about-us/` - About the CryptoQ track page

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is part of the CryptoQ Sentiment Analysis system for FIRE 2025.

## 🙏 Acknowledgments

- **FIRE 2025 Conference** - Forum for Information Retrieval Evaluation
- **IIIT Kottayam** - Summer Research Internship Program
- **VT RushiKannan** - Research Intern

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Contact: [Your Email]

---

**Built with ❤️ for the CryptoQ Sentiment Analysis project**