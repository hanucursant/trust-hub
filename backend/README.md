# Flask Backend

Python Flask backend for the Trust Hub application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python app.py
```

The server will start on http://localhost:5000

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/posts` - Get all posts
- `GET /api/posts/<id>` - Get specific post
- `POST /api/posts` - Create new post
- `GET /api/courses` - Get all courses
- `GET /api/courses/<id>` - Get specific course
- `GET /api/spaces` - Get all spaces
- `GET /api/members` - Get all members
- `GET /api/events` - Get all events
- `GET /api/user/profile` - Get user profile
