#!/bin/bash

# CryptoQ Sentiment Analyzer - Deployment Script
# This script helps prepare and deploy the application to Render

echo "🚀 CryptoQ Sentiment Analyzer - Deployment Preparation"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: manage.py not found. Please run this script from the CryptoQWeb directory."
    exit 1
fi

echo "✅ Found Django project"

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional)
echo "👤 Creating superuser (optional)..."
echo "You can skip this by pressing Ctrl+C"
python manage.py createsuperuser

echo "✅ Deployment preparation complete!"
echo ""
echo "Next steps:"
echo "1. Push your code to GitHub"
echo "2. Connect to Render.com"
echo "3. Deploy using the render.yaml configuration"
echo ""
echo "📖 See DEPLOYMENT.md for detailed instructions"
