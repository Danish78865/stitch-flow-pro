"""
Database initialization script for Task AI
Creates sample data for testing the application
"""

import asyncio
import sys
from datetime import datetime, timedelta
from app.database import SessionLocal, engine
from app.models import Base, User, Project, Task, Team, UserRole, ProjectStatus, TaskStatus, TaskPriority
from app.auth import get_password_hash

def create_sample_data():
    """Create sample data for testing"""
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = User(
            username="admin",
            email="admin@stitchflow.com",
            full_name="System Administrator",
            role="admin",
            hashed_password=get_password_hash("admin123")
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # Create sample team members
        team_members = [
            Team(
                name="Xavier Reed",
                email="xavier@stitchflow.com",
                role="Frontend Developer",
                department="Engineering",
                efficiency_score=85.0,
                tasks_completed=24,
                current_tasks=3
            ),
            Team(
                name="Nova Chen",
                email="nova@stitchflow.com",
                role="Backend Developer",
                department="Engineering",
                efficiency_score=92.0,
                tasks_completed=31,
                current_tasks=4
            ),
            Team(
                name="Kai Anderson",
                email="kai@stitchflow.com",
                role="UI/UX Designer",
                department="Design",
                efficiency_score=88.0,
                tasks_completed=18,
                current_tasks=2
            ),
            Team(
                name="Zara Mitchell",
                email="zara@stitchflow.com",
                role="Project Manager",
                department="Management",
                efficiency_score=95.0,
                tasks_completed=22,
                current_tasks=5
            ),
            Team(
                name="Leo Kim",
                email="leo@stitchflow.com",
                role="DevOps Engineer",
                department="Operations",
                efficiency_score=90.0,
                tasks_completed=19,
                current_tasks=3
            ),
            Team(
                name="Emma Thompson",
                email="emma@stitchflow.com",
                role="QA Engineer",
                department="Quality Assurance",
                efficiency_score=87.0,
                tasks_completed=28,
                current_tasks=4
            ),
            Team(
                name="David Wilson",
                email="david@stitchflow.com",
                role="Full Stack Developer",
                department="Engineering",
                efficiency_score=91.0,
                tasks_completed=35,
                current_tasks=5
            ),
            Team(
                name="Sarah Johnson",
                email="sarah@stitchflow.com",
                role="Product Owner",
                department="Product",
                efficiency_score=93.0,
                tasks_completed=16,
                current_tasks=2
            )
        ]
        
        for member in team_members:
            db.add(member)
        db.commit()
        
        # Create sample projects
        projects = [
            Project(
                name="Neural Net V2",
                description="Advanced neural network integration for real-time processing",
                owner_id=admin_user.id,
                status="active",
                progress=75.0,
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now() + timedelta(days=15)
            ),
            Project(
                name="Ghost Shell UI",
                description="Next-generation user interface with glassmorphism design",
                owner_id=admin_user.id,
                status="completed",
                progress=100.0,
                start_date=datetime.now() - timedelta(days=60),
                end_date=datetime.now() - timedelta(days=5)
            ),
            Project(
                name="Data Void Scan",
                description="Advanced data scanning and analysis system",
                owner_id=admin_user.id,
                status="active",
                progress=12.0,
                start_date=datetime.now() - timedelta(days=10),
                end_date=datetime.now() + timedelta(days=45)
            ),
            Project(
                name="Phoenix Platform",
                description="Core platform infrastructure upgrade",
                owner_id=admin_user.id,
                status="active",
                progress=45.0,
                start_date=datetime.now() - timedelta(days=20),
                end_date=datetime.now() + timedelta(days=30)
            ),
            Project(
                name="Quantum Bridge",
                description="Quantum computing integration layer",
                owner_id=admin_user.id,
                status="active",
                progress=60.0,
                start_date=datetime.now() - timedelta(days=25),
                end_date=datetime.now() + timedelta(days=20)
            ),
            Project(
                name="Cyber Shield",
                description="Advanced cybersecurity monitoring system",
                owner_id=admin_user.id,
                status="active",
                progress=30.0,
                start_date=datetime.now() - timedelta(days=15),
                end_date=datetime.now() + timedelta(days=35)
            ),
            Project(
                name="Nexus Core",
                description="Centralized data management system",
                owner_id=admin_user.id,
                status="active",
                progress=85.0,
                start_date=datetime.now() - timedelta(days=40),
                end_date=datetime.now() + timedelta(days=10)
            )
        ]
        
        for project in projects:
            db.add(project)
        db.commit()
        
        # Refresh projects to get their IDs
        for project in projects:
            db.refresh(project)
        
        # Create sample tasks
        tasks = [
            # Neural Net V2 tasks
            Task(
                title="Neural Core Integration",
                description="Implement asynchronous handshaking protocol between core processing unit and edge nodes",
                project_id=projects[0].id,
                priority="critical",
                status="todo",
                due_date=datetime.now() + timedelta(days=2),
                time_estimate=16
            ),
            Task(
                title="API Mesh Validation",
                description="Validating encrypted data streams across the mesh network architecture",
                project_id=projects[0].id,
                priority="high",
                status="in_progress",
                due_date=datetime.now() - timedelta(days=1),
                time_estimate=12
            ),
            Task(
                title="Datastore Migration",
                description="Moving legacy SQL structures to high-performance Phoenix vector database",
                project_id=projects[0].id,
                priority="high",
                status="in_progress",
                due_date=datetime.now() + timedelta(days=5),
                time_estimate=24
            ),
            Task(
                title="Model Training Pipeline",
                description="Build automated model training pipeline with hyperparameter optimization",
                project_id=projects[0].id,
                priority="high",
                status="todo",
                due_date=datetime.now() + timedelta(days=12),
                time_estimate=21
            ),
            Task(
                title="Inference API",
                description="Create REST API for model inference with batch processing",
                project_id=projects[0].id,
                priority="medium",
                status="todo",
                due_date=datetime.now() + timedelta(days=8),
                time_estimate=13
            ),
            
            # Ghost Shell UI tasks
            Task(
                title="UI Pattern Library",
                description="Standardize glassmorphism tokens across the phoenix platform modules",
                project_id=projects[1].id,
                priority="medium",
                status="completed",
                due_date=datetime.now() - timedelta(days=10),
                time_estimate=8,
                time_spent=7
            ),
            Task(
                title="Telemetry Dashboard",
                description="Final review of the real-time telemetry visualizer for phoenix system health",
                project_id=projects[1].id,
                priority="low",
                status="review",
                due_date=datetime.now() - timedelta(days=2),
                time_estimate=6
            ),
            Task(
                title="Component Library",
                description="Create reusable React component library with TypeScript",
                project_id=projects[1].id,
                priority="medium",
                status="completed",
                due_date=datetime.now() - timedelta(days=15),
                time_estimate=18,
                time_spent=17
            ),
            
            # Data Void Scan tasks
            Task(
                title="Vector Engine v1.2",
                description="Upgrade vector processing engine for improved performance",
                project_id=projects[2].id,
                priority="critical",
                status="todo",
                due_date=datetime.now() + timedelta(days=10),
                time_estimate=32
            ),
            Task(
                title="Edge Node Firewall",
                description="Implement advanced firewall system for edge nodes",
                project_id=projects[2].id,
                priority="high",
                status="todo",
                due_date=datetime.now() + timedelta(days=7),
                time_estimate=20
            ),
            Task(
                title="Data Pipeline",
                description="Build ETL pipeline for data ingestion and processing",
                project_id=projects[2].id,
                priority="high",
                status="in_progress",
                due_date=datetime.now() + timedelta(days=14),
                time_estimate=28
            ),
            
            # Phoenix Platform tasks
            Task(
                title="Core Infrastructure Setup",
                description="Set up core infrastructure components",
                project_id=projects[3].id,
                priority="high",
                status="completed",
                due_date=datetime.now() - timedelta(days=5),
                time_estimate=40,
                time_spent=38
            ),
            Task(
                title="Database Optimization",
                description="Optimize database queries and indexing",
                project_id=projects[3].id,
                priority="medium",
                status="in_progress",
                due_date=datetime.now() + timedelta(days=8),
                time_estimate=16
            ),
            Task(
                title="API Gateway",
                description="Implement API gateway with rate limiting and caching",
                project_id=projects[3].id,
                priority="high",
                status="todo",
                due_date=datetime.now() + timedelta(days=11),
                time_estimate=19
            ),
            
            # Quantum Bridge tasks
            Task(
                title="Quantum Algorithm Implementation",
                description="Implement quantum algorithms for optimization problems",
                project_id=projects[4].id,
                priority="critical",
                status="in_progress",
                due_date=datetime.now() + timedelta(days=18),
                time_estimate=45
            ),
            Task(
                title="Qubit Management",
                description="Build qubit state management system",
                project_id=projects[4].id,
                priority="high",
                status="todo",
                due_date=datetime.now() + timedelta(days=15),
                time_estimate=34
            ),
            Task(
                title="Hybrid Integration",
                description="Integrate quantum processing with classical systems",
                project_id=projects[4].id,
                priority="high",
                status="todo",
                due_date=datetime.now() + timedelta(days=20),
                time_estimate=38
            ),
            
            # Cyber Shield tasks
            Task(
                title="Threat Detection",
                description="Implement AI-powered threat detection system",
                project_id=projects[5].id,
                priority="critical",
                status="todo",
                due_date=datetime.now() + timedelta(days=25),
                time_estimate=52
            ),
            Task(
                title="Security Dashboard",
                description="Create real-time security monitoring dashboard",
                project_id=projects[5].id,
                priority="high",
                status="in_progress",
                due_date=datetime.now() + timedelta(days=12),
                time_estimate=24
            ),
            Task(
                title="Incident Response",
                description="Build automated incident response system",
                project_id=projects[5].id,
                priority="high",
                status="todo",
                due_date=datetime.now() + timedelta(days=30),
                time_estimate=41
            ),
            
            # Nexus Core tasks
            Task(
                title="Data Schema Design",
                description="Design unified data schema for all systems",
                project_id=projects[6].id,
                priority="critical",
                status="completed",
                due_date=datetime.now() - timedelta(days=20),
                time_estimate=22,
                time_spent=20
            ),
            Task(
                title="API Integration",
                description="Integrate all system APIs with central core",
                project_id=projects[6].id,
                priority="high",
                status="in_progress",
                due_date=datetime.now() + timedelta(days=5),
                time_estimate=18
            ),
            Task(
                title="Data Sync",
                description="Implement real-time data synchronization",
                project_id=projects[6].id,
                priority="medium",
                status="todo",
                due_date=datetime.now() + timedelta(days=8),
                time_estimate=15
            )
        ]
        
        for task in tasks:
            db.add(task)
        db.commit()
        
        print("✅ Sample data created successfully!")
        print(f"✅ Created {len(team_members)} team members")
        print(f"✅ Created {len(projects)} projects")
        print(f"✅ Created {len(tasks)} tasks")
        print("✅ Admin user created: username='admin', password='admin123'")
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def init_database():
    """Initialize database with tables and sample data"""
    print("🚀 Initializing Task AI database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    # Create sample data
    create_sample_data()
    
    print("🎉 Database initialization complete!")

if __name__ == "__main__":
    init_database()
