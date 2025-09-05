from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Gemini API configuration
GEMINI_API_KEY = "AIzaSyDnjSxh7OQpNX21g7AJ6wzo8UcguKz0Ja8"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

def call_gemini_api(prompt, max_tokens=2000):
    """Make a request to Gemini API"""
    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.7,
            "topP": 0.8,
            "topK": 40
        }
    }
    
    try:
        response = requests.post(GEMINI_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error calling Gemini API: {str(e)}"

def generate_example_poem(poem_type):
    """Generate an example poem of a specific type"""
    
    if poem_type == "haiku":
        prompt = """
        Write an original haiku (3-line poem with 5-7-5 syllable pattern) about nature.
        
        After the haiku, provide a comprehensive analysis including:
        1. Main themes and imagery
        2. Literary devices used
        3. Seasonal references (kigo) if any
        4. Mood and atmosphere
        5. Traditional haiku elements
        
        Format your response as:
        POEM:
        [haiku text here]
        
        ANALYSIS:
        [detailed analysis here using HTML tags like <h3>, <strong>, <p>]
        """
    
    elif poem_type == "sonnet":
        prompt = """
        Write an original sonnet (14 lines) about love or beauty with proper rhyme scheme.
        
        After the sonnet, provide a comprehensive analysis including:
        1. Main themes and development
        2. Rhyme scheme analysis
        3. Literary devices used
        4. Volta (turn) identification
        5. Meter and rhythm
        
        Format your response as:
        POEM:
        [sonnet text here]
        
        ANALYSIS:
        [detailed analysis here using HTML tags like <h3>, <strong>, <p>]
        """
    
    elif poem_type == "limerick":
        prompt = """
        Write an original limerick (5 lines with AABBA rhyme scheme) that is humorous.
        
        After the limerick, provide a comprehensive analysis including:
        1. Humor techniques used
        2. Rhyme scheme analysis (AABBA)
        3. Rhythm and meter
        4. Literary devices
        5. Traditional limerick structure
        
        Format your response as:
        POEM:
        [limerick text here]
        
        ANALYSIS:
        [detailed analysis here using HTML tags like <h3>, <strong>, <p>]
        """
    
    elif poem_type == "free_verse":
        prompt = """
        Write an original free verse poem (6-10 lines) about urban life with no regular rhyme or meter.
        
        After the poem, provide a comprehensive analysis including:
        1. Main themes and imagery
        2. Literary devices used
        3. Line breaks and structure
        4. Tone and mood
        5. Modern poetry techniques
        
        Format your response as:
        POEM:
        [poem text here]
        
        ANALYSIS:
        [detailed analysis here using HTML tags like <h3>, <strong>, <p>]
        """
    
    else:
        return "Invalid poem type"
    
    return call_gemini_api(prompt)

def analyze_poem(poem_text):
    """Analyze a user-provided poem"""
    prompt = f"""
    Please provide a comprehensive literary analysis of the following poem:
    
    {poem_text}
    
    Include in your analysis:
    1. Main themes and their development
    2. Literary devices (metaphor, simile, imagery, symbolism, alliteration, etc.)
    3. Tone and mood analysis
    4. Structure and form (rhyme scheme, meter, stanza structure)
    5. Key interpretations and deeper meanings
    6. Historical/cultural context if relevant
    7. Overall assessment of the poem's effectiveness
    
    Be thorough but accessible in your analysis.
    
    IMPORTANT: Format your response using HTML tags for structure:
    - Use <h3> for section headings
    - Use <strong> for emphasis/bold text
    - Use <em> for italics
    - Use <p> for paragraphs
    - Do NOT use markdown syntax like ** or ##
    """
    
    return call_gemini_api(prompt)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_poem', methods=['POST'])
def analyze_user_poem():
    """Analyze a user-provided poem"""
    try:
        data = request.get_json()
        poem_text = data.get('poem', '').strip()
        
        if not poem_text:
            return jsonify({"success": False, "error": "Please provide a poem to analyze"})
        
        analysis = analyze_poem(poem_text)
        return jsonify({"success": True, "analysis": analysis})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/generate_example', methods=['POST'])
def generate_example():
    """Generate and analyze an example poem of specific type"""
    try:
        data = request.get_json()
        poem_type = data.get('type', 'haiku')
        result = generate_example_poem(poem_type)
        return jsonify({"success": True, "content": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)