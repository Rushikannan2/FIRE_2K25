#!/bin/bash
# Startup script for CryptoQ Django app on Render

echo "Starting CryptoQ Django application..."

# Change to the Django project directory
cd CryptoQWeb

# Check if manage.py exists
if [ ! -f "manage.py" ]; then
    echo "ERROR: manage.py not found in CryptoQWeb directory"
    echo "Current directory: $(pwd)"
    echo "Files in current directory:"
    ls -la
    echo "Parent directory contents:"
    ls -la ..
    exit 1
fi

# Run Django development server
echo "Starting Django server on port $PORT..."
python manage.py runserver 0.0.0.0:$PORT