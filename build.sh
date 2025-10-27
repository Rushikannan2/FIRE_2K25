#!/bin/bash
# Build script for Render deployment
# This script downloads models and installs dependencies

echo "Starting CryptoQ build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Download model files
echo "Downloading model files..."
python download_models.py

# Verify models were downloaded
echo "Verifying model downloads..."
if [ -d "models" ]; then
    echo "Models directory created successfully"
    ls -la models/
else
    echo "ERROR: Models directory not found"
    exit 1
fi

echo "Build completed successfully!"
