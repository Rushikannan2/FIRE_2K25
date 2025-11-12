from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import SentimentAnalysis
from .ai_analyzer import SentimentAnalyzer
from .classification_formatter import format_classification_path
import json
import logging

logger = logging.getLogger(__name__)

# Initialize the sentiment analyzer
# Note: In production, you might want to use a singleton pattern or cache this
analyzer = None

def get_analyzer():
    """Get or initialize the sentiment analyzer (lazy loading - doesn't block startup)"""
    global analyzer
    if analyzer is None:
        try:
            # Use relative path for Render deployment
            # Don't block if models aren't ready - will use fallback analysis
            analyzer = SentimentAnalyzer(models_dir="models")
            logger.info("Sentiment analyzer initialized successfully")
        except Exception as e:
            logger.warning(f"Sentiment analyzer not available (models may still be downloading): {e}")
            logger.info("Application will use fallback rule-based analysis until models are ready")
            analyzer = None
    return analyzer

def health_check(request):
    """Health check endpoint for Render deployment"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'CryptoQ Sentiment Analyzer',
        'version': '1.0.0'
    })

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
        platform = request.POST.get('platform', '').strip()
        
        if not platform:
            messages.error(request, 'Please select a platform before analyzing.')
            return render(request, 'sentiment/home.html')
        
        if not text:
            messages.error(request, 'Please enter some text to analyze.')
            return render(request, 'sentiment/home.html', {'selected_platform': platform})
        
        try:
            # Get analyzer
            analyzer_instance = get_analyzer()
            if analyzer_instance is None:
                messages.error(request, 'Sentiment analyzer is not available.')
                return render(request, 'sentiment/home.html', {'selected_platform': platform})
            
            # Perform analysis
            results = analyzer_instance.analyze(text)
            
            # Format classification path
            classification_info = format_classification_path(
                results.get('level1_prediction'),
                results.get('level2_prediction'),
                results.get('level3_prediction')
            )
            results['classification_path'] = classification_info['full_path']
            results['classification_description'] = classification_info['description']
            results['classification_input_summary'] = classification_info['input_summary']
            
            # Save to database
            sentiment_record = SentimentAnalysis.objects.create(
                text=text,
                platform=platform,
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
                'original_text': text,
                'selected_platform': platform,
                'classification_info': classification_info
            })
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            messages.error(request, f'Analysis failed: {str(e)}')
            return render(request, 'sentiment/home.html', {'selected_platform': platform})
    
    return render(request, 'sentiment/home.html')

def analysis_history(request):
    """View analysis history"""
    analyses = SentimentAnalysis.objects.all()[:50]  # Show last 50 analyses
    return render(request, 'sentiment/history.html', {'analyses': analyses})

def analysis_detail(request, analysis_id):
    """View detailed analysis results"""
    try:
        analysis = SentimentAnalysis.objects.get(id=analysis_id)
        # Format classification path
        classification_info = format_classification_path(
            analysis.level1_prediction,
            analysis.level2_prediction,
            analysis.level3_prediction
        )
        return render(request, 'sentiment/detail.html', {
            'analysis': analysis,
            'classification_info': classification_info
        })
    except SentimentAnalysis.DoesNotExist:
        messages.error(request, 'Analysis not found.')
        return redirect('sentiment:home')

def about_author(request):
    """About Author page"""
    return render(request, 'sentiment/aboutauthor.html')

def about_us(request):
    """About Us page"""
    return render(request, 'sentiment/aboutus.html')

def edit_analysis(request, analysis_id):
    """Edit and re-analyze a sentiment analysis"""
    try:
        analysis = SentimentAnalysis.objects.get(id=analysis_id)
        
        if request.method == 'POST':
            new_text = request.POST.get('text', '').strip()
            platform = request.POST.get('platform', '').strip()
            
            if not platform:
                messages.error(request, 'Please select a platform.')
                return render(request, 'sentiment/edit_analysis.html', {'analysis': analysis})
            
            if not new_text:
                messages.error(request, 'Please enter some text to analyze.')
                return render(request, 'sentiment/edit_analysis.html', {'analysis': analysis})
            
            try:
                # Get analyzer
                analyzer_instance = get_analyzer()
                if analyzer_instance is None:
                    messages.error(request, 'Sentiment analyzer is not available.')
                    return render(request, 'sentiment/edit_analysis.html', {'analysis': analysis})
                
                # Perform new analysis
                results = analyzer_instance.analyze(new_text)
                
                # Update the record
                analysis.text = new_text
                analysis.platform = platform
                analysis.level1_prediction = results.get('level1_prediction')
                analysis.level2_prediction = results.get('level2_prediction')
                analysis.level3_prediction = results.get('level3_prediction')
                analysis.final_classification = results.get('final_classification')
                analysis.confidence_scores = results.get('confidence_scores', {})
                analysis.save()
                
                messages.success(request, 'Analysis updated successfully!')
                return redirect('sentiment:detail', analysis_id=analysis.id)
                
            except Exception as e:
                logger.error(f"Error in edit analysis: {e}")
                messages.error(request, f'Analysis failed: {str(e)}')
                return render(request, 'sentiment/edit_analysis.html', {'analysis': analysis})
        
        return render(request, 'sentiment/edit_analysis.html', {'analysis': analysis})
        
    except SentimentAnalysis.DoesNotExist:
        messages.error(request, 'Analysis not found.')
        return redirect('sentiment:history')

def delete_analysis(request, analysis_id):
    """Delete a sentiment analysis"""
    try:
        analysis = SentimentAnalysis.objects.get(id=analysis_id)
        
        if request.method == 'POST':
            analysis.delete()
            messages.success(request, 'Analysis deleted successfully.')
            return redirect('sentiment:history')
        
        return render(request, 'sentiment/delete_analysis.html', {'analysis': analysis})
        
    except SentimentAnalysis.DoesNotExist:
        messages.error(request, 'Analysis not found.')
        return redirect('sentiment:history')