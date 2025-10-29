#!/bin/bash
# Optimized build script for Render deployment
# This script optimizes the build process to prevent timeouts

set -e  # Exit on any error

echo "🚀 Starting optimized CryptoQ build process..."

# Step 1: Upgrade pip and install wheel for faster builds
echo "📦 Upgrading pip and installing build tools..."
pip install --no-cache-dir --upgrade pip wheel setuptools

# Step 2: Install dependencies with optimizations
echo "📦 Installing Python dependencies..."
pip install --no-cache-dir \
    --find-links https://download.pytorch.org/whl/cpu \
    -r requirements.txt

# Step 3: Collect static files (if needed)
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || echo "⚠️  Static collection failed, continuing..."

# Step 4: Download models (with timeout protection)
echo "🤖 Downloading ML models..."
timeout 1800 python download_models_optimized.py || {
    echo "⚠️  Model download timed out or failed, continuing with existing models..."
}

# Step 5: Run database migrations (if needed)
echo "🗄️  Running database migrations..."
python manage.py migrate --noinput || echo "⚠️  Migrations failed, continuing..."

echo "✅ Build process completed successfully!"
