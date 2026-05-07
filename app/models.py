from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float, func, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    VIEWER = "viewer"

class ProjectStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"

class TaskStatus(enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TaskPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String, default="member")
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owned_projects = relationship("Project", back_populates="owner")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="active")
    progress = Column(Float, default=0.0)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    owner = relationship("User", back_populates="owned_projects")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="todo")  # todo, in_progress, review, completed, blocked, cancelled
    priority = Column(String, default="medium")  # lowest, low, medium, high, highest, critical
    project_id = Column(Integer, ForeignKey("projects.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = Column(DateTime)
    assigned_to = Column(Integer, ForeignKey("team_members.id"))
    
    # Advanced Jira-like features
    story_points = Column(Integer, default=1)  # Story points for agile estimation
    task_type = Column(String, default="task")  # task, bug, feature, improvement, epic
    labels = Column(String)  # Comma-separated labels
    reporter_id = Column(Integer, ForeignKey("team_members.id"))
    environment = Column(String)  # production, staging, development
    resolution = Column(String)  # Fixed, Won't Fix, Duplicate, Incomplete, Cannot Reproduce
    resolution_date = Column(DateTime)
    time_estimate = Column(Integer)  # Hours
    time_spent = Column(Integer, default=0)  # Hours
    progress_percentage = Column(Integer, default=0)  # 0-100
    
    # Relationships
    project = relationship("Project", back_populates="tasks")

class Team(Base):
    __tablename__ = "team_members"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(String(50), nullable=False)
    department = Column(String(50))
    avatar_url = Column(String(255))
    is_active = Column(Boolean, default=True)
    efficiency_score = Column(Float, default=0.0)
    tasks_completed = Column(Integer, default=0)
    current_tasks = Column(Integer, default=0)
    last_active = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Analytics(Base):
    __tablename__ = "analytics"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float, nullable=False)
    metric_type = Column(String(50))  # 'system', 'project', 'team', 'task'
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())

# Task dependencies table
class TaskDependency(Base):
    __tablename__ = "task_dependencies"
    
    id = Column(Integer, primary_key=True, index=True)
    dependent_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    dependency_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    dependency_type = Column(String, default="blocks")  # blocks, depends_on
    created_at = Column(DateTime, default=datetime.utcnow)

# Task comments table
class TaskComment(Base):
    __tablename__ = "task_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("team_members.id"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    task = relationship("Task", backref="comments")
    author = relationship("Team", backref="task_comments")

# Task activity tracking
class TaskActivity(Base):
    __tablename__ = "task_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("team_members.id"), nullable=False)
    action = Column(String, nullable=False)  # created, updated, assigned, status_changed, comment_added
    old_value = Column(String)
    new_value = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    task = relationship("Task", backref="activities")
    user = relationship("Team", backref="task_activities")

# Task attachments
class TaskAttachment(Base):
    __tablename__ = "task_attachments"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    mime_type = Column(String)
    uploaded_by = Column(Integer, ForeignKey("team_members.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    task = relationship("Task", backref="attachments")
    uploader = relationship("Team", backref="uploaded_attachments")

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)  # created, updated, deleted, assigned, etc.
    entity_type = Column(String, nullable=False)  # project, task, team
    entity_id = Column(Integer, nullable=False)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
