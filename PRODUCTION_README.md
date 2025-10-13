# 🚀 Production Deployment Guide

This guide covers deploying the TODO application to production with all security, performance, and monitoring features enabled.

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **MongoDB** (local or Atlas)
- **Redis** (optional, for caching and rate limiting)
- **Linux/Unix** environment (Ubuntu 20.04+ recommended)

## 🔧 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd fastapi-nextjs-todo
chmod +x deploy.sh
```

### 2. Deploy Everything
```bash
./deploy.sh deploy
```

This will:
- ✅ Check all requirements
- ✅ Set up backend with virtual environment
- ✅ Set up frontend with dependencies
- ✅ Run all tests
- ✅ Start both services
- ✅ Verify everything is working

### 3. Access Your App
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

## 🛠 Manual Setup

### Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp env.example .env
# Edit .env with your settings

# Optimize database
python scripts/optimize_database.py

# Start server
python run.py
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Build for production
npm run build

# Start server
npm start
```

## 🔐 Security Configuration

### Environment Variables
Create a `.env` file in the `backend` directory:

```env
# Required
JWT_SECRET=your-super-secret-jwt-key-64-chars-minimum
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/todoapp

# Optional but recommended
REDIS_URL=redis://localhost:6379
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
```

### Security Features Enabled
- ✅ **JWT Authentication** with secure secret
- ✅ **Password Strength Validation** (8+ chars, mixed case, numbers, symbols)
- ✅ **Rate Limiting** (5/min for auth, 100/min for API)
- ✅ **CORS Protection** with configurable origins
- ✅ **Security Headers** (XSS, CSRF, Content-Type protection)
- ✅ **Input Validation** and sanitization
- ✅ **Request Size Limits** (10MB default)

## 📊 Performance Optimizations

### Database
- ✅ **Optimized Indexes** for all common queries
- ✅ **Connection Pooling** (10 connections, 30s idle timeout)
- ✅ **Query Optimization** with compound indexes
- ✅ **Text Search** indexes for task content

### Caching
- ✅ **Redis Caching** with fallback to memory
- ✅ **SWR Caching** on frontend (30s default)
- ✅ **Lazy Loading** for large task lists
- ✅ **Pagination** (10 items per page)

### Frontend
- ✅ **Code Splitting** and lazy loading
- ✅ **Image Optimization** ready
- ✅ **Bundle Optimization** with Next.js
- ✅ **Performance Monitoring** hooks

## 🔍 Monitoring & Health Checks

### Health Endpoints
- `GET /api/v1/health` - Basic health check
- `GET /api/v1/health/detailed` - Comprehensive system status
- `GET /api/v1/health/ready` - Kubernetes readiness probe
- `GET /api/v1/health/live` - Kubernetes liveness probe
- `GET /api/v1/health/metrics` - Application metrics

### Monitoring Features
- ✅ **System Resource Monitoring** (CPU, Memory, Disk)
- ✅ **Database Performance Tracking**
- ✅ **Error Tracking** with categorization
- ✅ **Request/Response Time Monitoring**
- ✅ **Cache Hit/Miss Ratios**

## 🧪 Testing

### Run All Tests
```bash
# Backend tests
cd backend
source venv/bin/activate
python -m pytest tests/ -v --cov=. --cov-report=html

# Frontend tests
cd frontend
npm test -- --coverage --watchAll=false
```

### Test Coverage
- **Backend**: 80%+ coverage target
- **Frontend**: 80%+ coverage target
- **Integration Tests**: API endpoints
- **Security Tests**: Authentication, validation, rate limiting

## 🚀 Production Deployment

### Using Docker (Recommended)
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Using PM2 (Process Manager)
```bash
# Install PM2
npm install -g pm2

# Start backend
cd backend
pm2 start run.py --name "todo-backend"

# Start frontend
cd frontend
pm2 start npm --name "todo-frontend" -- start

# Save PM2 configuration
pm2 save
pm2 startup
```

### Using Systemd (Linux)
```bash
# Create systemd service files
sudo cp deployment/todo-backend.service /etc/systemd/system/
sudo cp deployment/todo-frontend.service /etc/systemd/system/

# Enable and start services
sudo systemctl enable todo-backend todo-frontend
sudo systemctl start todo-backend todo-frontend
```

## 📈 Scaling

### Horizontal Scaling
- **Load Balancer**: Nginx or HAProxy
- **Multiple Backend Instances**: Behind load balancer
- **Database Clustering**: MongoDB replica set
- **Redis Cluster**: For distributed caching

### Vertical Scaling
- **Increase Memory**: For larger datasets
- **SSD Storage**: For better I/O performance
- **More CPU Cores**: For concurrent requests

## 🔧 Maintenance

### Database Maintenance
```bash
# Optimize database indexes
python scripts/optimize_database.py

# Backup database
mongodump --uri="your-mongodb-uri" --out=backup/

# Restore database
mongorestore --uri="your-mongodb-uri" backup/
```

### Log Management
```bash
# View logs
tail -f backend.log
tail -f frontend.log

# Rotate logs (with logrotate)
sudo logrotate -f /etc/logrotate.d/todo-app
```

### Updates
```bash
# Update backend
cd backend
git pull
source venv/bin/activate
pip install -r requirements.txt
python scripts/optimize_database.py

# Update frontend
cd frontend
git pull
npm install
npm run build

# Restart services
./deploy.sh restart
```

## 🚨 Troubleshooting

### Common Issues

#### Backend Won't Start
```bash
# Check logs
tail -f backend.log

# Check environment variables
cat backend/.env

# Test database connection
python -c "from core.db import connect_to_mongo; import asyncio; asyncio.run(connect_to_mongo())"
```

#### Frontend Build Fails
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### Database Connection Issues
```bash
# Test MongoDB connection
mongosh "your-mongodb-uri"

# Check network connectivity
telnet your-mongodb-host 27017
```

#### Performance Issues
```bash
# Check system resources
htop
df -h
free -h

# Check application metrics
curl http://localhost:8000/api/v1/health/metrics
```

### Health Check Commands
```bash
# Check service status
./deploy.sh status

# Test API endpoints
curl http://localhost:8000/api/v1/health
curl http://localhost:8000/api/v1/health/detailed

# Test frontend
curl http://localhost:3000
```

## 📞 Support

### Logs Location
- **Backend Logs**: `backend.log`
- **Frontend Logs**: `frontend.log`
- **System Logs**: `/var/log/syslog`

### Configuration Files
- **Backend Config**: `backend/.env`
- **Frontend Config**: `frontend/next.config.ts`
- **Database Config**: `backend/core/db.py`

### Monitoring
- **Health Dashboard**: http://localhost:8000/api/v1/health/detailed
- **API Documentation**: http://localhost:8000/docs
- **Metrics**: http://localhost:8000/api/v1/health/metrics

---

## 🎉 You're Production Ready!

Your TODO application is now deployed with:
- ✅ **Enterprise-grade security**
- ✅ **High performance optimizations**
- ✅ **Comprehensive monitoring**
- ✅ **Automated testing**
- ✅ **Production-ready configuration**

**Next Steps:**
1. Configure your domain and SSL certificates
2. Set up monitoring alerts (Sentry, DataDog, etc.)
3. Configure automated backups
4. Set up CI/CD pipeline
5. Scale based on usage patterns

Happy coding! 🚀
