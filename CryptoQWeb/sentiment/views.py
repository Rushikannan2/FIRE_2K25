from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import SentimentAnalysis
from .ai_analyzer import SentimentAnalyzer
import json
import logging

logger = logging.getLogger(__name__)

# Initialize the sentiment analyzer
# Note: In production, you might want to use a singleton pattern or cache this
analyzer = None

def get_analyzer():
    """Get or initialize the sentiment analyzer"""
    global analyzer
    if analyzer is None:
        try:
            # Update the path to match your actual model location
            analyzer = SentimentAnalyzer(models_dir="D:\\CryptoQ\\models")
        except Exception as e:
            logger.error(f"Failed to initialize sentiment analyzer: {e}")
            analyzer = None
    return analyzer

def home(request):
    """Home page with sentiment analysis form"""
    return render(request, 'sentiment/home.html')

def test_page(request):
    """Simple test page to verify the server is working"""
    return HttpResponse("""
    <html>
    <head><title>CryptoQ Test</title></head>
    <body>
        <h1>✅ CryptoQ Server is Working!</h1>
        <p>If you can see this page, the Django server is running correctly.</p>
        <p><a href="/">Go to Sentiment Analyzer</a></p>
        <p><a href="/history/">View History</a></p>
        
        <h2>Test Form Submission:</h2>
        <form method="post" action="/analyze/">
            <input type="hidden" name="csrfmiddlewaretoken" value="test">
            <textarea name="text" placeholder="Enter test text here..." rows="3" cols="50"></textarea><br><br>
            <button type="submit">Test Analysis</button>
        </form>
    </body>
    </html>
    """)

@require_http_methods(["POST"])
def analyze_sentiment(request):
    """Analyze sentiment of input text"""
    try:
        # Get text from request
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            text = data.get('text', '').strip()
        else:
            text = request.POST.get('text', '').strip()
        
        if not text:
            return JsonResponse({
                'error': 'No text provided',
                'classification': 'NOISE'
            }, status=400)
        
        # Get analyzer
        analyzer_instance = get_analyzer()
        if analyzer_instance is None:
            return JsonResponse({
                'error': 'Sentiment analyzer not available',
                'classification': 'NOISE'
            }, status=500)
        
        # Perform analysis
        results = analyzer_instance.analyze(text)
        
        # Save to database
        sentiment_record = SentimentAnalysis.objects.create(
            text=text,
            level1_prediction=results.get('level1_prediction'),
            level2_prediction=results.get('level2_prediction'),
            level3_prediction=results.get('level3_prediction'),
            final_classification=results.get('final_classification'),
            confidence_scores=results.get('confidence_scores', {})
        )
        
        # Return results
        response_data = {
            'classification': results.get('final_classification'),
            'level1': results.get('level1_prediction'),
            'level2': results.get('level2_prediction'),
            'level3': results.get('level3_prediction'),
            'confidence_scores': results.get('confidence_scores', {}),
            'analysis_id': sentiment_record.id
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        return JsonResponse({
            'error': 'Analysis failed',
            'classification': 'NOISE'
        }, status=500)

def analyze_sentiment_form(request):
    """Handle form-based sentiment analysis"""
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        
        if not text:
            messages.error(request, 'Please enter some text to analyze.')
            return render(request, 'sentiment/home.html')
        
        try:
            # Get analyzer
            analyzer_instance = get_analyzer()
            if analyzer_instance is None:
                messages.error(request, 'Sentiment analyzer is not available.')
                return render(request, 'sentiment/home.html')
            
            # Perform analysis
            results = analyzer_instance.analyze(text)
            
            # Save to database
            sentiment_record = SentimentAnalysis.objects.create(
                text=text,
                level1_prediction=results.get('level1_prediction'),
                level2_prediction=results.get('level2_prediction'),
                level3_prediction=results.get('level3_prediction'),
                final_classification=results.get('final_classification'),
                confidence_scores=results.get('confidence_scores', {})
            )
            
            # Add success message
            messages.success(request, f'Analysis completed: {results.get("final_classification")}')
            
            # Debug: Print results to console
            print(f"DEBUG: Analysis results: {results}")
            
            return render(request, 'sentiment/home.html', {
                'analysis_result': results,
                'analysis_id': sentiment_record.id,
                'original_text': text
            })
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            messages.error(request, f'Analysis failed: {str(e)}')
            return render(request, 'sentiment/home.html')
    
    return render(request, 'sentiment/home.html')

def analysis_history(request):
    """View analysis history"""
    analyses = SentimentAnalysis.objects.all()[:50]  # Show last 50 analyses
    return render(request, 'sentiment/history.html', {'analyses': analyses})

def analysis_detail(request, analysis_id):
    """View detailed analysis results"""
    try:
        analysis = SentimentAnalysis.objects.get(id=analysis_id)
        return render(request, 'sentiment/detail.html', {'analysis': analysis})
    except SentimentAnalysis.DoesNotExist:
        messages.error(request, 'Analysis not found.')
        return redirect('sentiment:home')