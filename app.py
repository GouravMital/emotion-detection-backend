from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import PyPDF2
import io
import re
from typing import Dict, List, Tuple
import numpy as np
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Configure Gemini API
genai.configure(api_key="-uRU2xX7mF25btw_e1bDxjI1Q")
gemini_model = genai.GenerativeModel('models/gemini-2.0-flash')

# Initialize emotion detection model
print("Loading emotion detection model...")
tokenizer = AutoTokenizer.from_pretrained("bhadresh-savani/bert-base-go-emotion")
model = AutoModelForSequenceClassification.from_pretrained("bhadresh-savani/bert-base-go-emotion")
emotion_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, return_all_scores=True)

# Emotion color mapping
EMOTION_COLORS = {
    'admiration': '#4CAF50',
    'amusement': '#FFC107',
    'anger': '#F44336',
    'annoyance': '#FF9800',
    'approval': '#8BC34A',
    'caring': '#E91E63',
    'confusion': '#9C27B0',
    'curiosity': '#673AB7',
    'desire': '#E91E63',
    'disappointment': '#607D8B',
    'disapproval': '#795548',
    'disgust': '#BF360C',
    'embarrassment': '#FF5722',
    'excitement': '#FFEB3B',
    'fear': '#D32F2F',
    'gratitude': '#4CAF50',
    'grief': '#424242',
    'joy': '#FFEB3B',
    'love': '#E91E63',
    'nervousness': '#FF9800',
    'optimism': '#8BC34A',
    'pride': '#3F51B5',
    'realization': '#2196F3',
    'relief': '#00BCD4',
    'remorse': '#607D8B',
    'sadness': '#2196F3',
    'surprise': '#FF9800',
    'neutral': '#9E9E9E'
}

def extract_text_from_pdf(pdf_file) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text.strip()
    except Exception as e:
        raise Exception(f"Error extracting PDF text: {str(e)}")

def split_text_into_sentences(text: str) -> List[str]:
    """Split text into sentences"""
    sentences = re.split(r'[.!?]+', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def analyze_emotion(text: str) -> List[Dict]:
    """Analyze emotion in text using enhanced Gemini API + BERT model"""
    try:
        # First, use Gemini API for contextual understanding
        prompt = f"""
        Analyze the emotional content of this text with precision:
        "{text}"
        
        Provide a detailed emotional analysis with these specific emotions and their intensity percentages (0-100):
        - joy, excitement, happiness, love, admiration, gratitude, optimism, pride, relief, amusement
        - sadness, grief, disappointment, remorse, embarrassment, nervousness, fear
        - anger, annoyance, disgust, disapproval
        - curiosity, realization, confusion, desire, caring, approval, surprise, neutral
        
        Return ONLY a JSON object in this exact format:
        {{
            "primary_emotion": "emotion_name",
            "primary_score": 85.5,
            "emotions": {{
                "emotion_name": score,
                "emotion_name": score
            }},
            "confidence": 0.95,
            "explanation": "Brief explanation of the emotional analysis"
        }}
        """
        
        try:
            response = gemini_model.generate_content(prompt)
            gemini_result = response.text
            
            # Extract JSON from response
            import json
            json_start = gemini_result.find('{')
            json_end = gemini_result.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = gemini_result[json_start:json_end]
                gemini_data = json.loads(json_str)
                
                # Convert Gemini results to our format
                emotions = []
                for emotion, score in gemini_data['emotions'].items():
                    color = EMOTION_COLORS.get(emotion, '#9E9E9E')
                    emotions.append({
                        'emotion': emotion,
                        'score': float(score) / 100,  # Convert to 0-1 range
                        'color': color
                    })
                
                # Sort by score descending
                emotions.sort(key=lambda x: x['score'], reverse=True)
                return emotions
                
        except Exception as gemini_error:
            print(f"Gemini API error: {gemini_error}")
            # Fallback to BERT model if Gemini fails
            pass
        
        # Fallback to BERT model
        results = emotion_classifier(text)[0]
        emotions = []
        for result in results:
            emotion = result['label']
            score = result['score']
            color = EMOTION_COLORS.get(emotion, '#9E9E9E')
            emotions.append({
                'emotion': emotion,
                'score': float(score),
                'color': color
            })
        return sorted(emotions, key=lambda x: x['score'], reverse=True)
    except Exception as e:
        raise Exception(f"Error analyzing emotion: {str(e)}")

def get_dominant_emotion(emotions: List[Dict]) -> Dict:
    """Get the dominant emotion from analysis results"""
    if emotions:
        return emotions[0]
    return {'emotion': 'neutral', 'score': 0.0, 'color': '#9E9E9E'}

def analyze_text_detailed(text: str) -> Dict:
    """Perform detailed emotion analysis on text with enhanced accuracy"""
    try:
        # Use Gemini for comprehensive text analysis
        comprehensive_prompt = f"""
        Analyze this text comprehensively for emotional content:
        "{text}"
        
        Provide a detailed analysis with:
        1. Overall primary emotion (most dominant)
        2. Secondary emotions (significant but less dominant)
        3. Emotional intensity levels (0-100)
        4. Contextual understanding of the emotional tone
        5. Sentence-by-sentence breakdown if multiple sentences
        
        Return a JSON object in this exact format:
        {{
            "overall_analysis": {{
                "primary_emotion": "emotion_name",
                "primary_score": 85.5,
                "secondary_emotions": ["emotion1", "emotion2"],
                "confidence": 0.95,
                "emotional_intensity": "high|medium|low",
                "tone": "positive|negative|neutral|mixed"
            }},
            "sentence_breakdown": [
                {{
                    "sentence": "sentence_text",
                    "primary_emotion": "emotion_name",
                    "score": 75.0,
                    "explanation": "why this emotion"
                }}
            ],
            "all_emotions": {{
                "emotion1": 85.5,
                "emotion2": 45.2,
                "emotion3": 12.8
            }}
        }}
        """
        
        try:
            response = gemini_model.generate_content(comprehensive_prompt)
            gemini_result = response.text
            
            # Extract JSON from response
            import json
            json_start = gemini_result.find('{')
            json_end = gemini_result.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = gemini_result[json_start:json_end]
                comprehensive_data = json.loads(json_str)
                
                # Convert to our format
                all_emotions = []
                for emotion, score in comprehensive_data['all_emotions'].items():
                    color = EMOTION_COLORS.get(emotion, '#9E9E9E')
                    all_emotions.append({
                        'emotion': emotion,
                        'score': float(score) / 100,  # Convert to 0-1 range
                        'color': color
                    })
                
                # Sort by score descending
                all_emotions.sort(key=lambda x: x['score'], reverse=True)
                
                # Build sentence analysis
                sentence_analysis = []
                for sentence_data in comprehensive_data.get('sentence_breakdown', []):
                    sentence_emotions = analyze_emotion(sentence_data['sentence'])
                    sentence_analysis.append({
                        'text': sentence_data['sentence'],
                        'dominant_emotion': {
                            'emotion': sentence_data['primary_emotion'],
                            'score': float(sentence_data['score']) / 100,
                            'color': EMOTION_COLORS.get(sentence_data['primary_emotion'], '#9E9E9E')
                        },
                        'all_emotions': sentence_emotions,
                        'explanation': sentence_data.get('explanation', '')
                    })
                
                # Build emotion distribution
                emotion_distribution = {}
                for emotion_data in all_emotions:
                    emotion_distribution[emotion_data['emotion']] = emotion_data['score']
                
                return {
                    'overall_emotions': all_emotions,
                    'overall_dominant': all_emotions[0] if all_emotions else {'emotion': 'neutral', 'score': 0.0, 'color': '#9E9E9E'},
                    'sentence_analysis': sentence_analysis,
                    'emotion_distribution': emotion_distribution,
                    'text_length': len(text),
                    'sentence_count': len(sentence_analysis),
                    'analysis_source': 'gemini_enhanced',
                    'confidence': comprehensive_data['overall_analysis']['confidence']
                }
                
        except Exception as gemini_error:
            print(f"Gemini comprehensive analysis error: {gemini_error}")
            # Fallback to improved BERT analysis
            pass
        
        # Fallback: Improved BERT analysis with better sentence handling
        sentences = split_text_into_sentences(text)
        
        # Analyze each sentence with improved logic
        sentence_analysis = []
        for sentence in sentences:
            if len(sentence.strip()) > 5:  # Reduced minimum length for better analysis
                try:
                    emotions = analyze_emotion(sentence.strip())
                    if emotions:  # Only add if we got valid results
                        dominant_emotion = get_dominant_emotion(emotions)
                        sentence_analysis.append({
                            'text': sentence.strip(),
                            'dominant_emotion': dominant_emotion,
                            'all_emotions': emotions
                        })
                except Exception as e:
                    print(f"Error analyzing sentence '{sentence}': {e}")
                    continue
        
        # Analyze overall text with better context
        overall_emotions = analyze_emotion(text)
        overall_dominant = get_dominant_emotion(overall_emotions)
        
        # Calculate emotion distribution
        emotion_distribution = {}
        for emotion_data in overall_emotions:
            emotion_distribution[emotion_data['emotion']] = emotion_data['score']
        
        return {
            'overall_emotions': overall_emotions,
            'overall_dominant': overall_dominant,
            'sentence_analysis': sentence_analysis,
            'emotion_distribution': emotion_distribution,
            'text_length': len(text),
            'sentence_count': len(sentences),
            'analysis_source': 'bert_fallback'
        }
        
    except Exception as e:
        raise Exception(f"Error in detailed text analysis: {str(e)}")

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """Analyze emotion in text"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Empty text provided'}), 400
        
        # Perform analysis
        analysis_result = analyze_text_detailed(text)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'message': 'Emotion analysis completed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analyze-pdf', methods=['POST'])
def analyze_pdf():
    """Analyze emotion in PDF document"""
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file provided'}), 400
        
        pdf_file = request.files['pdf']
        if pdf_file.filename == '':
            return jsonify({'error': 'No PDF file selected'}), 400
        
        # Extract text from PDF
        text = extract_text_from_pdf(pdf_file)
        if not text:
            return jsonify({'error': 'Could not extract text from PDF'}), 400
        
        # Perform analysis
        analysis_result = analyze_text_detailed(text)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'extracted_text': text,
            'message': 'PDF emotion analysis completed successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': True,
        'available_emotions': list(EMOTION_COLORS.keys())
    })

if __name__ == '__main__':
    print("Starting Emotion Detection API...")
    print("Available emotions:", list(EMOTION_COLORS.keys()))
    
    # Use PORT environment variable for cloud deployment
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)