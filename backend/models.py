from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

# Association table for many-to-many relationships
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
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'avatar': self.avatar
        }

class Token(Base):
    __tablename__ = 'tokens'
    
    id = Column(Integer, primary_key=True)
    token = Column(String(100), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship('User', backref='tokens')

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
