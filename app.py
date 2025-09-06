
from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Gemini Flash API configuration
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

def call_gemini_flash(prompt):
    """Call Gemini Flash API"""
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "maxOutputTokens": 2000,
            "temperature": 0.7
        }
    }
    
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
        elif response.status_code == 429:
            return "API quota exceeded. Please try again later."
        else:
            return f"API Error: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze_poem', methods=['POST'])
def analyze_poem():
    try:
        data = request.get_json()
        poem = data.get('poem', '').strip()
        
        if not poem:
            return jsonify({"success": False, "error": "Please provide a poem to analyze"})
        
        prompt = f"""Analyze this poem in detail:

{poem}

Provide analysis covering:
1. Main themes and meanings
2. Literary devices (metaphors, imagery, symbolism, etc.)
3. Tone and mood
4. Structure and form
5. Overall interpretation

Format with HTML tags: <h3> for headings, <strong> for emphasis, <p> for paragraphs."""
        
        analysis = call_gemini_flash(prompt)
        return jsonify({"success": True, "analysis": analysis})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/generate_example', methods=['POST'])
def generate_example():
    try:
        data = request.get_json()
        poem_type = data.get('type', 'haiku')
        
        if poem_type == 'haiku':
            prompt = """Write a haiku (3 lines, 5-7-5 syllables) about nature.

After the haiku, provide analysis covering:
- Imagery and nature themes
- Seasonal elements
- Mood and atmosphere
- Traditional haiku techniques

Format as:
POEM:
[haiku here]

ANALYSIS:
[analysis with HTML tags: <h3> for headings, <strong> for emphasis, <p> for paragraphs]"""

        elif poem_type == 'sonnet':
            prompt = """Write a 14-line sonnet about love or beauty with proper rhyme scheme.

After the sonnet, provide analysis covering:
- Rhyme scheme pattern
- Themes and development
- Literary devices
- Volta (turn) and structure

Format as:
POEM:
[sonnet here]

ANALYSIS:
[analysis with HTML tags: <h3> for headings, <strong> for emphasis, <p> for paragraphs]"""

        elif poem_type == 'limerick':
            prompt = """Write a humorous limerick (5 lines, AABBA rhyme).

After the limerick, provide analysis covering:
- Humor techniques
- Rhyme and rhythm
- Story structure
- Traditional limerick elements

Format as:
POEM:
[limerick here]

ANALYSIS:
[analysis with HTML tags: <h3> for headings, <strong> for emphasis, <p> for paragraphs]"""

        elif poem_type == 'free_verse':
            prompt = """Write a free verse poem (6-10 lines) about city life with no regular rhyme.

After the poem, provide analysis covering:
- Modern themes
- Line breaks and structure
- Imagery and language
- Free verse techniques

Format as:
POEM:
[poem here]

ANALYSIS:
[analysis with HTML tags: <h3> for headings, <strong> for emphasis, <p> for paragraphs]"""

        else:
            return jsonify({"success": False, "error": "Invalid poem type"})
        
        result = call_gemini_flash(prompt)
        return jsonify({"success": True, "content": result})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("Starting Poetry Analysis Studio...")
    print("Access the app at: http://localhost:8000")
    app.run(host='0.0.0.0', port=8000, debug=True)