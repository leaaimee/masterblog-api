from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import json
from pathlib import Path

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Masterblog API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

DATA_FILE = Path("posts.json")

def load_posts():
    """Load posts from the JSON storage file"""
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_posts(posts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2)

@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    """Handles listing, adding, searching, and sorting posts"""
    posts = load_posts()

    if request.method == 'GET':
        title_query = request.args.get('title', '').lower()
        content_query = request.args.get('content', '').lower()
        sort_field = request.args.get('sort')
        direction = request.args.get('direction', 'asc').lower()

        posts_to_return = [
            p for p in posts
            if (title_query in p['title'].lower())
            or (content_query in p['content'].lower())
            or (title_query in p.get('author', '').lower())
            or (content_query in p.get('date', ''))
        ] if (title_query or content_query) else posts.copy()

        if sort_field:
            if sort_field not in ('title', 'content', 'author', 'date'):
                return jsonify({'error': 'Invalid sort field. Use "title", "content", "author", or "date".'}), 400
            reverse = direction == 'desc'
            if sort_field == 'date':
                posts_to_return.sort(
                    key=lambda p: datetime.strptime(p['date'], "%Y-%m-%d"),
                    reverse=reverse
                )
            else:
                posts_to_return.sort(
                    key=lambda p: p[sort_field].lower(),
                    reverse=reverse
                )

        return jsonify(posts_to_return), 200

    if request.method == 'POST':
        data = request.get_json()
        if not data or "title" not in data or "content" not in data:
            return jsonify({"error": "Missing title or content"}), 400

        new_id = max((post['id'] for post in posts), default=0) + 1
        new_post = {
            "id": new_id,
            "title": data["title"],
            "content": data["content"],
            "author": data.get("author", "Unknown"),
            "date": data.get("date", datetime.now().strftime("%Y-%m-%d"))
        }

        posts.append(new_post)
        save_posts(posts)
        return jsonify(new_post), 201

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Deletes a post by ID"""
    posts = load_posts()
    post_to_delete = next((post for post in posts if post['id'] == id), None)
    if not post_to_delete:
        return jsonify({"error": f"Post with id {id} not found."}), 404
    posts.remove(post_to_delete)
    save_posts(posts)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200

@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_posts(id):
    """Updates a post by ID"""
    posts = load_posts()
    data = request.get_json()
    post = next((post for post in posts if post['id'] == id), None)
    if not post:
        return jsonify({"error": f"Post with id {id} not found."}), 404

    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])
    post['author'] = data.get('author', post['author'])
    post['date'] = data.get('date', post['date'])

    save_posts(posts)
    return jsonify(post), 200

@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """Searches posts by title, content, author, or date"""
    posts = load_posts()
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    matching_posts = [
        post for post in posts
        if (title_query in post['title'].lower())
        or (content_query in post['content'].lower())
        or (title_query in post.get('author', '').lower())
        or (content_query in post.get('date', ''))
    ]
    return jsonify(matching_posts), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
