
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)  # Применение CORS ко всем маршрутам

app = Flask(__name__)
CORS(app, resources={r"/parse": {"origins": "http://localhost:5000"}})

from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    Doc
)

app = Flask(__name__)

# Инициализация компонентов Natasha
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse():
    data = request.get_json()
    text = data['text']

    # Обработка текста с помощью Natasha
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.parse_syntax(syntax_parser)

    # Формирование результата
    result = []
    for token in doc.tokens:
        result.append({
            'text': token.text,
            'lemma': token.lemma,
            'pos': token.pos,
            'feats': token.feats,
            'head_id': token.head_id,
            'rel': token.rel
        })

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
