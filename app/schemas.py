from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# Auth schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: str = "member"
    avatar_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Project schemas
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"
    progress: float = 0.0

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Task schemas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    priority: Optional[str] = "medium"
    status: Optional[str] = "todo"
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    # Advanced Jira-like features
    story_points: Optional[int] = 1
    task_type: Optional[str] = "task"
    labels: Optional[str] = None
    reporter_id: Optional[int] = None
    environment: Optional[str] = None
    time_estimate: Optional[int] = None
    depends_on: Optional[List[int]] = []
    blocks: Optional[List[int]] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None
    story_points: Optional[int] = None
    task_type: Optional[str] = None
    labels: Optional[str] = None
    environment: Optional[str] = None
    resolution: Optional[str] = None
    time_estimate: Optional[int] = None
    time_spent: Optional[int] = None
    progress_percentage: Optional[int] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    project_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]
    assigned_to: Optional[int]
    project_name: Optional[str] = None
    # Advanced features
    story_points: int
    task_type: str
    labels: Optional[str]
    reporter_id: Optional[int]
    environment: Optional[str]
    resolution: Optional[str]
    resolution_date: Optional[datetime]
    time_estimate: Optional[int]
    time_spent: int
    progress_percentage: int
    assignee_name: Optional[str] = None
    reporter_name: Optional[str] = None
    comment_count: Optional[int] = 0
    attachment_count: Optional[int] = 0

class TaskCommentCreate(BaseModel):
    comment: str

class TaskCommentResponse(BaseModel):
    id: int
    task_id: int
    author_id: int
    comment: str
    created_at: datetime
    updated_at: datetime
    author_name: Optional[str] = None

class TaskActivityResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    action: str
    old_value: Optional[str]
    new_value: Optional[str]
    description: str
    created_at: datetime
    user_name: Optional[str] = None

class TaskDependencyCreate(BaseModel):
    dependency_id: int
    dependency_type: Optional[str] = "blocks"

# Team schemas
class TeamBase(BaseModel):
    name: str
    email: EmailStr
    role: str
    department: Optional[str] = None
    avatar_url: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int
    is_active: bool
    efficiency_score: float
    tasks_completed: int
    current_tasks: int
    last_active: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Analytics schemas
class AnalyticsResponse(BaseModel):
    system_integrity: float
    total_projects: int
    active_projects: int
    total_tasks: int
    completed_tasks: int
    project_completion_rate: float
    team_efficiency: float
    workload_distribution: List[int]

class DashboardStats(BaseModel):
    active_projects: int
    total_tasks: int
    completed_tasks: int
    task_completion_rate: float
    team_members: int
    team_efficiency: float
    critical_alerts: int

# Activity Log schemas
class ActivityLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    details: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
