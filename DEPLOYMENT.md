# Task AI - Deployment Guide

## Overview
Task AI is a production-ready project management system with real-time updates, advanced analytics, and team collaboration features.

## Features
- ✅ Real-time WebSocket updates
- ✅ Advanced project and task management
- ✅ Team collaboration tools
- ✅ Analytics dashboard
- ✅ JWT authentication
- ✅ SQLite database with full CRUD operations
- ✅ Docker containerization
- ✅ Production-ready configuration

## Quick Start (Development)

### Prerequisites
- Python 3.11+
- Node.js (for frontend development)
- SQLite

### Setup
```bash
# Clone and setup
git clone <repository>
cd stitch_flow_pro_workspace

# Install Python dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Start backend
python -m app.main

# Start frontend (in separate terminal)
python serve_frontend.py
```

### Access
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Login: Username: `admin`, Password: `admin123`

## Production Deployment

### Using Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Manual Deployment

#### Backend
```bash
# Build Docker image
docker build -t stitchflow-backend .

# Run backend
docker run -d \
  --name stitchflow-backend \
  -p 8000:8000 \
  -v $(pwd)/stitchflow.db:/app/stitchflow.db \
  -e DATABASE_URL=sqlite:///./stitchflow.db \
  -e SECRET_KEY=your-production-secret-key \
  stitchflow-backend
```

#### Frontend
```bash
# Run nginx with frontend
docker run -d \
  --name stitchflow-frontend \
  -p 3000:80 \
  -v $(pwd)/static:/usr/share/nginx/html/static \
  -v $(pwd)/*.html:/usr/share/nginx/html/ \
  nginx:alpine
```

## Environment Variables

### Backend
- `DATABASE_URL`: Database connection string (default: `sqlite:///./stitchflow.db`)
- `SECRET_KEY`: JWT secret key (change for production!)
- `ENVIRONMENT`: `production` or `development`
- `DEBUG`: Set to `false` in production

### Frontend
- `API_BASE_URL`: Backend API URL (default: `http://localhost:8000`)

## Database Management

### Backup
```bash
# Manual backup
cp stitchflow.db backup_$(date +%Y%m%d_%H%M%S).db

# Via API
curl -X POST http://localhost:8000/backup \
  -H "Authorization: Bearer <token>"
```

### Migration
```bash
# Initialize fresh database
python init_db.py

# Reset database (WARNING: Deletes all data)
rm stitchflow.db
python init_db.py
```

## Monitoring

### Health Checks
- Backend: `GET /health`
- System Info: `GET /system/info`

### Logs
```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Application logs
tail -f /var/log/stitchflow.log
```

## Security

### Production Checklist
- [ ] Change default admin password
- [ ] Set strong `SECRET_KEY`
- [ ] Enable HTTPS
- [ ] Configure firewall
- [ ] Set up database backups
- [ ] Monitor logs
- [ ] Update dependencies

### Authentication
- JWT tokens with 30-minute expiration
- Password hashing with bcrypt
- Role-based access control

## Performance

### Optimization
- WebSocket connections for real-time updates
- Efficient database queries
- Frontend caching
- Gzip compression (nginx)

### Scaling
- Horizontal scaling with load balancer
- Database connection pooling
- Redis for session storage (optional)

## Troubleshooting

### Common Issues

#### Database Connection Error
```bash
# Check database file
ls -la stitchflow.db

# Check permissions
chmod 664 stitchflow.db
```

#### WebSocket Connection Failed
```bash
# Check backend logs
docker-compose logs backend | grep WebSocket

# Verify port accessibility
telnet localhost 8000
```

#### Frontend Not Loading
```bash
# Check nginx configuration
docker-compose exec frontend nginx -t

# Reload nginx
docker-compose exec frontend nginx -s reload
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Projects
- `GET /projects` - List projects
- `POST /projects` - Create project
- `POST /projects/{id}/duplicate` - Duplicate project

### Tasks
- `GET /tasks` - List tasks
- `POST /tasks` - Create task
- `POST /tasks/{id}/complete` - Complete task

### Team
- `GET /team` - List team members
- `POST /team` - Add team member

### Analytics
- `GET /dashboard/stats` - Dashboard statistics
- `GET /analytics` - General analytics
- `GET /analytics/workload` - Workload data

### WebSocket
- `WS /ws` - Real-time updates

## Support

For issues and support:
1. Check logs for error messages
2. Verify environment configuration
3. Test API endpoints directly
4. Check database connectivity

## License
© 2024 Task AI. All rights reserved.
