from flask import Flask, request, jsonify
from analyzer import analyze_article
from database import init_db, log_analysis

app = Flask(__name__)

init_db()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json(force=True)
    article = data.get('article', '')
    result = analyze_article(article)
    log_analysis(article, result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
