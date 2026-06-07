import logging
import os
import sys
from flask import Flask, request, jsonify
from requests import get, post, timeout
from typing import Dict, Any

logging.basicConfig(level=os.environ.get('LOG_LEVEL','WARNING'), stream=sys.stderr)
log = logging.getLogger(__name__)

def fetch(url: str, timeout: int = 10) -> Dict:
    try:
        response = get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        log.error('failed: %s', exc)
        return None

def post_request(url: str, data: Dict, timeout: int = 10) -> Dict:
    try:
        response = post(url, json=data, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        log.error('failed: %s', exc)
        return None

def retry(func, max_attempts: int = 3, sleep_factor: int = 2):
    def wrapper(*args, **kwargs):
        attempt = 0
        while attempt < max_attempts:
            result = func(*args, **kwargs)
            if result is not None:
                return result
            time.sleep(sleep_factor * (2 ** attempt))
            attempt += 1
        log.error('max attempts reached')
        return None

    return wrapper

def create_app() -> Flask:
    app = Flask(__name__)
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'})

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'error': 'not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({'error': 'internal server error'}), 500
    return app

def main() -> int:
    api_key = os.environ.get('OPENAI_API_KEY') or sys.exit('OPENAI_API_KEY not set')
    flask_app = create_app()

    @flask_app.route('/search', methods=['GET'])
    def search():
        query = request.args.get('query')
        limit = int(request.args.get('limit', 10))
        url = f'https://api.nytimes.com/svc/search/v2/articles.json?query={query}&limit={limit}'
        response = fetch(url)
        if response is None:
            return jsonify({'error': 'failed to fetch data'}), 500
        return jsonify(response)

    @flask_app.route('/search', methods=['POST'])
    def search_post():
        query = request.json.get('query')
        limit = int(request.json.get('limit', 10))
        url = f'https://api.nytimes.com/svc/search/v2/articles.json?query={query}&limit={limit}'
        response = post_request(url, data=request.json)
        if response is None:
            return jsonify({'error': 'failed to fetch data'}), 500
        return jsonify(response)

    @flask_app.route('/health', methods=['GET'])
    def health_get():
        return jsonify({'status': 'ok'})

    @flask_app.errorhandler(404)
    def page_not_found_get(e):
        return jsonify({'error': 'not found'}), 404

    @flask_app.errorhandler(500)
    def internal_server_error_get(e):
        return jsonify({'error': 'internal server error'}), 500
    return flask_app.run(debug=os.environ.get('FLASK_DEBUG','false'))

if __name__ == '__main__':
    sys.exit(main())