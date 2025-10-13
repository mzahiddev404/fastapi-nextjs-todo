#!/bin/bash

# =============================================================================
# PRODUCTION DEPLOYMENT SCRIPT
# =============================================================================
# Automated deployment script for the TODO application
# Supports both backend and frontend deployment

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKEND_DIR="backend"
FRONTEND_DIR="frontend"
PROJECT_NAME="todo-app"

# Functions
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

check_requirements() {
    log "Checking requirements..."
    
    # Check if required tools are installed
    command -v python3 >/dev/null 2>&1 || error "Python 3 is required but not installed"
    command -v node >/dev/null 2>&1 || error "Node.js is required but not installed"
    command -v npm >/dev/null 2>&1 || error "npm is required but not installed"
    
    # Check Python version
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [[ $(echo "$python_version < 3.8" | bc -l) -eq 1 ]]; then
        error "Python 3.8 or higher is required. Current version: $python_version"
    fi
    
    # Check Node.js version
    node_version=$(node -v | cut -d'v' -f2)
    if [[ $(echo "$node_version < 16.0" | bc -l) -eq 1 ]]; then
        error "Node.js 16 or higher is required. Current version: $node_version"
    fi
    
    success "All requirements satisfied"
}

setup_backend() {
    log "Setting up backend..."
    
    cd $BACKEND_DIR
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        log "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    log "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Check if .env file exists
    if [ ! -f ".env" ]; then
        warning ".env file not found. Creating from template..."
        if [ -f "env.example" ]; then
            cp env.example .env
            warning "Please update .env file with your configuration"
        else
            error ".env file not found and no template available"
        fi
    fi
    
    # Run database optimization
    log "Optimizing database..."
    python scripts/optimize_database.py || warning "Database optimization failed"
    
    success "Backend setup complete"
    cd ..
}

setup_frontend() {
    log "Setting up frontend..."
    
    cd $FRONTEND_DIR
    
    # Install dependencies
    log "Installing Node.js dependencies..."
    npm install
    
    # Build for production
    log "Building frontend for production..."
    npm run build
    
    success "Frontend setup complete"
    cd ..
}

run_tests() {
    log "Running tests..."
    
    # Backend tests
    log "Running backend tests..."
    cd $BACKEND_DIR
    source venv/bin/activate
    python -m pytest tests/ -v --cov=. --cov-report=html || warning "Backend tests failed"
    cd ..
    
    # Frontend tests
    log "Running frontend tests..."
    cd $FRONTEND_DIR
    npm test -- --coverage --watchAll=false || warning "Frontend tests failed"
    cd ..
    
    success "Tests completed"
}

start_services() {
    log "Starting services..."
    
    # Start backend in background
    log "Starting backend server..."
    cd $BACKEND_DIR
    source venv/bin/activate
    nohup python run.py > ../backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../backend.pid
    cd ..
    
    # Wait for backend to start
    log "Waiting for backend to start..."
    sleep 5
    
    # Check if backend is running
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        success "Backend is running on http://localhost:8000"
    else
        error "Backend failed to start"
    fi
    
    # Start frontend in background
    log "Starting frontend server..."
    cd $FRONTEND_DIR
    nohup npm start > ../frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../frontend.pid
    cd ..
    
    # Wait for frontend to start
    log "Waiting for frontend to start..."
    sleep 10
    
    # Check if frontend is running
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        success "Frontend is running on http://localhost:3000"
    else
        error "Frontend failed to start"
    fi
    
    success "All services started successfully"
}

stop_services() {
    log "Stopping services..."
    
    # Stop backend
    if [ -f "backend.pid" ]; then
        BACKEND_PID=$(cat backend.pid)
        if kill -0 $BACKEND_PID 2>/dev/null; then
            kill $BACKEND_PID
            success "Backend stopped"
        fi
        rm backend.pid
    fi
    
    # Stop frontend
    if [ -f "frontend.pid" ]; then
        FRONTEND_PID=$(cat frontend.pid)
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            kill $FRONTEND_PID
            success "Frontend stopped"
        fi
        rm frontend.pid
    fi
}

show_status() {
    log "Service Status:"
    
    # Check backend
    if curl -f http://localhost:8000/health >/dev/null 2>&1; then
        success "Backend: Running (http://localhost:8000)"
    else
        error "Backend: Not running"
    fi
    
    # Check frontend
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        success "Frontend: Running (http://localhost:3000)"
    else
        error "Frontend: Not running"
    fi
}

show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  setup     - Set up the application for production"
    echo "  start     - Start all services"
    echo "  stop      - Stop all services"
    echo "  restart   - Restart all services"
    echo "  status    - Show service status"
    echo "  test      - Run all tests"
    echo "  deploy    - Full deployment (setup + start)"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy    # Full deployment"
    echo "  $0 start     # Start services"
    echo "  $0 status    # Check status"
}

# Main script
case "${1:-help}" in
    setup)
        check_requirements
        setup_backend
        setup_frontend
        success "Setup complete! Run '$0 start' to start services."
        ;;
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        stop_services
        sleep 2
        start_services
        ;;
    status)
        show_status
        ;;
    test)
        run_tests
        ;;
    deploy)
        check_requirements
        setup_backend
        setup_frontend
        run_tests
        start_services
        success "Deployment complete!"
        show_status
        ;;
    help)
        show_help
        ;;
    *)
        error "Unknown command: $1"
        show_help
        ;;
esac
