#!/bin/bash
# Build script for Render deployment
set -e

echo "🚀 Starting CryptoQ build process..."

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --no-cache-dir --upgrade pip

# Install requirements
echo "📦 Installing requirements..."
pip install --no-cache-dir -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Download models
echo "🤖 Downloading models..."
python download_models_optimized.py

echo "✅ Build completed successfully!"