from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
import hashlib
import secrets
from sqlalchemy.orm import scoped_session
from models import init_db, get_session, User, Token, Post, Course, Space, Member, Event

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg://trusthub_user:trusthub_pass@localhost:5432/trusthub_db')
engine = init_db(DATABASE_URL)
db_session = scoped_session(lambda: get_session(engine))

# Helper functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    return secrets.token_urlsafe(32)

def get_user_initials(name):
    parts = name.split()
    if len(parts) > 1:
        return (parts[0][0] + parts[1][0]).upper()
    return (parts[0][0] + (parts[0][1] if len(parts[0]) > 1 else '')).upper()

# Cleanup
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# Authentication Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    session = db_session()
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if not name or not email or not password:
            return jsonify({'message': 'All fields are required'}), 400
        
        # Check if user already exists
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            return jsonify({'message': 'Email already registered'}), 400
        
        # Create new user
        hashed_password = hash_password(password)
        avatar = get_user_initials(name)
        
        user = User(
            name=name,
            email=email,
            password=hashed_password,
            avatar=avatar
        )
        
        session.add(user)
        session.commit()
        
        # Generate token
        token_str = generate_token()
        token = Token(token=token_str, user_id=user.id)
        session.add(token)
        session.commit()
        
        return jsonify({
            'user': user.to_dict(),
            'token': token_str,
            'message': 'Registration successful'
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error during registration: {str(e)}'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    session = db_session()
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'message': 'Email and password are required'}), 400
        
        # Find user
        user = session.query(User).filter_by(email=email).first()
        
        if not user or user.password != hash_password(password):
            return jsonify({'message': 'Invalid email or password'}), 401
        
        # Generate token
        token_str = generate_token()
        token = Token(token=token_str, user_id=user.id)
        session.add(token)
        session.commit()
        
        return jsonify({
            'user': user.to_dict(),
            'token': token_str,
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error during login: {str(e)}'}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session = db_session()
    try:
        token_str = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if token_str:
            token = session.query(Token).filter_by(token=token_str).first()
            if token:
                session.delete(token)
                session.commit()
        
        return jsonify({'message': 'Logout successful'}), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error during logout: {str(e)}'}), 500

# Routes
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/posts', methods=['GET'])
def get_posts():
    session = db_session()
    try:
        posts = session.query(Post).order_by(Post.created_at.desc()).all()
        return jsonify({'posts': [post.to_dict() for post in posts]})
    except Exception as e:
        return jsonify({'message': f'Error fetching posts: {str(e)}'}), 500

@app.route('/api/courses', methods=['GET'])
def get_courses():
    session = db_session()
    try:
        courses = session.query(Course).all()
        return jsonify({'courses': [course.to_dict() for course in courses]})
    except Exception as e:
        return jsonify({'message': f'Error fetching courses: {str(e)}'}), 500

@app.route('/api/spaces', methods=['GET'])
def get_spaces():
    session = db_session()
    try:
        spaces = session.query(Space).all()
        return jsonify({'spaces': [space.to_dict() for space in spaces]})
    except Exception as e:
        return jsonify({'message': f'Error fetching spaces: {str(e)}'}), 500

@app.route('/api/members', methods=['GET'])
def get_members():
    session = db_session()
    try:
        members = session.query(Member).all()
        return jsonify({'members': [member.to_dict() for member in members]})
    except Exception as e:
        return jsonify({'message': f'Error fetching members: {str(e)}'}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    session = db_session()
    try:
        events = session.query(Event).all()
        return jsonify({'events': [event.to_dict() for event in events]})
    except Exception as e:
        return jsonify({'message': f'Error fetching events: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

