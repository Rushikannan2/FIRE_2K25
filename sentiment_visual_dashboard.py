import dash
from dash import dcc, html, Input, Output, State, callback_context
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import json
import re
from collections import Counter
import umap
from sentence_transformers import SentenceTransformer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "CryptoQ Sentiment Analysis Dashboard"

# Color scheme for the 3-level hierarchy
COLORS = {
    'level1': {
        'NOISE': '#dc3545',      # Red
        'OBJECTIVE': '#0d6efd',  # Blue  
        'SUBJECTIVE': '#198754'  # Green
    },
    'level2': {
        'NEUTRAL': '#6c757d',    # Gray
        'NEGATIVE': '#dc3545',   # Red
        'POSITIVE': '#28a745'    # Green
    },
    'level3': {
        'NEUTRAL_SENTIMENTS': '#6c757d',  # Gray
        'QUESTIONS': '#0dcaf0',           # Cyan
        'ADVERTISEMENTS': '#fd7e14',      # Orange
        'MISCELLANEOUS': '#6f42c1'        # Purple
    }
}

# Sample data structure - replace with your actual analysis results
def get_analysis_data(user_text, analysis_results):
    """
    Process user input and analysis results to create visualization data
    """
    # Tokenize and analyze the input text
    tokens = re.findall(r'\b\w+\b', user_text.lower())
    
    # Create token importance data
    token_data = []
    sentiment_words = {
        'positive': ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'incredible', 
                    'potential', 'growth', 'success', 'profit', 'bullish', 'moon', 'pump', 'hodl', 
                    'buy', 'strong', 'up', 'rise', 'gain', 'best', 'love', 'awesome'],
        'negative': ['bad', 'terrible', 'awful', 'horrible', 'worst', 'crash', 'dump', 'bearish', 
                    'sell', 'weak', 'down', 'fall', 'loss', 'scam', 'fraud', 'bubble', 'overpriced',
                    'hate', 'disappointed', 'worried'],
        'neutral': ['the', 'is', 'are', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
                   'by', 'from', 'about', 'into', 'through', 'during', 'will', 'can', 'should']
    }
    
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
    
    # Generate UMAP embeddings
    umap_data = generate_umap_data(user_text, analysis_results)
    
    return {
        'tokens': token_data,
        'word_cloud': word_cloud_data,
        'umap_data': umap_data,
        'confidence': analysis_results.get('confidence', {
            'level1': 0.83,
            'level2': 0.78, 
            'level3': 0.82
        }),
        'predictions': analysis_results.get('predictions', {
            'level1': 'SUBJECTIVE',
            'level2': 'POSITIVE',
            'level3': 'QUESTIONS'
        })
    }

def generate_umap_data(user_text, analysis_results):
    """
    Generate UMAP embedding data for visualization
    """
    # Sample texts for each class (in real implementation, use your training data)
    sample_texts = {
        'level1': {
            'NOISE': ['asdf qwerty', 'random text', 'gibberish'],
            'OBJECTIVE': ['Bitcoin price is $50000', 'Market cap increased', 'Trading volume is high'],
            'SUBJECTIVE': ['Bitcoin is amazing', 'I love crypto', 'This is terrible']
        },
        'level2': {
            'NEUTRAL': ['Bitcoin exists', 'Crypto is digital', 'Blockchain technology'],
            'NEGATIVE': ['Bitcoin will crash', 'Crypto is a scam', 'Market is terrible'],
            'POSITIVE': ['Bitcoin to the moon', 'Crypto is the future', 'Amazing potential']
        },
        'level3': {
            'NEUTRAL_SENTIMENTS': ['Bitcoin is okay', 'Crypto is fine', 'Market is stable'],
            'QUESTIONS': ['What is Bitcoin?', 'How does crypto work?', 'Should I invest?'],
            'ADVERTISEMENTS': ['Buy Bitcoin now!', 'Best crypto exchange', 'Limited time offer'],
            'MISCELLANEOUS': ['Crypto news today', 'Market analysis', 'Technical indicators']
        }
    }
    
    # Add user text to appropriate category
    user_prediction = analysis_results.get('predictions', {})
    level1_pred = user_prediction.get('level1', 'SUBJECTIVE')
    level2_pred = user_prediction.get('level2', 'POSITIVE')
    level3_pred = user_prediction.get('level3', 'QUESTIONS')
    
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
        
        # Generate embeddings (simplified - use actual Sentence-BERT in production)
        embeddings = np.random.rand(len(all_texts), 50)  # Replace with real embeddings
        
        # Apply UMAP
        reducer = umap.UMAP(n_components=2, random_state=42)
        embedding_2d = reducer.fit_transform(embeddings)
        
        umap_results[level] = {
            'x': embedding_2d[:, 0].tolist(),
            'y': embedding_2d[:, 1].tolist(),
            'labels': labels,
            'texts': all_texts,
            'user_indices': user_indices
        }
    
    return umap_results

def create_token_heatmap_figure(token_data):
    """
    Create token importance heatmap visualization
    """
    fig = go.Figure()
    
    x_positions = []
    y_positions = []
    colors = []
    texts = []
    hover_texts = []
    
    x_pos = 0
    y_pos = 0
    max_width = 10
    
    for i, token_info in enumerate(token_data):
        x_positions.append(x_pos)
        y_positions.append(y_pos)
        
        # Color based on sentiment
        if token_info['sentiment'] == 'positive':
            color = '#28a745'
        elif token_info['sentiment'] == 'negative':
            color = '#dc3545'
        else:
            color = '#6c757d'
            
        colors.append(color)
        texts.append(token_info['token'])
        
        hover_texts.append(f"Token: {token_info['token']}<br>"
                          f"Sentiment: {token_info['sentiment']}<br>"
                          f"Importance: {token_info['importance']:.2f}")
        
        x_pos += 1
        if x_pos >= max_width:
            x_pos = 0
            y_pos += 1
    
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=y_positions,
        mode='markers+text',
        marker=dict(
            size=30,
            color=colors,
            line=dict(width=2, color='white')
        ),
        text=texts,
        textposition="middle center",
        hovertext=hover_texts,
        hoverinfo='text'
    ))
    
    fig.update_layout(
        title="Token Importance Heatmap",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=300
    )
    
    return fig

def create_word_cloud_figure(word_cloud_data):
    """
    Create word cloud visualization
    """
    if not word_cloud_data:
        return go.Figure().add_annotation(
            text="No significant words found",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )
    
    fig = go.Figure()
    
    x_positions = []
    y_positions = []
    sizes = []
    colors = []
    texts = []
    
    # Generate random positions for words
    np.random.seed(42)
    for i, word_info in enumerate(word_cloud_data):
        x_positions.append(np.random.uniform(0, 10))
        y_positions.append(np.random.uniform(0, 10))
        sizes.append(word_info['count'] * 20)
        
        if word_info['sentiment'] == 'positive':
            colors.append('#28a745')
        elif word_info['sentiment'] == 'negative':
            colors.append('#dc3545')
        else:
            colors.append('#6c757d')
            
        texts.append(word_info['word'])
    
    fig.add_trace(go.Scatter(
        x=x_positions,
        y=y_positions,
        mode='markers+text',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=0.7,
            line=dict(width=1, color='white')
        ),
        text=texts,
        textposition="middle center",
        hovertext=[f"Word: {w['word']}<br>Count: {w['count']}<br>Sentiment: {w['sentiment']}" 
                  for w in word_cloud_data],
        hoverinfo='text'
    ))
    
    fig.update_layout(
        title="Sentiment-Weighted Word Cloud",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='#f8f9fa',
        height=300
    )
    
    return fig

def create_confidence_gauge(level, confidence, prediction):
    """
    Create confidence gauge for each level
    """
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = confidence * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Level {level}"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 75], 'color': "yellow"},
                {'range': [75, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig

def create_umap_figure(level, umap_data, level_name):
    """
    Create UMAP visualization for each level
    """
    data = umap_data[level]
    
    fig = go.Figure()
    
    # Get unique labels and their colors
    unique_labels = list(set(data['labels']))
    colors = COLORS[level_name]
    
    for label in unique_labels:
        # Get indices for this label
        indices = [i for i, l in enumerate(data['labels']) if l == label]
        
        x_vals = [data['x'][i] for i in indices]
        y_vals = [data['y'][i] for i in indices]
        texts = [data['texts'][i] for i in indices]
        
        # Check if user text is in this label
        is_user = [i in data['user_indices'] for i in indices]
        
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='markers',
            name=label,
            marker=dict(
                size=[20 if user else 10 for user in is_user],
                color=colors.get(label, '#6c757d'),
                opacity=0.7,
                line=dict(width=2, color='white')
            ),
            text=texts,
            hovertemplate='<b>%{text}</b><br>Label: ' + label + '<extra></extra>'
        ))
    
    fig.update_layout(
        title=f"UMAP Visualization - Level {level}",
        xaxis_title="UMAP Dimension 1",
        yaxis_title="UMAP Dimension 2",
        height=400,
        showlegend=True
    )
    
    return fig

def create_decision_flow_figure(predictions):
    """
    Create decision flow diagram
    """
    fig = go.Figure()
    
    # Define flow steps
    steps = [
        {'name': 'Input Tokens', 'x': 0, 'y': 0},
        {'name': 'Transformer Encoder', 'x': 2, 'y': 0},
        {'name': 'Pooled Embedding', 'x': 4, 'y': 0},
        {'name': 'Classification Head', 'x': 6, 'y': 0},
        {'name': f'Final Output: {predictions.get("level1", "SUBJECTIVE")}', 'x': 8, 'y': 0}
    ]
    
    # Add step boxes
    for step in steps:
        fig.add_trace(go.Scatter(
            x=[step['x']],
            y=[step['y']],
            mode='markers+text',
            marker=dict(size=100, color='#4F46E5', opacity=0.8),
            text=[step['name']],
            textposition="middle center",
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add arrows
    for i in range(len(steps) - 1):
        fig.add_annotation(
            x=steps[i]['x'] + 1,
            y=steps[i]['y'],
            ax=steps[i]['x'] + 0.5,
            ay=steps[i]['y'],
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#4F46E5"
        )
    
    fig.update_layout(
        title="Decision Flow Visualization",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 8.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, 0.5]),
        plot_bgcolor='white',
        height=200
    )
    
    return fig

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("CryptoQ Sentiment Analysis Dashboard", 
                style={'color': 'white', 'textAlign': 'center', 'margin': '20px'}),
        html.P("Advanced visual insights into the sentiment analysis process",
               style={'color': 'white', 'textAlign': 'center', 'marginBottom': '30px'})
    ], style={'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', 'padding': '20px'}),
    
    html.Div([
        # Input section
        html.Div([
            html.H3("Enter Text for Analysis"),
            dcc.Textarea(
                id='input-text',
                placeholder='Enter cryptocurrency-related text here...',
                value='Bitcoin is showing incredible potential for future growth and adoption',
                style={'width': '100%', 'height': 100}
            ),
            html.Button('Analyze Text', id='analyze-button', n_clicks=0,
                       style={'marginTop': '10px', 'backgroundColor': '#4F46E5', 'color': 'white'})
        ], style={'marginBottom': '30px', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'}),
        
        # Token Importance Heatmap
        html.Div([
            html.H3("Token Importance Heatmap"),
            dcc.Graph(id='token-heatmap')
        ], style={'marginBottom': '30px', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'}),
        
        # Word Cloud
        html.Div([
            html.H3("Sentiment-Weighted Word Cloud"),
            dcc.Graph(id='word-cloud')
        ], style={'marginBottom': '30px', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'}),
        
        # Confidence Gauges
        html.Div([
            html.H3("Model Confidence Gauges"),
            html.Div([
                html.Div([
                    dcc.Graph(id='level1-gauge')
                ], style={'width': '33%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='level2-gauge')
                ], style={'width': '33%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Graph(id='level3-gauge')
                ], style={'width': '33%', 'display': 'inline-block'})
            ])
        ], style={'marginBottom': '30px', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'}),
        
        # UMAP Visualizations
        html.Div([
            html.H3("UMAP Embedding Visualizations"),
            dcc.Tabs(id='umap-tabs', value='level1', children=[
                dcc.Tab(label='Level 1 (NOISE/OBJECTIVE/SUBJECTIVE)', value='level1'),
                dcc.Tab(label='Level 2 (NEUTRAL/NEGATIVE/POSITIVE)', value='level2'),
                dcc.Tab(label='Level 3 (Detailed Categories)', value='level3')
            ]),
            dcc.Graph(id='umap-plot')
        ], style={'marginBottom': '30px', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'}),
        
        # Decision Flow
        html.Div([
            html.H3("Decision Flow Visualization"),
            dcc.Graph(id='decision-flow')
        ], style={'marginBottom': '30px', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '10px'})
        
    ], style={'padding': '20px', 'maxWidth': '1200px', 'margin': '0 auto'})
])

# Callbacks
@app.callback(
    [Output('token-heatmap', 'figure'),
     Output('word-cloud', 'figure'),
     Output('level1-gauge', 'figure'),
     Output('level2-gauge', 'figure'),
     Output('level3-gauge', 'figure'),
     Output('umap-plot', 'figure'),
     Output('decision-flow', 'figure')],
    [Input('analyze-button', 'n_clicks')],
    [State('input-text', 'value')]
)
def update_visualizations(n_clicks, input_text):
    if not input_text:
        input_text = "Bitcoin is showing incredible potential for future growth and adoption"
    
    # Simulate analysis results (replace with your actual model output)
    analysis_results = {
        'confidence': {
            'level1': 0.83,
            'level2': 0.78,
            'level3': 0.82
        },
        'predictions': {
            'level1': 'SUBJECTIVE',
            'level2': 'POSITIVE', 
            'level3': 'QUESTIONS'
        }
    }
    
    # Get analysis data
    data = get_analysis_data(input_text, analysis_results)
    
    # Create visualizations
    token_fig = create_token_heatmap_figure(data['tokens'])
    word_cloud_fig = create_word_cloud_figure(data['word_cloud'])
    
    level1_gauge = create_confidence_gauge(1, data['confidence']['level1'], data['predictions']['level1'])
    level2_gauge = create_confidence_gauge(2, data['confidence']['level2'], data['predictions']['level2'])
    level3_gauge = create_confidence_gauge(3, data['confidence']['level3'], data['predictions']['level3'])
    
    umap_fig = create_umap_figure('level1', data['umap_data'], 'level1')
    decision_fig = create_decision_flow_figure(data['predictions'])
    
    return token_fig, word_cloud_fig, level1_gauge, level2_gauge, level3_gauge, umap_fig, decision_fig

@app.callback(
    Output('umap-plot', 'figure'),
    [Input('umap-tabs', 'value')],
    [State('input-text', 'value')]
)
def update_umap_plot(selected_tab, input_text):
    if not input_text:
        input_text = "Bitcoin is showing incredible potential for future growth and adoption"
    
    analysis_results = {
        'confidence': {'level1': 0.83, 'level2': 0.78, 'level3': 0.82},
        'predictions': {'level1': 'SUBJECTIVE', 'level2': 'POSITIVE', 'level3': 'QUESTIONS'}
    }
    
    data = get_analysis_data(input_text, analysis_results)
    
    level_mapping = {
        'level1': 'level1',
        'level2': 'level2', 
        'level3': 'level3'
    }
    
    return create_umap_figure(selected_tab, data['umap_data'], level_mapping[selected_tab])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
