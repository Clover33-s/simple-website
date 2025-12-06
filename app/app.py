from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import random

app = Flask(__name__)

# List of supported languages by code (subset of common ones to ensure stability)
# deep-translator supports many, but let's stick to a robust list.
SUPPORTED_LANGUAGES = [
    'af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca',
    'ceb', 'ny', 'zh-CN', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et',
    'tl', 'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha',
    'haw', 'iw', 'hi', 'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja',
    'jw', 'kn', 'kk', 'km', 'ko', 'ku', 'ky', 'lo', 'la', 'lv', 'lt',
    'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr', 'mn', 'my', 'ne',
    'no', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr',
    'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv',
    'tg', 'ta', 'te', 'th', 'tr', 'uk', 'ur', 'uz', 'vi', 'cy', 'xh',
    'yi', 'yo', 'zu'
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text', '')
    n = int(data.get('n', 3))

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Limit N to prevent timeouts or excessive API usage
    if n > 20:
        n = 20
    if n < 1:
        n = 1

    # Select N unique random languages
    # We exclude 'en' from the intermediate steps if possible to ensure it moves away,
    # but randomness handles this generally.
    random_langs = random.sample(SUPPORTED_LANGUAGES, n)

    current_text = text
    # Assuming start is auto-detected or English, we want to return to English at the end
    # or ideally return to the original language.
    # For this "funny" app, returning to English is usually the goal if the input is English.
    # If the user inputs another language, they might expect it back in that language.
    # Let's try to detect, but GoogleTranslator auto-detect is implicit.
    # We will assume the user wants the final output in English if not specified,
    # OR we can assume the input language is the target language.
    # For simplicity and "Telephone game" tradition: Input (User Lang) -> ... -> Output (User Lang).
    # Since we can't easily detect the source language reliably without an extra call,
    # and the user interface usually implies English for these jokes, we'll default to 'en' for the final step
    # BUT we can try to be smarter.

    # Strategy:
    # 1. Translate Text -> Lang 1
    # 2. Lang 1 -> Lang 2
    # ...
    # N. Lang N-1 -> Lang N
    # Final. Lang N -> English (Assuming the user speaks English as they are using this app)

    # Let's check if the input is empty
    if not current_text.strip():
         return jsonify({'result': ''})

    translator = GoogleTranslator(source='auto', target=random_langs[0])

    try:
        # First hop
        current_text = translator.translate(current_text)

        # Intermediate hops
        for i in range(len(random_langs) - 1):
            source_lang = random_langs[i]
            target_lang = random_langs[i+1]
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            current_text = translator.translate(current_text)

        # Final hop: Back to English
        # (The user prompt didn't specify language, but "funny results" implies reading them in a language you know)
        last_lang = random_langs[-1]
        translator = GoogleTranslator(source=last_lang, target='en')
        final_text = translator.translate(current_text)

        return jsonify({
            'original': text,
            'result': final_text,
            'path': ['Input'] + random_langs + ['English']
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
