# CryptoQ Sentiment Analyzer - Deployment Guide

## 🚀 Deploy to Render.com

Follow these steps to deploy your CryptoQ Sentiment Analyzer to Render:

### Step 1: Prepare Your Repository

1. **Initialize Git** (if not already done):
   ```bash
   cd C:\Users\hp\Desktop\CryptoQ
   git init
   ```

2. **Add all files**:
   ```bash
   git add .
   ```

3. **Create initial commit**:
   ```bash
   git commit -m "Initial commit: CryptoQ Sentiment Analyzer"
   ```

### Step 2: Push to GitHub

1. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Repository name: `CryptoQ-Sentiment-Analyzer`
   - Make it public
   - Don't initialize with README (we already have one)

2. **Add GitHub remote**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/CryptoQ-Sentiment-Analyzer.git
   ```

3. **Push to GitHub**:
   ```bash
   git branch -M main
   git push -u origin main
   ```

### Step 3: Deploy on Render

1. **Go to Render Dashboard**:
   - Visit https://render.com
   - Sign up/Login with GitHub

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `CryptoQ-Sentiment-Analyzer`

3. **Configure Service**:
   - **Name**: `cryptoq-sentiment-analyzer`
   - **Environment**: `Python 3`
   - **Plan**: `Free`
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command**: `python manage.py runserver 0.0.0.0:$PORT`

4. **Environment Variables**:
   ```
   DEBUG=False
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=cryptoq-sentiment-analyzer.onrender.com
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete

### Step 4: Update Django Settings

Make sure your `CryptoQWeb/settings.py` has these production settings:

```python
import os
from decouple import config

# Security settings
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / 'assets',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Database (Render provides DATABASE_URL)
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3'
    )
}

# Static files serving
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Step 5: Test Your Deployment

1. **Visit your app**: `https://cryptoq-sentiment-analyzer.onrender.com`
2. **Test functionality**:
   - Home page loads
   - Analysis form works
   - Visualizations display
   - About pages accessible

### Troubleshooting

**Common Issues:**

1. **Static files not loading**:
   - Add `whitenoise` to MIDDLEWARE
   - Run `python manage.py collectstatic`

2. **Database errors**:
   - Check DATABASE_URL environment variable
   - Run migrations: `python manage.py migrate`

3. **Model files not found**:
   - Ensure model files are in the repository
   - Check file paths in your code

4. **Build failures**:
   - Check requirements.txt
   - Verify Python version compatibility

### Environment Variables for Production

Set these in Render dashboard:

```
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=cryptoq-sentiment-analyzer.onrender.com
DATABASE_URL=postgresql://... (auto-provided by Render)
```

### Custom Domain (Optional)

1. **Add custom domain** in Render dashboard
2. **Update ALLOWED_HOSTS** environment variable
3. **Configure DNS** to point to Render

### Monitoring

- **Logs**: Available in Render dashboard
- **Metrics**: CPU, Memory usage
- **Uptime**: Service availability

## 🎉 Success!

Your CryptoQ Sentiment Analyzer is now live on Render!

**Live URL**: `https://cryptoq-sentiment-analyzer.onrender.com`

## 📝 Next Steps

1. **Test all features** thoroughly
2. **Monitor performance** and logs
3. **Set up custom domain** if needed
4. **Configure backups** for production data
5. **Add monitoring** and alerts

## 🔧 Maintenance

- **Regular updates**: Keep dependencies updated
- **Security patches**: Monitor for Django/Python updates
- **Performance**: Monitor resource usage
- **Backups**: Regular database backups

---

**Happy Deploying! 🚀**
