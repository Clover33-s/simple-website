from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import random

app = Flask(__name__)

# Get supported languages dynamically
SUPPORTED_LANGUAGES_DICT = GoogleTranslator().get_supported_languages(as_dict=True)
SUPPORTED_LANGUAGES_CODES = list(SUPPORTED_LANGUAGES_DICT.values())

@app.route('/')
def index():
    # Pass languages to the template for dropdowns
    # Sort by language name for better UX
    sorted_langs = dict(sorted(SUPPORTED_LANGUAGES_DICT.items()))
    return render_template('index.html', languages=sorted_langs)

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text', '')
    n = int(data.get('n', 3))
    start_lang = data.get('start_lang', 'auto')
    end_lang = data.get('end_lang', 'en')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Limit N
    if n > 20: n = 20
    if n < 1: n = 1

    # Select N unique random languages
    random_langs = random.sample(SUPPORTED_LANGUAGES_CODES, n)

    current_text = text
    path_codes = []

    # If start_lang is not auto, we can track it better in the path
    if start_lang == 'auto':
        path_codes.append('Auto')
    else:
        path_codes.append(start_lang)

    try:
        # Hop 1: Start -> Random 1
        translator = GoogleTranslator(source=start_lang, target=random_langs[0])
        current_text = translator.translate(current_text)
        path_codes.append(random_langs[0])

        # Intermediate hops
        for i in range(len(random_langs) - 1):
            source = random_langs[i]
            target = random_langs[i+1]
            translator = GoogleTranslator(source=source, target=target)
            current_text = translator.translate(current_text)
            path_codes.append(target)

        # Final Hop: Random N -> End Lang
        last_lang = random_langs[-1]
        translator = GoogleTranslator(source=last_lang, target=end_lang)
        final_text = translator.translate(current_text)
        path_codes.append(end_lang)

        return jsonify({
            'original': text,
            'result': final_text,
            'path': path_codes
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
