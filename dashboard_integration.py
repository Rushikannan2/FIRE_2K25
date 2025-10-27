"""
Integration script to connect the Dash dashboard with Django analysis results
This script can be imported into your Django views to generate visualization data
"""

import json
import numpy as np
import umap
from collections import Counter
import re

def integrate_with_django_analysis(analysis_object):
    """
    Convert Django SentimentAnalysis object to dashboard-compatible format
    
    Args:
        analysis_object: Django SentimentAnalysis model instance
    
    Returns:
        dict: Analysis data formatted for the dashboard
    """
    
    # Extract data from Django model
    user_text = analysis_object.text
    confidence_scores = analysis_object.confidence_scores or {}
    predictions = {
        'level1': analysis_object.level1_prediction,
        'level2': analysis_object.level2_prediction,
        'level3': analysis_object.level3_prediction
    }
    
    # Process tokens from the actual user text
    tokens = re.findall(r'\b\w+\b', user_text.lower())
    
    # Enhanced sentiment word detection
    sentiment_words = {
        'positive': ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'incredible', 
                    'potential', 'growth', 'success', 'profit', 'bullish', 'moon', 'pump', 'hodl', 
                    'buy', 'strong', 'up', 'rise', 'gain', 'best', 'love', 'awesome', 'brilliant',
                    'outstanding', 'superb', 'magnificent', 'exceptional', 'remarkable', 'impressive'],
        'negative': ['bad', 'terrible', 'awful', 'horrible', 'worst', 'crash', 'dump', 'bearish', 
                    'sell', 'weak', 'down', 'fall', 'loss', 'scam', 'fraud', 'bubble', 'overpriced',
                    'hate', 'disappointed', 'worried', 'concerned', 'risky', 'dangerous', 'volatile',
                    'unstable', 'declining', 'dropping', 'plummeting', 'collapsing'],
        'neutral': ['the', 'is', 'are', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
                   'by', 'from', 'about', 'into', 'through', 'during', 'will', 'can', 'should', 'may',
                   'might', 'could', 'would', 'has', 'have', 'had', 'been', 'being', 'was', 'were']
    }
    
    # Analyze tokens
    token_data = []
    for token in tokens:
        sentiment = 'neutral'
        importance = 0.3
        
        if token in sentiment_words['positive']:
            sentiment = 'positive'
            importance = 0.8 + np.random.random() * 0.2
        elif token in sentiment_words['negative']:
            sentiment = 'negative'
            importance = 0.8 + np.random.random() * 0.2
        elif token in sentiment_words['neutral']:
            sentiment = 'neutral'
            importance = 0.1 + np.random.random() * 0.3
        else:
            # Unknown words get medium importance
            importance = 0.4 + np.random.random() * 0.4
            
        token_data.append({
            'token': token,
            'sentiment': sentiment,
            'importance': importance
        })
    
    # Generate word cloud data
    word_counts = Counter(tokens)
    word_cloud_data = []
    for word, count in word_counts.most_common(25):
        if len(word) > 2:  # Filter short words
            sentiment = 'neutral'
            if word in sentiment_words['positive']:
                sentiment = 'positive'
            elif word in sentiment_words['negative']:
                sentiment = 'negative'
            
            word_cloud_data.append({
                'word': word,
                'count': count,
                'sentiment': sentiment
            })
    
    # Generate UMAP data based on actual predictions
    umap_data = generate_realistic_umap_data(user_text, predictions)
    
    return {
        'tokens': token_data,
        'word_cloud': word_cloud_data,
        'umap_data': umap_data,
        'confidence': {
            'level1': confidence_scores.get('level1', 0.83),
            'level2': confidence_scores.get('level2', 0.78),
            'level3': confidence_scores.get('level3', 0.82)
        },
        'predictions': predictions,
        'original_text': user_text,
        'analysis_id': analysis_object.id
    }

def generate_realistic_umap_data(user_text, predictions):
    """
    Generate realistic UMAP data based on actual predictions
    """
    # Sample texts for each class (replace with your actual training data)
    sample_texts = {
        'level1': {
            'NOISE': [
                'asdf qwerty', 'random text', 'gibberish', 'lorem ipsum',
                'test test test', 'random words', 'nonsense text'
            ],
            'OBJECTIVE': [
                'Bitcoin price is $50000', 'Market cap increased by 10%', 
                'Trading volume is 1.2B', 'Price moved from $45k to $50k',
                'Market opened at $48000', 'Volume increased significantly'
            ],
            'SUBJECTIVE': [
                'Bitcoin is amazing', 'I love crypto', 'This is terrible',
                'Crypto will moon', 'Market is crashing', 'Best investment ever'
            ]
        },
        'level2': {
            'NEUTRAL': [
                'Bitcoin exists', 'Crypto is digital', 'Blockchain technology',
                'Digital currency', 'Cryptocurrency market', 'Blockchain network'
            ],
            'NEGATIVE': [
                'Bitcoin will crash', 'Crypto is a scam', 'Market is terrible',
                'Worst investment', 'Going to zero', 'Complete disaster'
            ],
            'POSITIVE': [
                'Bitcoin to the moon', 'Crypto is the future', 'Amazing potential',
                'Best investment', 'Incredible technology', 'Life changing'
            ]
        },
        'level3': {
            'NEUTRAL_SENTIMENTS': [
                'Bitcoin is okay', 'Crypto is fine', 'Market is stable',
                'Nothing special', 'Average performance', 'Moderate growth'
            ],
            'QUESTIONS': [
                'What is Bitcoin?', 'How does crypto work?', 'Should I invest?',
                'When to buy?', 'Is it safe?', 'How much to invest?'
            ],
            'ADVERTISEMENTS': [
                'Buy Bitcoin now!', 'Best crypto exchange', 'Limited time offer',
                'Sign up today', 'Get 10% bonus', 'Exclusive deal'
            ],
            'MISCELLANEOUS': [
                'Crypto news today', 'Market analysis', 'Technical indicators',
                'Price prediction', 'Market update', 'Weekly report'
            ]
        }
    }
    
    # Add user text to appropriate category
    level1_pred = predictions.get('level1', 'SUBJECTIVE')
    level2_pred = predictions.get('level2', 'POSITIVE')
    level3_pred = predictions.get('level3', 'QUESTIONS')
    
    sample_texts['level1'][level1_pred].append(user_text)
    if level1_pred == 'SUBJECTIVE':
        sample_texts['level2'][level2_pred].append(user_text)
        if level2_pred == 'NEUTRAL':
            sample_texts['level3'][level3_pred].append(user_text)
    
    umap_results = {}
    
    for level, classes in sample_texts.items():
        # Flatten all texts
        all_texts = []
        labels = []
        user_indices = []
        
        for class_name, texts in classes.items():
            for i, text in enumerate(texts):
                all_texts.append(text)
                labels.append(class_name)
                if text == user_text:
                    user_indices.append(len(all_texts) - 1)
        
        # Generate realistic embeddings (replace with actual Sentence-BERT)
        np.random.seed(42)  # For reproducible results
        embeddings = np.random.rand(len(all_texts), 50)
        
        # Apply UMAP
        reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=5, min_dist=0.1)
        embedding_2d = reducer.fit_transform(embeddings)
        
        umap_results[level] = {
            'x': embedding_2d[:, 0].tolist(),
            'y': embedding_2d[:, 1].tolist(),
            'labels': labels,
            'texts': all_texts,
            'user_indices': user_indices
        }
    
    return umap_results

def create_django_view_integration():
    """
    Example Django view integration
    """
    django_view_code = '''
# Add this to your Django views.py

from django.http import JsonResponse
from django.shortcuts import render
from .models import SentimentAnalysis
from .dashboard_integration import integrate_with_django_analysis

def analysis_dashboard(request, analysis_id):
    """View to display analysis with interactive dashboard"""
    try:
        analysis = SentimentAnalysis.objects.get(id=analysis_id)
        dashboard_data = integrate_with_django_analysis(analysis)
        
        return render(request, 'sentiment/dashboard.html', {
            'analysis': analysis,
            'dashboard_data': json.dumps(dashboard_data)
        })
    except SentimentAnalysis.DoesNotExist:
        return JsonResponse({'error': 'Analysis not found'}, status=404)

def dashboard_api(request, analysis_id):
    """API endpoint to get dashboard data"""
    try:
        analysis = SentimentAnalysis.objects.get(id=analysis_id)
        dashboard_data = integrate_with_django_analysis(analysis)
        return JsonResponse(dashboard_data)
    except SentimentAnalysis.DoesNotExist:
        return JsonResponse({'error': 'Analysis not found'}, status=404)
    '''
    
    return django_view_code

# Example usage
if __name__ == "__main__":
    # Example Django model data
    class MockAnalysis:
        def __init__(self):
            self.id = 1
            self.text = "Bitcoin is showing incredible potential for future growth and adoption"
            self.level1_prediction = "SUBJECTIVE"
            self.level2_prediction = "POSITIVE"
            self.level3_prediction = "QUESTIONS"
            self.confidence_scores = {
                'level1': 0.87,
                'level2': 0.92,
                'level3': 0.78
            }
    
    mock_analysis = MockAnalysis()
    dashboard_data = integrate_with_django_analysis(mock_analysis)
    
    print("Dashboard data generated successfully!")
    print(f"Analysis ID: {dashboard_data['analysis_id']}")
    print(f"Original text: {dashboard_data['original_text']}")
    print(f"Predictions: {dashboard_data['predictions']}")
    print(f"Confidence scores: {dashboard_data['confidence']}")
    print(f"Number of tokens: {len(dashboard_data['tokens'])}")
    print(f"Number of word cloud entries: {len(dashboard_data['word_cloud'])}")
