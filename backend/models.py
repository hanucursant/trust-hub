from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table, Enum as SQLEnum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum

Base = declarative_base()

# Enums for status management
class UserRole(enum.Enum):
    COMPANY = "company"
    EXPERT = "expert"
    ADMIN = "admin"
    ARBITRATOR = "arbitrator"

class KYCStatus(enum.Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

class BadgeType(enum.Enum):
    TRIAL = "trial"
    RECOMMENDED = "recommended"
    TRUSTED = "trusted"
    CERTIFIED = "certified"

class JobStatus(enum.Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    DELIVERED = "delivered"
    DISPUTED = "disputed"
    COMPLETED = "completed"
    CLOSED = "closed"

class EscrowStatus(enum.Enum):
    CREATED = "created"
    FUNDED = "funded"
    HELD = "held"
    RELEASED = "released"
    REFUNDED = "refunded"
    DISPUTED = "disputed"

class ServiceType(enum.Enum):
    DIRECT_TRUST = "direct_trust"
    GUIDED_TRUST = "guided_trust"
    DELEGATED_TRUST = "delegated_trust"

class DisputeStatus(enum.Enum):
    OPEN = "open"
    UNDER_REVIEW = "under_review"
    RESOLVED = "resolved"
    CLOSED = "closed"

# Association tables
space_members = Table('space_members', Base.metadata,
    Column('space_id', Integer, ForeignKey('spaces.id')),
    Column('member_id', Integer, ForeignKey('members.id'))
)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    avatar = Column(String(10), nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.COMPANY)
    kyc_status = Column(SQLEnum(KYCStatus), default=KYCStatus.PENDING)
    badge = Column(SQLEnum(BadgeType), default=BadgeType.TRIAL)
    trust_score = Column(Integer, default=0)
    company_name = Column(String(200))
    tax_id = Column(String(50))  # CUI/CIF for Romanian companies
    bio = Column(Text)
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    stripe_account_id = Column(String(100))  # For Stripe Connect
    recommended_by_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recommended_by = relationship('User', remote_side=[id], backref='recommendations')
    jobs_created = relationship('Job', foreign_keys='Job.client_id', back_populates='client')
    jobs_assigned = relationship('Job', foreign_keys='Job.expert_id', back_populates='expert')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'avatar': self.avatar,
            'role': self.role.value if self.role else None,
            'kyc_status': self.kyc_status.value if self.kyc_status else None,
            'badge': self.badge.value if self.badge else None,
            'trust_score': self.trust_score,
            'company_name': self.company_name,
            'bio': self.bio,
            'is_active': self.is_active
        }

class Token(Base):
    __tablename__ = 'tokens'
    
    id = Column(Integer, primary_key=True)
    token = Column(String(100), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', backref='tokens')

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    service_type = Column(SQLEnum(ServiceType), nullable=False)
    status = Column(SQLEnum(JobStatus), default=JobStatus.DRAFT)
    budget = Column(Numeric(10, 2), nullable=False)
    deadline = Column(DateTime)
    deliverables = Column(Text)  # JSON stored as text
    client_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    expert_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    approved_by_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = relationship('User', foreign_keys=[client_id], back_populates='jobs_created')
    expert = relationship('User', foreign_keys=[expert_id], back_populates='jobs_assigned')
    escrow = relationship('Escrow', back_populates='job', uselist=False)
    milestones = relationship('Milestone', back_populates='job')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'service_type': self.service_type.value if self.service_type else None,
            'status': self.status.value if self.status else None,
            'budget': float(self.budget) if self.budget else 0,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'deliverables': self.deliverables,
            'client_id': self.client_id,
            'expert_id': self.expert_id,
            'approved_by_admin': self.approved_by_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Escrow(Base):
    __tablename__ = 'escrows'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    status = Column(SQLEnum(EscrowStatus), default=EscrowStatus.CREATED)
    total_amount = Column(Numeric(10, 2), nullable=False)
    platform_fee = Column(Numeric(10, 2), default=0)
    stripe_payment_intent_id = Column(String(100))
    stripe_transfer_id = Column(String(100))
    funded_at = Column(DateTime)
    released_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = relationship('Job', back_populates='escrow')
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'status': self.status.value if self.status else None,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'platform_fee': float(self.platform_fee) if self.platform_fee else 0,
            'funded_at': self.funded_at.isoformat() if self.funded_at else None,
            'released_at': self.released_at.isoformat() if self.released_at else None
        }

class Milestone(Base):
    __tablename__ = 'milestones'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    amount = Column(Numeric(10, 2), nullable=False)
    deadline = Column(DateTime)
    status = Column(String(50), default='pending')  # pending, in_progress, delivered, accepted
    delivered_at = Column(DateTime)
    accepted_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship('Job', back_populates='milestones')
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'title': self.title,
            'description': self.description,
            'amount': float(self.amount) if self.amount else 0,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'status': self.status,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'accepted_at': self.accepted_at.isoformat() if self.accepted_at else None
        }

class Dispute(Base):
    __tablename__ = 'disputes'
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    opened_by_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Arbitrator
    status = Column(SQLEnum(DisputeStatus), default=DisputeStatus.OPEN)
    reason = Column(Text, nullable=False)
    evidence = Column(Text)  # JSON array of file URLs
    resolution = Column(Text)
    decision = Column(String(50))  # release, refund, partial_split
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship('Job', backref='disputes')
    opened_by = relationship('User', foreign_keys=[opened_by_id])
    assigned_to = relationship('User', foreign_keys=[assigned_to_id])
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'opened_by_id': self.opened_by_id,
            'status': self.status.value if self.status else None,
            'reason': self.reason,
            'resolution': self.resolution,
            'decision': self.decision,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Keep existing models for backward compatibility
class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    author = Column(String(100), nullable=False)
    avatar = Column(String(200))
    timestamp = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(500))
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author,
            'avatar': self.avatar,
            'timestamp': self.timestamp,
            'content': self.content,
            'imageUrl': self.image_url,
            'likes': self.likes,
            'comments': self.comments,
            'shares': self.shares
        }

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    instructor = Column(String(100), nullable=False)
    duration = Column(String(50), nullable=False)
    level = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500))
    enrolled = Column(Integer, default=0)
    rating = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'instructor': self.instructor,
            'duration': self.duration,
            'level': self.level,
            'description': self.description,
            'imageUrl': self.image_url,
            'enrolled': self.enrolled,
            'rating': self.rating
        }

class Space(Base):
    __tablename__ = 'spaces'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    member_count = Column(Integer, default=0)
    image_url = Column(String(500))
    category = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    members = relationship('Member', secondary=space_members, back_populates='spaces')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'memberCount': self.member_count,
            'imageUrl': self.image_url,
            'category': self.category
        }

class Member(Base):
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    title = Column(String(200))
    avatar = Column(String(200))
    connections = Column(Integer, default=0)
    mutual = Column(Integer, default=0)
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    spaces = relationship('Space', secondary=space_members, back_populates='members')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'avatar': self.avatar,
            'connections': self.connections,
            'mutual': self.mutual,
            'bio': self.bio
        }

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    date = Column(String(100), nullable=False)
    time = Column(String(50), nullable=False)
    location = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(500))
    attendees = Column(Integer, default=0)
    category = Column(String(100))
    organizer = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date,
            'time': self.time,
            'location': self.location,
            'description': self.description,
            'imageUrl': self.image_url,
            'attendees': self.attendees,
            'category': self.category,
            'organizer': self.organizer
        }

# Database setup function
def init_db(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
