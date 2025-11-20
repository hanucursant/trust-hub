import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models import (Base, get_session, User, Post, Course, Space, Member, Event,
                    Job, Escrow, Milestone, Dispute, UserRole, KYCStatus, BadgeType)
import hashlib

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg://trusthub_user:trusthub_pass@localhost:5432/trusthub_db')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def seed_database():
    """Initialize database with mock data"""
    print("Initializing database...")
    
    # Create engine and drop all tables first, then recreate them
    engine = create_engine(DATABASE_URL)
    print("Dropping all existing tables...")
    Base.metadata.drop_all(engine)
    print("Creating all tables with new schema...")
    Base.metadata.create_all(engine)
    
    session = get_session(engine)
    
    try:
        # Seed Posts
        print("Seeding posts...")
        posts = [
            Post(
                author='Todea Bianca',
                avatar='TB',
                timestamp='3d',
                content='💥 Cu 60 de lei pe lună intri la cel mai mare eveniment VSFA+ 💥\n\nDa, ai citit bine. Cu doar 60 de lei pe lună, intri GRATUIT la FoundAIrs Summit - evenimentul în care vei învăța să construiești proiecte de impact cu AI.',
                image_url='https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800',
                likes=42,
                comments=8,
                shares=5
            ),
            Post(
                author='John Doe',
                avatar='JD',
                timestamp='1h',
                content='Excited to share our latest project updates! 🚀 We\'ve been working on something amazing for the community.',
                image_url='https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800',
                likes=15,
                comments=3,
                shares=2
            ),
            Post(
                author='Maria Popescu',
                avatar='MP',
                timestamp='5h',
                content='Just finished an amazing workshop on machine learning! Can\'t wait to implement these new techniques. 🤖✨',
                image_url='https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800',
                likes=28,
                comments=12,
                shares=7
            ),
            Post(
                author='Alex Ionescu',
                avatar='AI',
                timestamp='1d',
                content='Looking forward to the networking event tonight! Who else is attending? 🎉',
                image_url='',
                likes=19,
                comments=6,
                shares=1
            ),
            Post(
                author='Elena Dumitrescu',
                avatar='ED',
                timestamp='2d',
                content='Three key lessons I learned from scaling my startup:\n\n1. Focus on customer feedback\n2. Build a strong team\n3. Stay adaptable\n\nWhat would you add?',
                image_url='https://images.unsplash.com/photo-1552664730-d307ca884978?w=800',
                likes=67,
                comments=23,
                shares=15
            )
        ]
        session.add_all(posts)
        
        # Seed Courses
        print("Seeding courses...")
        courses = [
            Course(
                title='Harta Antreprenorului',
                instructor='Todea Bianca',
                duration='6 weeks',
                level='Beginner',
                description='Learn the fundamentals of entrepreneurship and build your business roadmap.',
                image_url='https://images.unsplash.com/photo-1552664730-d307ca884978?w=400',
                enrolled=234,
                rating='4.8'
            ),
            Course(
                title='Lista Antreprenorului',
                instructor='Ion Popescu',
                duration='4 weeks',
                level='Intermediate',
                description='Essential tools and frameworks every entrepreneur needs to succeed.',
                image_url='https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400',
                enrolled=189,
                rating='4.6'
            ),
            Course(
                title='AI for Business',
                instructor='Maria Popescu',
                duration='8 weeks',
                level='Advanced',
                description='Implement AI solutions to scale your business and automate processes.',
                image_url='https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400',
                enrolled=156,
                rating='4.9'
            ),
            Course(
                title='Digital Marketing Mastery',
                instructor='Alex Ionescu',
                duration='5 weeks',
                level='Intermediate',
                description='Master digital marketing strategies to grow your online presence.',
                image_url='https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400',
                enrolled=312,
                rating='4.7'
            )
        ]
        session.add_all(courses)
        
        # Seed Spaces
        print("Seeding spaces...")
        spaces = [
            Space(
                name='Tech Innovators',
                description='A community for tech enthusiasts and innovators building the future.',
                member_count=245,
                image_url='https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=400',
                category='Technology'
            ),
            Space(
                name='Business Growth',
                description='Share strategies and insights on scaling your business.',
                member_count=189,
                image_url='https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=400',
                category='Business'
            ),
            Space(
                name='AI & Machine Learning',
                description='Explore the latest in AI and ML technologies.',
                member_count=312,
                image_url='https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400',
                category='Technology'
            ),
            Space(
                name='Startup Founders',
                description='Connect with fellow founders and share your journey.',
                member_count=156,
                image_url='https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=400',
                category='Entrepreneurship'
            )
        ]
        session.add_all(spaces)
        
        # Seed Members
        print("Seeding members...")
        members = [
            Member(
                name='Alice Smith',
                title='Full Stack Developer',
                avatar='AS',
                connections=234,
                mutual=12,
                bio='Passionate about building scalable web applications'
            ),
            Member(
                name='Bob Johnson',
                title='UI/UX Designer',
                avatar='BJ',
                connections=189,
                mutual=8,
                bio='Creating beautiful and intuitive user experiences'
            ),
            Member(
                name='Carol White',
                title='Product Manager',
                avatar='CW',
                connections=312,
                mutual=15,
                bio='Bridging the gap between business and technology'
            ),
            Member(
                name='David Brown',
                title='Data Scientist',
                avatar='DB',
                connections=156,
                mutual=5,
                bio='Turning data into actionable insights'
            ),
            Member(
                name='Emma Wilson',
                title='Marketing Specialist',
                avatar='EW',
                connections=278,
                mutual=10,
                bio='Growing brands through strategic digital marketing'
            ),
            Member(
                name='Frank Miller',
                title='Business Analyst',
                avatar='FM',
                connections=145,
                mutual=6,
                bio='Analyzing business processes to drive efficiency'
            )
        ]
        session.add_all(members)
        
        # Seed Events
        print("Seeding events...")
        events = [
            Event(
                title='FoundAIrs Summit 2025',
                date='2025-12-01',
                time='10:00 AM',
                location='Online',
                description='Learn to build AI-powered projects with industry experts.',
                image_url='https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400',
                attendees=450,
                category='Conference',
                organizer='VSFA+'
            ),
            Event(
                title='Tech Meetup Bucharest',
                date='2025-11-25',
                time='6:00 PM',
                location='Bucharest Tech Hub',
                description='Monthly networking event for tech professionals.',
                image_url='https://images.unsplash.com/photo-1505373877841-8d25f7d46678?w=400',
                attendees=120,
                category='Meetup',
                organizer='Tech Hub'
            ),
            Event(
                title='AI Workshop Series',
                date='2025-11-30',
                time='2:00 PM',
                location='Online',
                description='Hands-on workshop covering AI fundamentals and applications.',
                image_url='https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400',
                attendees=89,
                category='Workshop',
                organizer='AI Academy'
            ),
            Event(
                title='Startup Pitch Night',
                date='2025-12-05',
                time='7:00 PM',
                location='Innovation Center',
                description='Pitch your startup idea to investors and mentors.',
                image_url='https://images.unsplash.com/photo-1556761175-5973dc0f32e7?w=400',
                attendees=67,
                category='Competition',
                organizer='Innovation Center'
            )
        ]
        session.add_all(events)
        
        session.commit()
        print("✅ Database seeded successfully!")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding database: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == '__main__':
    seed_database()
