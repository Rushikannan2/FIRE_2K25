from django.urls import path
from . import views

app_name = 'sentiment'

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test_page, name='test'),
    path('analyze/', views.analyze_sentiment_form, name='analyze_form'),
    path('api/analyze/', views.analyze_sentiment, name='analyze_api'),
    path('history/', views.analysis_history, name='history'),
    path('detail/<int:analysis_id>/', views.analysis_detail, name='detail'),
    path('about-author/', views.about_author, name='about_author'),
    path('about-us/', views.about_us, name='about_us'),
]
