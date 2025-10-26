from django.contrib import admin
from .models import SentimentAnalysis

@admin.register(SentimentAnalysis)
class SentimentAnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'text_preview', 'final_classification', 'level1_prediction', 'level2_prediction', 'level3_prediction', 'created_at']
    list_filter = ['level1_prediction', 'level2_prediction', 'level3_prediction', 'created_at']
    search_fields = ['text', 'final_classification']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text Preview'
