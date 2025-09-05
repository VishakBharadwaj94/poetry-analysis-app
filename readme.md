# Poetry Analysis Studio

A Flask web application that analyzes poetry using Google's Gemini AI. Users can either submit their own poems for analysis or generate example poems in different styles (Haiku, Sonnet, Limerick, Free Verse) with detailed literary analysis.

## Features

- **Poem Analysis**: Submit your own poems for comprehensive literary analysis
- **Example Generation**: Generate example poems in 4 different styles:
  - Haiku (3-line, 5-7-5 syllable pattern)
  - Sonnet (14-line structured poem)
  - Limerick (5-line humorous poem)
  - Free Verse (modern unstructured poetry)
- **Literary Analysis**: Detailed analysis including themes, devices, structure, and interpretation
- **Clean UI**: Modern, responsive design with smooth scrolling

## Prerequisites

- Python 3.7+
- Gemini API key from Google AI Studio

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vishakbharadwaj94/poetry-analysis-app.git
cd poetry-analysis-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Update the Gemini API key in `app.py`:
```python
GEMINI_API_KEY = "your-api-key-here"
```

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to `http://127.0.0.1:5000`

3. Either:
   - Paste your own poem in the text area and click "Analyze Poem"
   - Choose a poem type button to generate an example with analysis

## API Endpoints

- `GET /` - Main application page
- `POST /analyze_poem` - Analyze user-submitted poem
- `POST /generate_example` - Generate example poem of specified type

## Technologies Used

- **Backend**: Flask, Python
- **AI**: Google Gemini API
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Custom CSS with gradients and animations

## Configuration

The app uses the Gemini 1.5 Flash model with the following parameters:
- Max tokens: 2000
- Temperature: 0.7
- Top P: 0.8
- Top K: 40

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Google Gemini AI for poetry generation and analysis
- Flask framework for web application structure