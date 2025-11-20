from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv
import hashlib
import secrets
from sqlalchemy.orm import scoped_session
from models import (init_db, get_session, User, Token, Post, Course, Space, Member, Event,
                   Job, Escrow, Milestone, Dispute, UserRole, KYCStatus, BadgeType,
                   JobStatus, EscrowStatus, ServiceType, DisputeStatus)

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
        role = data.get('role', 'company')  # Default to company
        
        if not name or not email or not password:
            return jsonify({'message': 'All fields are required'}), 400
        
        # Validate role
        try:
            user_role = UserRole(role)
        except ValueError:
            return jsonify({'message': 'Invalid role. Must be: company or expert'}), 400
        
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
            avatar=avatar,
            role=user_role,
            kyc_status=KYCStatus.PENDING,
            badge=BadgeType.TRIAL,
            trust_score=0,
            company_name=data.get('company_name'),
            tax_id=data.get('tax_id'),
            bio=data.get('bio'),
            phone=data.get('phone')
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

# Job / Task Management Routes
@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all jobs (filtered by user role and status)"""
    session = db_session()
    try:
        # TODO: Add authentication middleware to get current user
        # For now, return all approved jobs
        jobs = session.query(Job).filter_by(approved_by_admin=True).order_by(Job.created_at.desc()).all()
        return jsonify({'jobs': [job.to_dict() for job in jobs]})
    except Exception as e:
        return jsonify({'message': f'Error fetching jobs: {str(e)}'}), 500

@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job/task"""
    session = db_session()
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['title', 'description', 'service_type', 'budget', 'client_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        # Validate service type
        try:
            service_type = ServiceType(data['service_type'])
        except ValueError:
            return jsonify({'message': 'Invalid service type'}), 400
        
        # Create job
        job = Job(
            title=data['title'],
            description=data['description'],
            service_type=service_type,
            budget=data['budget'],
            deliverables=data.get('deliverables'),
            deadline=datetime.fromisoformat(data['deadline']) if data.get('deadline') else None,
            client_id=data['client_id'],
            expert_id=data.get('expert_id'),
            status=JobStatus.DRAFT
        )
        
        session.add(job)
        session.commit()
        
        return jsonify({
            'message': 'Job created successfully',
            'job': job.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error creating job: {str(e)}'}), 500

@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get a specific job by ID"""
    session = db_session()
    try:
        job = session.query(Job).filter_by(id=job_id).first()
        if not job:
            return jsonify({'message': 'Job not found'}), 404
        
        # Include related data
        job_data = job.to_dict()
        if job.escrow:
            job_data['escrow'] = job.escrow.to_dict()
        if job.milestones:
            job_data['milestones'] = [m.to_dict() for m in job.milestones]
        
        return jsonify({'job': job_data})
    except Exception as e:
        return jsonify({'message': f'Error fetching job: {str(e)}'}), 500

@app.route('/api/jobs/<int:job_id>/submit', methods=['POST'])
def submit_job_for_approval(job_id):
    """Submit job for admin approval"""
    session = db_session()
    try:
        job = session.query(Job).filter_by(id=job_id).first()
        if not job:
            return jsonify({'message': 'Job not found'}), 404
        
        if job.status != JobStatus.DRAFT:
            return jsonify({'message': 'Job already submitted'}), 400
        
        job.status = JobStatus.PENDING_APPROVAL
        session.commit()
        
        return jsonify({
            'message': 'Job submitted for approval',
            'job': job.to_dict()
        })
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error submitting job: {str(e)}'}), 500

@app.route('/api/jobs/<int:job_id>/approve', methods=['POST'])
def approve_job(job_id):
    """Admin approves a job"""
    session = db_session()
    try:
        # TODO: Add admin authentication check
        
        job = session.query(Job).filter_by(id=job_id).first()
        if not job:
            return jsonify({'message': 'Job not found'}), 404
        
        job.approved_by_admin = True
        job.status = JobStatus.ACTIVE
        session.commit()
        
        return jsonify({
            'message': 'Job approved successfully',
            'job': job.to_dict()
        })
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error approving job: {str(e)}'}), 500

# Escrow Routes
@app.route('/api/escrow', methods=['POST'])
def create_escrow():
    """Create escrow contract for a job"""
    session = db_session()
    try:
        data = request.json
        
        job_id = data.get('job_id')
        if not job_id:
            return jsonify({'message': 'job_id is required'}), 400
        
        job = session.query(Job).filter_by(id=job_id).first()
        if not job:
            return jsonify({'message': 'Job not found'}), 404
        
        if job.escrow:
            return jsonify({'message': 'Escrow already exists for this job'}), 400
        
        # Calculate platform fee based on service type
        platform_fee_percent = {
            ServiceType.DIRECT_TRUST: 0.02,
            ServiceType.GUIDED_TRUST: 0.07,
            ServiceType.DELEGATED_TRUST: 0.15
        }
        
        fee_percent = platform_fee_percent.get(job.service_type, 0.05)
        platform_fee = float(job.budget) * fee_percent
        
        escrow = Escrow(
            job_id=job.id,
            total_amount=job.budget,
            platform_fee=platform_fee,
            status=EscrowStatus.CREATED
        )
        
        session.add(escrow)
        session.commit()
        
        return jsonify({
            'message': 'Escrow created successfully',
            'escrow': escrow.to_dict()
        }), 201
        
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error creating escrow: {str(e)}'}), 500

# Admin endpoints
@app.route('/api/admin/users', methods=['GET'])
def admin_get_users():
    """Get all users with filtering options"""
    session = db_session()
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'No token provided'}), 401
        
        token_value = auth_header.split(' ')[1]
        token = session.query(Token).filter_by(token=token_value).first()
        
        if not token:
            return jsonify({'message': 'Invalid token'}), 401
        
        admin = session.query(User).filter_by(id=token.user_id).first()
        if not admin or admin.role != UserRole.ADMIN:
            return jsonify({'message': 'Admin access required'}), 403
        
        # Get query parameters
        role = request.args.get('role')
        kyc_status = request.args.get('kyc_status')
        
        query = session.query(User)
        
        if role:
            query = query.filter_by(role=UserRole[role.upper()])
        if kyc_status:
            query = query.filter_by(kyc_status=KYCStatus[kyc_status.upper()])
        
        users = query.all()
        
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching users: {str(e)}'}), 500

@app.route('/api/admin/kyc/<int:user_id>/verify', methods=['POST'])
def admin_verify_kyc(user_id):
    """Verify a user's KYC"""
    session = db_session()
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'No token provided'}), 401
        
        token_value = auth_header.split(' ')[1]
        token = session.query(Token).filter_by(token=token_value).first()
        
        if not token:
            return jsonify({'message': 'Invalid token'}), 401
        
        admin = session.query(User).filter_by(id=token.user_id).first()
        if not admin or admin.role != UserRole.ADMIN:
            return jsonify({'message': 'Admin access required'}), 403
        
        # Get user
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        # Update KYC status
        user.kyc_status = KYCStatus.VERIFIED
        user.kyc_verified_at = datetime.utcnow()
        session.commit()
        
        return jsonify({
            'message': 'KYC verified successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error verifying KYC: {str(e)}'}), 500

@app.route('/api/admin/kyc/<int:user_id>/reject', methods=['POST'])
def admin_reject_kyc(user_id):
    """Reject a user's KYC"""
    session = db_session()
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'No token provided'}), 401
        
        token_value = auth_header.split(' ')[1]
        token = session.query(Token).filter_by(token=token_value).first()
        
        if not token:
            return jsonify({'message': 'Invalid token'}), 401
        
        admin = session.query(User).filter_by(id=token.user_id).first()
        if not admin or admin.role != UserRole.ADMIN:
            return jsonify({'message': 'Admin access required'}), 403
        
        # Get user
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404
        
        data = request.get_json()
        reason = data.get('reason', 'KYC documents rejected')
        
        # Update KYC status
        user.kyc_status = KYCStatus.REJECTED
        session.commit()
        
        return jsonify({
            'message': 'KYC rejected successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error rejecting KYC: {str(e)}'}), 500

@app.route('/api/admin/jobs/pending', methods=['GET'])
def admin_get_pending_jobs():
    """Get all jobs pending approval"""
    session = db_session()
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'No token provided'}), 401
        
        token_value = auth_header.split(' ')[1]
        token = session.query(Token).filter_by(token=token_value).first()
        
        if not token:
            return jsonify({'message': 'Invalid token'}), 401
        
        admin = session.query(User).filter_by(id=token.user_id).first()
        if not admin or admin.role != UserRole.ADMIN:
            return jsonify({'message': 'Admin access required'}), 403
        
        # Get pending jobs
        jobs = session.query(Job).filter_by(
            status=JobStatus.PENDING_APPROVAL
        ).all()
        
        return jsonify({
            'jobs': [job.to_dict() for job in jobs]
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching pending jobs: {str(e)}'}), 500

@app.route('/api/admin/disputes', methods=['GET'])
def admin_get_disputes():
    """Get all disputes"""
    session = db_session()
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'No token provided'}), 401
        
        token_value = auth_header.split(' ')[1]
        token = session.query(Token).filter_by(token=token_value).first()
        
        if not token:
            return jsonify({'message': 'Invalid token'}), 401
        
        admin = session.query(User).filter_by(id=token.user_id).first()
        if not admin or admin.role != UserRole.ADMIN:
            return jsonify({'message': 'Admin access required'}), 403
        
        # Get query parameters
        status = request.args.get('status')
        
        query = session.query(Dispute)
        
        if status:
            query = query.filter_by(status=DisputeStatus[status.upper()])
        
        disputes = query.all()
        
        return jsonify({
            'disputes': [dispute.to_dict() for dispute in disputes]
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error fetching disputes: {str(e)}'}), 500

@app.route('/api/admin/disputes/<int:dispute_id>/assign', methods=['POST'])
def admin_assign_dispute(dispute_id):
    """Assign an arbitrator to a dispute"""
    session = db_session()
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'No token provided'}), 401
        
        token_value = auth_header.split(' ')[1]
        token = session.query(Token).filter_by(token=token_value).first()
        
        if not token:
            return jsonify({'message': 'Invalid token'}), 401
        
        admin = session.query(User).filter_by(id=token.user_id).first()
        if not admin or admin.role != UserRole.ADMIN:
            return jsonify({'message': 'Admin access required'}), 403
        
        # Get dispute
        dispute = session.query(Dispute).filter_by(id=dispute_id).first()
        if not dispute:
            return jsonify({'message': 'Dispute not found'}), 404
        
        data = request.get_json()
        arbitrator_id = data.get('arbitrator_id')
        
        if not arbitrator_id:
            return jsonify({'message': 'Arbitrator ID is required'}), 400
        
        # Verify arbitrator exists and has correct role
        arbitrator = session.query(User).filter_by(id=arbitrator_id).first()
        if not arbitrator or arbitrator.role != UserRole.ARBITRATOR:
            return jsonify({'message': 'Invalid arbitrator'}), 400
        
        # Assign arbitrator
        dispute.arbitrator_id = arbitrator_id
        dispute.status = DisputeStatus.IN_REVIEW
        session.commit()
        
        return jsonify({
            'message': 'Arbitrator assigned successfully',
            'dispute': dispute.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error assigning arbitrator: {str(e)}'}), 500

@app.route('/api/admin/disputes/<int:dispute_id>/resolve', methods=['POST'])
def admin_resolve_dispute(dispute_id):
    """Resolve a dispute"""
    session = db_session()
    try:
        # Get auth token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'message': 'No token provided'}), 401
        
        token_value = auth_header.split(' ')[1]
        token = session.query(Token).filter_by(token=token_value).first()
        
        if not token:
            return jsonify({'message': 'Invalid token'}), 401
        
        admin = session.query(User).filter_by(id=token.user_id).first()
        if not admin or admin.role != UserRole.ADMIN:
            return jsonify({'message': 'Admin access required'}), 403
        
        # Get dispute
        dispute = session.query(Dispute).filter_by(id=dispute_id).first()
        if not dispute:
            return jsonify({'message': 'Dispute not found'}), 404
        
        data = request.get_json()
        resolution = data.get('resolution')
        winner = data.get('winner')  # 'client' or 'expert'
        
        if not resolution or not winner:
            return jsonify({'message': 'Resolution and winner are required'}), 400
        
        # Update dispute
        dispute.status = DisputeStatus.RESOLVED
        dispute.resolution = resolution
        dispute.resolved_at = datetime.utcnow()
        
        # Update escrow based on resolution
        escrow = session.query(Escrow).filter_by(job_id=dispute.job_id).first()
        if escrow:
            if winner == 'client':
                escrow.status = EscrowStatus.REFUNDED
            elif winner == 'expert':
                escrow.status = EscrowStatus.RELEASED
                escrow.released_at = datetime.utcnow()
        
        session.commit()
        
        return jsonify({
            'message': 'Dispute resolved successfully',
            'dispute': dispute.to_dict()
        }), 200
        
    except Exception as e:
        session.rollback()
        return jsonify({'message': f'Error resolving dispute: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

