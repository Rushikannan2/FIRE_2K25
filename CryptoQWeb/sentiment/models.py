from django.db import models
from django.utils import timezone

class SentimentAnalysis(models.Model):
    """Model to store sentiment analysis results"""
    
    text = models.TextField(help_text="The input text to analyze")
    level1_prediction = models.CharField(max_length=20, choices=[
        ('NOISE', 'Noise'),
        ('OBJECTIVE', 'Objective'),
        ('SUBJECTIVE', 'Subjective'),
    ], null=True, blank=True)
    level2_prediction = models.CharField(max_length=20, choices=[
        ('NEUTRAL', 'Neutral'),
        ('NEGATIVE', 'Negative'),
        ('POSITIVE', 'Positive'),
    ], null=True, blank=True)
    level3_prediction = models.CharField(max_length=20, choices=[
        ('NEUTRAL_SENTIMENT', 'Neutral Sentiment'),
        ('QUESTION', 'Question'),
        ('ADVERTISEMENT', 'Advertisement'),
        ('MISCELLANEOUS', 'Miscellaneous'),
    ], null=True, blank=True)
    final_classification = models.CharField(max_length=100, help_text="Human-readable final classification")
    confidence_scores = models.JSONField(default=dict, help_text="Confidence scores for each level")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sentiment Analysis"
        verbose_name_plural = "Sentiment Analyses"
    
    def __str__(self):
        return f"Analysis of '{self.text[:50]}...' - {self.final_classification}"
