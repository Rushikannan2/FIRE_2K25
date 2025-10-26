from django.core.management.base import BaseCommand
from sentiment.ai_analyzer import SentimentAnalyzer

class Command(BaseCommand):
    help = 'Test the sentiment analyzer with sample text'

    def add_arguments(self, parser):
        parser.add_argument('--text', type=str, help='Text to analyze')
        parser.add_argument('--models-dir', type=str, default='models', help='Models directory path')

    def handle(self, *args, **options):
        text = options.get('text', 'This is a great cryptocurrency! I love Bitcoin.')
        
        self.stdout.write(f"Testing sentiment analyzer with text: '{text}'")
        
        try:
            analyzer = SentimentAnalyzer(models_dir=options['models_dir'])
            results = analyzer.analyze(text)
            
            self.stdout.write(self.style.SUCCESS("Analysis completed successfully!"))
            self.stdout.write(f"Final Classification: {results['final_classification']}")
            self.stdout.write(f"Level 1: {results.get('level1_prediction', 'N/A')}")
            self.stdout.write(f"Level 2: {results.get('level2_prediction', 'N/A')}")
            self.stdout.write(f"Level 3: {results.get('level3_prediction', 'N/A')}")
            
            if results.get('confidence_scores'):
                self.stdout.write("Confidence Scores:")
                for level, score in results['confidence_scores'].items():
                    self.stdout.write(f"  {level}: {score:.3f}")
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
