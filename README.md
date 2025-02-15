# Masterblog API

## Overview

Masterblog API is a RESTful API built with Flask that allows users to manage blog posts. The application supports the following functionalities:

- Listing all posts
- Adding new posts
- Updating existing posts
- Deleting posts
- Searching posts by title or content

Additionally, the API includes Swagger documentation for easy reference and testing.

## Features

### API Endpoints

#### 1. **List Posts**
   - **Endpoint**: `/api/posts`
   - **Method**: `GET`
   - **Description**: Fetches a list of all blog posts.

#### 2. **Add Post**
   - **Endpoint**: `/api/posts`
   - **Method**: `POST`
   - **Description**: Adds a new blog post.
   - **Input**: JSON object containing `title` and `content`.

#### 3. **Update Post**
   - **Endpoint**: `/api/posts/<id>`
   - **Method**: `PUT`
   - **Description**: Updates an existing blog post by its ID.
   - **Input**: JSON object containing `title` and/or `content`.

#### 4. **Delete Post**
   - **Endpoint**: `/api/posts/<id>`
   - **Method**: `DELETE`
   - **Description**: Deletes a blog post by its ID.

#### 5. **Search Posts**
   - **Endpoint**: `/api/posts/search`
   - **Method**: `GET`
   - **Description**: Searches posts by title or content using query parameters.

### Swagger Documentation

- **URL**: `/api/docs`
- Provides a user-friendly interface to explore and test the API.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```bash
   cd masterblog-api
   ```

3. Set up a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the backend:
   ```bash
   python backend/backend_app.py
   ```

6. Run the frontend:
   ```bash
   python frontend/frontend_app.py
   ```

## Project Structure

```
masterblog-api/
├── backend/
│   ├── static/
│   │   └── masterblog.json
│   └── backend_app.py
├── frontend/
│   ├── static/
│   │   ├── styles.css
│   │   └── main.js
│   ├── templates/
│   │   └── index.html
│   └── frontend_app.py
├── .venv/
├── requirements.txt
└── README.md
```

## Example Request

### Add a New Post

#### Request:
```bash
POST /api/posts HTTP/1.1
Content-Type: application/json

{
  "title": "New Blog Post",
  "content": "This is a new post."
}
```

#### Response:
```json
{
  "id": 3,
  "title": "New Blog Post",
  "content": "This is a new post."
}
```

## Notes

- Ensure the backend is running on `http://127.0.0.1:5002`.
- The Swagger documentation can be accessed at `http://127.0.0.1:5002/api/docs`.

---

Enjoy building and extending the Masterblog API!

