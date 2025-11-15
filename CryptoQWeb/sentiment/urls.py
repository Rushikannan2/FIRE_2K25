from django.urls import path
from . import views

app_name = 'sentiment'

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health_check, name='health_check'),
    path('test/', views.test_page, name='test'),
    path('analyze/', views.analyze_sentiment_form, name='analyze_form'),
    path('api/analyze/', views.analyze_sentiment, name='analyze_api'),
    path('history/', views.analysis_history, name='history'),
    path('detail/<int:analysis_id>/', views.analysis_detail, name='detail'),
    path('edit/<int:analysis_id>/', views.edit_analysis, name='edit'),
    path('delete/<int:analysis_id>/', views.delete_analysis, name='delete'),
    path('about-author/', views.about_author, name='about_author'),
    path('about-us/', views.about_us, name='about_us'),
    path('gallery/', views.gallery, name='gallery'),
]
