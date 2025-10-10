# MongoDB Setup Guide

## Python 3.13 Compatibility Issue

**IMPORTANT**: Python 3.13 has known SSL compatibility issues with MongoDB Atlas. This is a limitation of Python 3.13's stricter SSL certificate validation.

## Solutions

### Option 1: Use Local MongoDB (Recommended for Development)

1. **Install MongoDB locally:**
   ```bash
   # macOS with Homebrew
   brew tap mongodb/brew
   brew install mongodb-community
   
   # Start MongoDB
   brew services start mongodb/brew/mongodb-community
   ```

2. **Update your .env file:**
   ```env
   MONGODB_URL=mongodb://localhost:27017/todo_app
   JWT_SECRET=your-super-secret-jwt-key-here
   ```

3. **Test the connection:**
   ```bash
   cd backend
   python3 -c "import asyncio; from core.db import connect_to_mongo; asyncio.run(connect_to_mongo())"
   ```

### Option 2: Use Python 3.12 (Production Ready)

1. **Install Python 3.12:**
   ```bash
   # macOS with Homebrew
   brew install python@3.12
   
   # Create virtual environment with Python 3.12
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Use Atlas connection:**
   ```env
   MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/todo_app?retryWrites=true&w=majority
   JWT_SECRET=your-super-secret-jwt-key-here
   ```

### Option 3: Use Docker (Cross-Platform)

1. **Create docker-compose.yml:**
   ```yaml
   version: '3.8'
   services:
     mongodb:
       image: mongo:7.0
       ports:
         - "27017:27017"
       environment:
         MONGO_INITDB_ROOT_USERNAME: admin
         MONGO_INITDB_ROOT_PASSWORD: password
       volumes:
         - mongodb_data:/data/db
   
   volumes:
     mongodb_data:
   ```

2. **Start MongoDB:**
   ```bash
   docker-compose up -d
   ```

3. **Update .env:**
   ```env
   MONGODB_URL=mongodb://admin:password@localhost:27017/todo_app?authSource=admin
   JWT_SECRET=your-super-secret-jwt-key-here
   ```

## Current Status

- ✅ **PyMongo 4.9.2**: Latest version with Python 3.13 support
- ✅ **Motor 3.6.0**: Latest async driver
- ✅ **Enhanced SSL Configuration**: Optimized for Python 3.13
- ✅ **Fallback Mechanism**: Automatic fallback to localhost
- ⚠️ **Atlas SSL Issue**: Known Python 3.13 limitation

## Testing

Run the connection test:
```bash
cd backend
python3 -c "
import asyncio
from core.db import connect_to_mongo

async def test():
    try:
        await connect_to_mongo()
        print('✅ MongoDB connected successfully!')
    except Exception as e:
        print(f'❌ Connection failed: {e}')

asyncio.run(test())
"
```

## Production Recommendations

1. **For Production**: Use Python 3.12 with MongoDB Atlas
2. **For Development**: Use Python 3.13 with local MongoDB
3. **For CI/CD**: Use Docker with MongoDB container

## Troubleshooting

### SSL Handshake Failed
- **Cause**: Python 3.13 SSL compatibility issue
- **Solution**: Use local MongoDB or Python 3.12

### Connection Refused
- **Cause**: MongoDB not running
- **Solution**: Start MongoDB service

### Authentication Failed
- **Cause**: Wrong credentials or database name
- **Solution**: Check connection string and credentials
