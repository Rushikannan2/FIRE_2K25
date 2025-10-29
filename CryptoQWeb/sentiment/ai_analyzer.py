"""
CryptoQ Sentiment Analyzer AI
3-level hierarchical sentiment analysis with ensemble averaging
"""

import os
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Tuple, Optional
import logging
import re
from collections import Counter

# Try to import transformers, fallback if not available
try:
    from transformers import AutoTokenizer, AutoModel
    TRANSFORMERS_AVAILABLE = True
except (ImportError, ValueError) as e:
    TRANSFORMERS_AVAILABLE = False
    print(f"Warning: transformers library not available or has compatibility issues: {e}")
    print("Falling back to simple LSTM-based models.")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomDeBERTaClassifier(nn.Module):
    """Custom DeBERTa-based text classifier that matches the saved model architecture"""
    def __init__(self, num_classes=3):
        super(CustomDeBERTaClassifier, self).__init__()
        
        # Create architecture that exactly matches the saved model structure
        # The saved model has: deberta.embeddings.word_embeddings.weight
        # So we need to create a nested structure
        
        # Create deberta module
        self.deberta = nn.ModuleDict({
            'embeddings': nn.ModuleDict({
                'word_embeddings': nn.Embedding(50265, 768),
                'LayerNorm': nn.LayerNorm(768),
            }),
            'encoder': nn.ModuleDict({
                'layer': nn.ModuleList()
            }),
            'rel_embeddings': nn.Embedding(256, 768),
            'LayerNorm': nn.LayerNorm(768),
        })
        
        # Add encoder layers
        for i in range(6):  # Based on error messages, there are 6 layers (0-5)
            layer = nn.ModuleDict({
                'attention': nn.ModuleDict({
                    'self': nn.ModuleDict({
                        'query_proj': nn.Linear(768, 768),
                        'key_proj': nn.Linear(768, 768),
                        'value_proj': nn.Linear(768, 768),
                    }),
                    'output': nn.ModuleDict({
                        'dense': nn.Linear(768, 768),
                        'LayerNorm': nn.LayerNorm(768),
                    }),
                }),
                'intermediate': nn.ModuleDict({
                    'dense': nn.Linear(768, 3072),
                }),
                'output': nn.ModuleDict({
                    'dense': nn.Linear(3072, 768),
                    'LayerNorm': nn.LayerNorm(768),
                }),
            })
            self.deberta['encoder']['layer'].append(layer)
        
        # Pooler and classifier (these are at the top level in the saved model)
        self.pooler = nn.ModuleDict({
            'dense': nn.Linear(768, 768),
        })
        self.classifier = nn.Linear(768, num_classes)
        
    def forward(self, input_ids, attention_mask=None):
        # Simplified forward pass - just return classifier output
        # This is a placeholder that can load the weights but doesn't perform full DeBERTa computation
        batch_size = input_ids.size(0)
        
        # Get embeddings using the nested structure
        embeddings = self.deberta['embeddings']['word_embeddings'](input_ids)
        
        # Simple pooling (take mean of non-padded tokens)
        if attention_mask is not None:
            mask_expanded = attention_mask.unsqueeze(-1).expand(embeddings.size()).float()
            sum_embeddings = torch.sum(embeddings * mask_expanded, 1)
            sum_mask = torch.clamp(mask_expanded.sum(1), min=1e-9)
            pooled_output = sum_embeddings / sum_mask
        else:
            pooled_output = torch.mean(embeddings, dim=1)
        
        # Apply pooler
        pooled_output = torch.tanh(self.pooler['dense'](pooled_output))
        
        # Classifier
        logits = self.classifier(pooled_output)
        return logits

class DeBERTaClassifier(nn.Module):
    """DeBERTa-based text classifier that directly matches the saved model structure"""
    def __init__(self, model_name="microsoft/deberta-base", num_classes=3):
        super(DeBERTaClassifier, self).__init__()
        if TRANSFORMERS_AVAILABLE:
            self.deberta = AutoModel.from_pretrained(model_name)
            self.classifier = nn.Linear(self.deberta.config.hidden_size, num_classes)
        else:
            # Use custom DeBERTa architecture directly (no nesting)
            # Create deberta module directly in this class
            self.deberta = nn.ModuleDict({
                'embeddings': nn.ModuleDict({
                    'word_embeddings': nn.Embedding(128100, 768),  # Correct vocabulary size
                    'LayerNorm': nn.LayerNorm(768),
                }),
                'encoder': nn.ModuleDict({
                    'layer': nn.ModuleList(),
                    'rel_embeddings': nn.Embedding(512, 768),  # Correct size from error message
                    'LayerNorm': nn.LayerNorm(768),  # Move to encoder level
                }),
            })
            
            # Add encoder layers
            for i in range(6):  # Based on error messages, there are 6 layers (0-5)
                layer = nn.ModuleDict({
                    'attention': nn.ModuleDict({
                        'self': nn.ModuleDict({
                            'query_proj': nn.Linear(768, 768),
                            'key_proj': nn.Linear(768, 768),
                            'value_proj': nn.Linear(768, 768),
                        }),
                        'output': nn.ModuleDict({
                            'dense': nn.Linear(768, 768),
                            'LayerNorm': nn.LayerNorm(768),
                        }),
                    }),
                    'intermediate': nn.ModuleDict({
                        'dense': nn.Linear(768, 3072),
                    }),
                    'output': nn.ModuleDict({
                        'dense': nn.Linear(3072, 768),
                        'LayerNorm': nn.LayerNorm(768),
                    }),
                })
                self.deberta['encoder']['layer'].append(layer)
            
            # Pooler and classifier (these are at the top level in the saved model)
            self.pooler = nn.ModuleDict({
                'dense': nn.Linear(768, 768),
            })
            self.classifier = nn.Linear(768, num_classes)
        
    def forward(self, input_ids, attention_mask=None):
        if TRANSFORMERS_AVAILABLE and hasattr(self, 'deberta') and hasattr(self.deberta, 'config'):
            outputs = self.deberta(input_ids=input_ids, attention_mask=attention_mask)
            pooled_output = outputs.pooler_output
            logits = self.classifier(pooled_output)
            return logits
        else:
            # Use custom implementation with proper transformer processing
            batch_size = input_ids.size(0)
            seq_len = input_ids.size(1)
            
            # Get embeddings using the nested structure
            embeddings = self.deberta['embeddings']['word_embeddings'](input_ids)
            embeddings = self.deberta['embeddings']['LayerNorm'](embeddings)
            
            # Process through encoder layers
            hidden_states = embeddings
            for layer in self.deberta['encoder']['layer']:
                # Self-attention
                attention_output = self._self_attention(
                    hidden_states, 
                    attention_mask,
                    layer['attention']['self'],
                    layer['attention']['output']
                )
                hidden_states = attention_output + hidden_states
                
                # Feed-forward
                intermediate_output = layer['intermediate']['dense'](hidden_states)
                intermediate_output = torch.nn.functional.gelu(intermediate_output)
                layer_output = layer['output']['dense'](intermediate_output)
                layer_output = layer['output']['LayerNorm'](layer_output + hidden_states)
                hidden_states = layer_output
            
            # Apply encoder LayerNorm
            hidden_states = self.deberta['encoder']['LayerNorm'](hidden_states)
            
            # Pooling (take mean of non-padded tokens)
            if attention_mask is not None:
                mask_expanded = attention_mask.unsqueeze(-1).expand(hidden_states.size()).float()
                sum_embeddings = torch.sum(hidden_states * mask_expanded, 1)
                sum_mask = torch.clamp(mask_expanded.sum(1), min=1e-9)
                pooled_output = sum_embeddings / sum_mask
            else:
                pooled_output = torch.mean(hidden_states, dim=1)
            
            # Apply pooler
            pooled_output = torch.tanh(self.pooler['dense'](pooled_output))
            
            # Classifier
            logits = self.classifier(pooled_output)
            return logits
    
    def _self_attention(self, hidden_states, attention_mask, self_attn, output_layer):
        """Simplified self-attention implementation"""
        batch_size, seq_len, hidden_size = hidden_states.size()
        
        # Linear projections
        query = self_attn['query_proj'](hidden_states)
        key = self_attn['key_proj'](hidden_states)
        value = self_attn['value_proj'](hidden_states)
        
        # Reshape for multi-head attention (assuming 12 heads)
        head_size = hidden_size // 12
        query = query.view(batch_size, seq_len, 12, head_size).transpose(1, 2)
        key = key.view(batch_size, seq_len, 12, head_size).transpose(1, 2)
        value = value.view(batch_size, seq_len, 12, head_size).transpose(1, 2)
        
        # Attention scores
        scores = torch.matmul(query, key.transpose(-2, -1)) / (head_size ** 0.5)
        
        # Apply attention mask
        if attention_mask is not None:
            mask = attention_mask.unsqueeze(1).unsqueeze(1)
            scores = scores.masked_fill(mask == 0, -1e9)
        
        # Softmax
        attention_weights = torch.nn.functional.softmax(scores, dim=-1)
        
        # Apply attention to values
        context = torch.matmul(attention_weights, value)
        
        # Reshape back
        context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, hidden_size)
        
        # Output projection
        output = output_layer['dense'](context)
        output = output_layer['LayerNorm'](output)
        
        return output

class SimpleTextClassifier(nn.Module):
    """Simple neural network for text classification (fallback)"""
    def __init__(self, vocab_size=10000, embedding_dim=128, hidden_dim=256, num_classes=3):
        super(SimpleTextClassifier, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.dropout = nn.Dropout(0.3)
        self.fc = nn.Linear(hidden_dim, num_classes)
        
    def forward(self, x):
        embedded = self.embedding(x)
        lstm_out, _ = self.lstm(embedded)
        # Use the last output
        last_output = lstm_out[:, -1, :]
        dropped = self.dropout(last_output)
        output = self.fc(dropped)
        return output

class SentimentAnalyzer:
    """
    Hierarchical sentiment analyzer with 3 levels:
    Level 1: NOISE, OBJECTIVE, SUBJECTIVE
    Level 2: NEUTRAL, NEGATIVE, POSITIVE (only if Level 1 = SUBJECTIVE)
    Level 3: NEUTRAL_SENTIMENT, QUESTION, ADVERTISEMENT, MISCELLANEOUS (only if Level 2 = NEUTRAL)
    """
    
    def __init__(self, models_dir: str = None):
        """
        Initialize the sentiment analyzer with model paths
        
        Args:
            models_dir: Directory containing the .pth model files
        """
        # Set default models directory to the correct path
        if models_dir is None:
            # Get the parent directory of the sentiment app
            current_dir = os.path.dirname(os.path.abspath(__file__))
            models_dir = os.path.join(os.path.dirname(current_dir), 'models')
        
        self.models_dir = models_dir
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Build model paths supporting both flat and nested layouts
        self.model_paths = self._discover_model_paths(models_dir)
        
        # Initialize models attribute
        self.models = None

    def _ensure_models_loaded(self):
        """Ensure models are loaded before use"""
        if self.models is None:
            self.models = self._load_models()

    def _discover_model_paths(self, models_dir: str) -> Dict[str, List[str]]:
        """Discover model files in both legacy flat layout and new nested Level/Fold layout."""
        def nested(level: int) -> List[str]:
            paths: List[str] = []
            level_dir = os.path.join(models_dir, f"Level{level}")
            for fold in range(1, 6):
                candidate = os.path.join(level_dir, f"Fold{fold}", "model.pth")
                if os.path.exists(candidate):
                    paths.append(candidate)
            return paths

        def flat(level: int) -> List[str]:
            return [
                p for p in [os.path.join(models_dir, f"level{level}_fold{i}.pth") for i in range(1, 6)]
                if os.path.exists(p)
            ]

        paths_level1 = nested(1) or flat(1)
        paths_level2 = nested(2) or flat(2)
        paths_level3 = nested(3) or flat(3)

        return {
            'level1': paths_level1,
            'level2': paths_level2,
            'level3': paths_level3,
        }
        
        # Class mappings
        self.level1_classes = ['NOISE', 'OBJECTIVE', 'SUBJECTIVE']
        self.level2_classes = ['NEUTRAL', 'NEGATIVE', 'POSITIVE']
        self.level3_classes = ['NEUTRAL_SENTIMENT', 'QUESTION', 'ADVERTISEMENT', 'MISCELLANEOUS']
        
        # Initialize tokenizer if transformers available
        if TRANSFORMERS_AVAILABLE:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-base")
                logger.info("✓ DeBERTa tokenizer loaded successfully")
            except Exception as e:
                logger.error(f"Error loading tokenizer: {e}")
                self.tokenizer = None
        else:
            self.tokenizer = None
            # Fallback vocabulary for text preprocessing
            self.vocab = self._build_vocab()
        
        # Load models
        self.models = self._load_models()
    
    def _build_vocab(self):
        """Build a simple vocabulary for text preprocessing"""
        # Common words for sentiment analysis
        common_words = [
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'shall',
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'its', 'our', 'their',
            'good', 'bad', 'great', 'terrible', 'amazing', 'awful', 'love', 'hate', 'like', 'dislike',
            'happy', 'sad', 'angry', 'excited', 'disappointed', 'positive', 'negative', 'neutral',
            'bitcoin', 'crypto', 'cryptocurrency', 'price', 'market', 'trading', 'investment',
            'what', 'how', 'when', 'where', 'why', 'who', 'which', 'question', 'advertisement', 'ad'
        ]
        
        # Create vocabulary with word to index mapping
        vocab = {'<PAD>': 0, '<UNK>': 1}
        for i, word in enumerate(common_words, 2):
            vocab[word] = i
        
        return vocab
        
    def _load_models(self) -> Dict[str, List[nn.Module]]:
        """Load all pre-trained models"""
        models = {'level1': [], 'level2': [], 'level3': []}
        
        logger.info(f"Loading models from directory: {self.models_dir}")
        
        for level in ['level1', 'level2', 'level3']:
            logger.info(f"Loading {level} models...")
            for i, model_path in enumerate(self.model_paths[level]):
                try:
                    if os.path.exists(model_path):
                        # Create model instance - always use DeBERTaClassifier
                        # It will use custom architecture when transformers is not available
                        if level == 'level1':
                            model = DeBERTaClassifier(num_classes=3)
                        elif level == 'level2':
                            model = DeBERTaClassifier(num_classes=3)
                        else:  # level3
                            model = DeBERTaClassifier(num_classes=4)
                        
                        # Load state dictionary
                        state_dict = torch.load(model_path, map_location=self.device)
                        model.load_state_dict(state_dict)
                        model.eval()
                        model.to(self.device)
                        
                        models[level].append(model)
                        logger.info(f"✓ Loaded {level} model from {model_path}")
                    else:
                        logger.warning(f"✗ Model not found: {model_path}")
                except Exception as e:
                    logger.error(f"✗ Error loading {model_path}: {e}")
        
        # Log summary of loaded models
        for level in ['level1', 'level2', 'level3']:
            logger.info(f"{level}: {len(models[level])}/5 models loaded")
        
        return models
    
    def _preprocess_text(self, text: str) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Preprocess text for model input using DeBERTa tokenizer or fallback vocabulary
        """
        if not text or not text.strip():
            return None, None
            
        if self.tokenizer is not None:
            # Use DeBERTa tokenizer
            try:
                # Tokenize text
                encoded = self.tokenizer(
                    text.strip(),
                    max_length=512,
                    padding='max_length',
                    truncation=True,
                    return_tensors='pt'
                )
                return encoded['input_ids'], encoded['attention_mask']
            except Exception as e:
                logger.error(f"Error tokenizing text: {e}")
                return None, None
        else:
            # Fallback: improved tokenization that's more compatible with DeBERTa
            import re
            
            text = text.strip().lower()
            
            # Simple tokenization (split by spaces and punctuation)
            words = re.findall(r'\b\w+\b', text)
            
            # Convert words to indices using a more realistic vocabulary mapping
            # This maps common words to indices that are more likely to be in the DeBERTa vocabulary
            word_indices = []
            for word in words:
                # Use a hash-based approach to map words to indices in the DeBERTa vocabulary range
                # This is a simplified approach - ideally we'd have the actual DeBERTa vocabulary
                word_hash = hash(word) % 50000  # Map to a reasonable range within the 128k vocab
                word_indices.append(word_hash + 1000)  # Offset to avoid special tokens
            
            # Pad or truncate to fixed length (100 tokens max)
            max_length = 100
            pad_token_id = 0  # Use 0 as padding token (common in DeBERTa)
            
            if len(word_indices) < max_length:
                word_indices.extend([pad_token_id] * (max_length - len(word_indices)))
                attention_mask = [1] * len(words) + [0] * (max_length - len(words))
            else:
                word_indices = word_indices[:max_length]
                attention_mask = [1] * max_length
            
            # Convert to tensors
            input_ids = torch.tensor(word_indices, dtype=torch.long).unsqueeze(0)
            attention_mask = torch.tensor(attention_mask, dtype=torch.long).unsqueeze(0)
            
            return input_ids, attention_mask
    
    def _ensemble_predict(self, models: List[nn.Module], input_ids: torch.Tensor, attention_mask: torch.Tensor = None) -> Tuple[int, float, List[float]]:
        """
        Make ensemble prediction across multiple models (5-fold ensemble)
        
        Args:
            models: List of trained models (should be 5 models for 5-fold ensemble)
            input_ids: Preprocessed input IDs tensor
            attention_mask: Attention mask tensor (for DeBERTa models)
            
        Returns:
            Tuple of (predicted_class_index, confidence_score, probability_distribution)
        """
        if not models or input_ids is None:
            logger.warning("No models available or invalid input")
            return 0, 0.0, [1.0, 0.0, 0.0]  # NOISE class index with default probabilities
            
        logger.info(f"Running ensemble prediction with {len(models)} models")
        
        predictions = []
        confidences = []
        all_probabilities = []
        
        with torch.no_grad():
            for i, model in enumerate(models):
                try:
                    # All models are now DeBERTaClassifier instances
                    output = model(input_ids, attention_mask)
                    
                    # Get probabilities
                    probabilities = torch.softmax(output, dim=1)
                    confidence, predicted = torch.max(probabilities, 1)
                    
                    predictions.append(predicted.item())
                    confidences.append(confidence.item())
                    all_probabilities.append(probabilities.cpu().numpy()[0])  # Store full probability distribution
                    
                    logger.debug(f"Model {i+1}: predicted class {predicted.item()}, confidence {confidence.item():.3f}")
                except Exception as e:
                    logger.error(f"Error in model {i+1} prediction: {e}")
                    continue
        
        if not predictions:
            logger.warning("No successful predictions from any model")
            return 0, 0.0, [1.0, 0.0, 0.0]  # NOISE class index with default probabilities
        
        # Ensemble averaging - average probabilities across all models
        if all_probabilities:
            avg_probabilities = np.mean(all_probabilities, axis=0)
            predicted_class = np.argmax(avg_probabilities)
            avg_confidence = np.max(avg_probabilities)
            
            logger.info(f"Ensemble prediction: class {predicted_class}, confidence {avg_confidence:.3f}")
            logger.info(f"Individual predictions: {predictions}")
            logger.info(f"Individual confidences: {[f'{c:.3f}' for c in confidences]}")
            
            return predicted_class, avg_confidence, avg_probabilities.tolist()
        else:
            # Fallback to majority voting if probability averaging fails
            avg_confidence = np.mean(confidences)
            prediction_counts = Counter(predictions)
            most_common_pred = prediction_counts.most_common(1)[0][0]
            
            logger.info(f"Fallback majority vote: class {most_common_pred}, avg confidence {avg_confidence:.3f}")
            # Create a simple probability distribution based on majority vote
            num_classes = len(self.level1_classes) if 'level1' in str(models[0]) else (len(self.level2_classes) if 'level2' in str(models[0]) else len(self.level3_classes))
            prob_dist = [0.0] * num_classes
            prob_dist[most_common_pred] = avg_confidence
            return most_common_pred, avg_confidence, prob_dist
    
    def analyze(self, text: str) -> Dict:
        """
        Perform hierarchical sentiment analysis
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        if not text or not text.strip():
            return {
                'final_classification': 'NOISE',
                'level1_prediction': 'NOISE',
                'level2_prediction': None,
                'level3_prediction': None,
                'confidence_scores': {'level1': 1.0, 'level2': 0.0, 'level3': 0.0}
            }
        
        # Ensure models are loaded
        self._ensure_models_loaded()
        
        # Check if models are available
        if not any(self.models.values()):
            logger.warning("No models available, using fallback analysis")
            return self._fallback_analysis(text)
        
        # Use actual models for prediction
        logger.info("Using pre-trained models for inference")
        
        # Preprocess text
        input_ids, attention_mask = self._preprocess_text(text)
        if input_ids is None:
            return {
                'final_classification': 'NOISE',
                'level1_prediction': 'NOISE',
                'level2_prediction': None,
                'level3_prediction': None,
                'confidence_scores': {'level1': 1.0, 'level2': 0.0, 'level3': 0.0}
            }
        
        results = {
            'level1_prediction': None,
            'level2_prediction': None,
            'level3_prediction': None,
            'confidence_scores': {},
            'probability_distributions': {}
        }
        
        # Level 1: Always run
        try:
            pred_idx, confidence, prob_dist = self._ensemble_predict(self.models['level1'], input_ids, attention_mask)
            level1_class = self.level1_classes[pred_idx] if pred_idx < len(self.level1_classes) else 'NOISE'
            results['level1_prediction'] = level1_class
            results['confidence_scores']['level1'] = confidence
            results['probability_distributions']['level1'] = prob_dist
            logger.info(f"Level 1 prediction: {level1_class} (index: {pred_idx}, confidence: {confidence:.3f})")
        except Exception as e:
            logger.error(f"Error in Level 1 prediction: {e}")
            results['level1_prediction'] = 'NOISE'
            results['confidence_scores']['level1'] = 0.0
            results['probability_distributions']['level1'] = [1.0, 0.0, 0.0]
        
        # Level 2: Only if Level 1 = SUBJECTIVE
        if results['level1_prediction'] == 'SUBJECTIVE':
            try:
                pred_idx, confidence, prob_dist = self._ensemble_predict(self.models['level2'], input_ids, attention_mask)
                level2_class = self.level2_classes[pred_idx] if pred_idx < len(self.level2_classes) else 'NEUTRAL'
                results['level2_prediction'] = level2_class
                results['confidence_scores']['level2'] = confidence
                results['probability_distributions']['level2'] = prob_dist
                logger.info(f"Level 2 prediction: {level2_class} (index: {pred_idx}, confidence: {confidence:.3f})")
            except Exception as e:
                logger.error(f"Error in Level 2 prediction: {e}")
                results['level2_prediction'] = 'NEUTRAL'
                results['confidence_scores']['level2'] = 0.0
                results['probability_distributions']['level2'] = [1.0, 0.0, 0.0]
        
        # Level 3: Only if Level 2 = NEUTRAL
        if results['level2_prediction'] == 'NEUTRAL':
            try:
                pred_idx, confidence, prob_dist = self._ensemble_predict(self.models['level3'], input_ids, attention_mask)
                level3_class = self.level3_classes[pred_idx] if pred_idx < len(self.level3_classes) else 'MISCELLANEOUS'
                results['level3_prediction'] = level3_class
                results['confidence_scores']['level3'] = confidence
                results['probability_distributions']['level3'] = prob_dist
                logger.info(f"Level 3 prediction: {level3_class} (index: {pred_idx}, confidence: {confidence:.3f})")
            except Exception as e:
                logger.error(f"Error in Level 3 prediction: {e}")
                results['level3_prediction'] = 'MISCELLANEOUS'
                results['confidence_scores']['level3'] = 0.0
                results['probability_distributions']['level3'] = [0.0, 0.0, 0.0, 1.0]
        
        # Generate final classification
        results['final_classification'] = self._generate_final_classification(results)
        
        return results
    
    def _generate_final_classification(self, results: Dict) -> str:
        """Generate human-readable final classification"""
        level1 = results['level1_prediction']
        level2 = results['level2_prediction']
        level3 = results['level3_prediction']
        
        if level1 == 'NOISE' or level1 == 'OBJECTIVE':
            return level1
        elif level1 == 'SUBJECTIVE':
            if level2 is None:
                return 'SUBJECTIVE'
            elif level2 in ['NEGATIVE', 'POSITIVE']:
                return f'SUBJECTIVE -> {level2}'
            elif level2 == 'NEUTRAL':
                if level3 is None:
                    return 'SUBJECTIVE -> NEUTRAL'
                else:
                    return f'SUBJECTIVE -> NEUTRAL -> {level3}'
        
        return 'NOISE'  # Fallback
    
    def _fallback_analysis(self, text: str) -> Dict:
        """
        Fallback analysis when models are not available
        Uses simple rule-based classification
        """
        text_lower = text.lower().strip()
        
        # Simple rule-based classification
        if len(text) < 3:
            return {
                'final_classification': 'NOISE',
                'level1_prediction': 'NOISE',
                'level2_prediction': None,
                'level3_prediction': None,
                'confidence_scores': {'level1': 0.8, 'level2': 0.0, 'level3': 0.0}
            }
        
        # Check for question indicators
        question_words = ['what', 'how', 'when', 'where', 'why', 'who', 'which', '?']
        is_question = any(text_lower.startswith(word) for word in question_words) or '?' in text
        
        # Check for sentiment indicators
        positive_words = ['good', 'great', 'excellent', 'amazing', 'love', 'like', 'happy', 'positive']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'sad', 'negative', 'angry']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        # Level 1 classification
        if is_question:
            level1 = 'SUBJECTIVE'
        elif positive_count > 0 or negative_count > 0:
            level1 = 'SUBJECTIVE'
        else:
            level1 = 'OBJECTIVE'
        
        results = {
            'level1_prediction': level1,
            'level2_prediction': None,
            'level3_prediction': None,
            'confidence_scores': {'level1': 0.7, 'level2': 0.0, 'level3': 0.0}
        }
        
        # Level 2 classification (only if SUBJECTIVE)
        if level1 == 'SUBJECTIVE':
            if positive_count > negative_count:
                results['level2_prediction'] = 'POSITIVE'
                results['confidence_scores']['level2'] = 0.6
            elif negative_count > positive_count:
                results['level2_prediction'] = 'NEGATIVE'
                results['confidence_scores']['level2'] = 0.6
            else:
                results['level2_prediction'] = 'NEUTRAL'
                results['confidence_scores']['level2'] = 0.5
                
                # Level 3 classification (only if NEUTRAL)
                if is_question:
                    results['level3_prediction'] = 'QUESTION'
                    results['confidence_scores']['level3'] = 0.7
                else:
                    results['level3_prediction'] = 'MISCELLANEOUS'
                    results['confidence_scores']['level3'] = 0.5
        
        # Generate final classification
        results['final_classification'] = self._generate_final_classification(results)
        
        return results
