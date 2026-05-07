from fastapi import FastAPI, Depends, HTTPException, status, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn
from datetime import datetime, timedelta
from app.websocket import manager, websocket_endpoint

from app.database import get_db, engine, Base
from app.models import User, Project, Task, Team, Analytics, ActivityLog, TaskComment, TaskActivity, TaskAttachment, TaskDependency
from app.schemas import (
    UserCreate, UserResponse, ProjectCreate, ProjectResponse,
    TaskCreate, TaskResponse, TaskUpdate, TeamCreate, TeamResponse,
    AnalyticsResponse, DashboardStats, LoginRequest, Token,
    TaskCommentCreate, TaskCommentResponse, TaskActivityResponse,
    TaskDependencyCreate
)
from app.auth import create_access_token, verify_token, get_password_hash, authenticate_user

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task AI API",
    description="Backend API for Task AI Project Management System",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Authentication dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Auth endpoints
@app.post("/auth/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        role=user_data.role,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Dashboard endpoints
@app.get("/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get counts
    active_projects = db.query(Project).filter(Project.status == "active").count()
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "completed").count()
    team_members = db.query(Team).count()
    
    # Calculate metrics
    task_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Calculate critical alerts (tasks with high priority and not completed)
    critical_tasks = db.query(Task).filter(
        Task.priority == "critical",
        Task.status != "completed"
    ).count()
    
    # Calculate team efficiency based on completed tasks vs total tasks
    team_efficiency = task_completion_rate
    
    return DashboardStats(
        active_projects=active_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        task_completion_rate=task_completion_rate,
        team_members=team_members,
        team_efficiency=team_efficiency,
        critical_alerts=critical_tasks
    )

# Project endpoints
@app.get("/projects", response_model=List[ProjectResponse])
async def get_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects

@app.post("/projects", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_project = Project(
        name=project_data.name,
        description=project_data.description,
        owner_id=current_user.id,
        status=project_data.status or "active"
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@app.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# Task endpoints
@app.get("/tasks", response_model=List[TaskResponse])
async def get_tasks(
    project_id: Optional[int] = None,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    if project_id:
        query = query.filter(Task.project_id == project_id)
    if status:
        query = query.filter(Task.status == status)
    tasks = query.all()
    
    # Add project information to each task
    task_responses = []
    for task in tasks:
        task_dict = task.__dict__.copy()
        # Remove SQLAlchemy internal state
        task_dict.pop('_sa_instance_state', None)
        
        # Add project name if project_id exists
        if task.project_id:
            project = db.query(Project).filter(Project.id == task.project_id).first()
            task_dict['project_name'] = project.name if project else 'Unknown Project'
        else:
            task_dict['project_name'] = 'No Project'
            
        task_responses.append(TaskResponse(**task_dict))
    
    return task_responses

@app.post("/tasks", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        project_id=task_data.project_id,
        priority=task_data.priority,
        status=task_data.status,
        due_date=task_data.due_date,
        assigned_to=task_data.assigned_to,
        # Advanced features
        story_points=task_data.story_points,
        task_type=task_data.task_type,
        labels=task_data.labels,
        reporter_id=task_data.reporter_id or current_user.id,
        environment=task_data.environment,
        time_estimate=task_data.time_estimate
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Add task dependencies
    if task_data.depends_on:
        for dep_id in task_data.depends_on:
            dependency = TaskDependency(
                dependent_id=db_task.id,
                dependency_id=dep_id,
                dependency_type="depends_on"
            )
            db.add(dependency)

    if task_data.blocks:
        for block_id in task_data.blocks:
            dependency = TaskDependency(
                dependent_id=block_id,
                dependency_id=db_task.id,
                dependency_type="blocks"
            )
            db.add(dependency)

    db.commit()

    # Log activity
    activity = TaskActivity(
        task_id=db_task.id,
        user_id=current_user.id,
        action="created",
        description=f"Task '{db_task.title}' was created"
    )
    db.add(activity)
    db.commit()

    return db_task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Track changes for activity log
    old_values = {}
    new_values = {}

    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(db_task, field):
            old_values[field] = getattr(db_task, field)
            setattr(db_task, field, value)
            new_values[field] = value

    # Set resolution date if status is completed
    if task_update.status == "completed" and db_task.status != "completed":
        db_task.resolution_date = datetime.utcnow()
        if not db_task.resolution:
            db_task.resolution = "Fixed"

    db_task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_task)

    # Log activity
    if old_values:
        activity = TaskActivity(
            task_id=task_id,
            user_id=current_user.id,
            action="updated",
            old_value=str(old_values),
            new_value=str(new_values),
            description=f"Task '{db_task.title}' was updated"
        )
        db.add(activity)
        db.commit()

    return db_task

# Team endpoints
@app.get("/team", response_model=List[TeamResponse])
async def get_team_members(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    team_members = db.query(Team).all()
    return team_members

@app.post("/team", response_model=TeamResponse)
async def add_team_member(
    member_data: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_member = db.query(Team).filter(Team.email == member_data.email).first()
    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="Team member with this email already exists"
        )
    
    db_member = Team(
        name=member_data.name,
        role=member_data.role,
        email=member_data.email,
        department=member_data.department,
        avatar_url=member_data.avatar_url
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

# Task Comments
@app.get("/tasks/{task_id}/comments", response_model=List[TaskCommentResponse])
async def get_task_comments(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    comments = db.query(TaskComment).filter(TaskComment.task_id == task_id).order_by(TaskComment.created_at.desc()).all()
    return comments

@app.post("/tasks/{task_id}/comments", response_model=TaskCommentResponse)
async def create_task_comment(
    task_id: int,
    comment_data: TaskCommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_comment = TaskComment(
        task_id=task_id,
        author_id=current_user.id,
        comment=comment_data.comment
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    # Log activity
    activity = TaskActivity(
        task_id=task_id,
        user_id=current_user.id,
        action="comment_added",
        description=f"Comment added to task '{task.title}'"
    )
    db.add(activity)
    db.commit()

    return db_comment

# Task Activities
@app.get("/tasks/{task_id}/activities", response_model=List[TaskActivityResponse])
async def get_task_activities(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    activities = db.query(TaskActivity).filter(TaskActivity.task_id == task_id).order_by(TaskActivity.created_at.desc()).all()
    return activities

# Task Dependencies
@app.post("/tasks/{task_id}/dependencies", response_model=dict)
async def add_task_dependency(
    task_id: int,
    dependency_data: TaskDependencyCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify task exists
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    dependency = TaskDependency(
        dependent_id=task_id,
        dependency_id=dependency_data.dependency_id,
        dependency_type=dependency_data.dependency_type
    )
    db.add(dependency)
    db.commit()

    return {"message": "Dependency added successfully"}

# Analytics endpoints
@app.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get system metrics
    total_projects = db.query(Project).count()
    active_projects = db.query(Project).filter(Project.status == "active").count()
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "completed").count()
    
    # Calculate rates
    project_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    system_integrity = 82.0  # Placeholder metric
    
    return AnalyticsResponse(
        system_integrity=system_integrity,
        total_projects=total_projects,
        active_projects=active_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        project_completion_rate=project_completion_rate,
        team_efficiency=94.0,
        workload_distribution=[40, 65, 55, 85, 35, 90, 45, 60, 75, 95, 30, 50, 80, 70]  # Placeholder data
    )

@app.get("/analytics/workload")
async def get_workload_intensity(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Return mock workload data for the heatmap
    return {
        "workload_data": [
            [40, 20, 60, 100, 40, 20, 10],
            [10, 60, 40, 80, 20, 40, 60],
            [40, 10, 20, 40, 10, 20, 40],
            [80, 40, 60, 10, 20, 40, 80],
            [20, 10, 40, 20, 60, 10, 20]
        ]
    }

@app.get("/analytics/velocity")
async def get_task_velocity(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Return mock velocity data
    return {
        "planned_velocity": [80, 60, 70, 30, 45, 15, 25],
        "actual_velocity": [85, 75, 65, 55, 45, 35, 25],
        "labels": ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    }

@app.get("/analytics/team-distribution")
async def get_team_distribution(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Return mock team skill distribution
    return {
        "skills": ["BACKEND", "UI/UX", "DEVOPS", "QA"],
        "values": [92, 78, 85, 70],
        "core_ops": 92,
        "reliability": 78
    }

@app.websocket("/ws")
async def websocket_route(websocket: WebSocket):
    await websocket_endpoint(websocket)

# Advanced features endpoints
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/system/info")
async def system_info():
    return {
        "version": "2.0.48",
        "environment": "production",
        "features": ["real-time-updates", "advanced-analytics", "team-collaboration"],
        "database": "sqlite",
        "api_version": "v1"
    }

@app.post("/projects/{project_id}/duplicate")
async def duplicate_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get original project
    original_project = db.query(Project).filter(Project.id == project_id).first()
    if not original_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create duplicate
    duplicate = Project(
        name=f"{original_project.name} (Copy)",
        description=original_project.description,
        owner_id=current_user.id,
        status="active",
        progress=0.0
    )
    db.add(duplicate)
    db.commit()
    db.refresh(duplicate)
    
    # Notify all connected clients
    await manager.broadcast(json.dumps({
        "type": "project_created",
        "data": duplicate.__dict__
    }))
    
    return duplicate

@app.post("/tasks/{task_id}/complete")
async def complete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = "completed"
    db.commit()
    
    # Notify all connected clients
    await manager.broadcast(json.dumps({
        "type": "task_completed",
        "data": task.__dict__
    }))
    
    return task

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
