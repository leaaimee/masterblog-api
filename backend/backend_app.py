from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint


app = Flask(__name__)
CORS(app)


SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "Masterblog API"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
@app.route('/api/posts/', methods=['GET', 'POST'])
def handle_posts():
    """Handles listing and adding posts"""
    if request.method == 'GET':
        return jsonify(POSTS)
    if request.method == 'POST':
        data = request.get_json()
        if not data or "title" not in data or "content" not in data:
            return jsonify({"error": "Missing title or content"}), 400
        new_id = max(post['id'] for post in POSTS) + 1 if POSTS else 1
        new_post = {
            "id": new_id,
            "title": data["title"],
            "content": data["content"]
        }
        POSTS.append(new_post)
        return jsonify(new_post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """ Deletes a post by ID """
    post_to_delete = next((post for post in POSTS if post['id'] == id), None)
    if not post_to_delete:
        return jsonify({"error": f"Post with id {id} not found."}), 404
    POSTS.remove(post_to_delete)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_posts(id):
    """ Updates a post by ID """
    data = request.get_json()
    post = next((post for post in POSTS if post['id'] == id), None)
    if not post:
        return jsonify({"error": f"Post with id {id} not found."}), 404
    post['title'] = data.get('title', post['title'])
    post['content'] = data.get('content', post['content'])
    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search_post():
    """ Searches posts by title or content """
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()
    matching_posts = [
        post for post in POSTS
        if (title_query in post['title'].lower()) or (content_query in post['content'].lower())
    ]
    return jsonify(matching_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
