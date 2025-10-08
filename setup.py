# setup.py - Simple setup script for our TODO app
import os

def create_env_file():
    """Create .env file with basic configuration"""
    env_content = """# MongoDB connection
MONGODB_URL=mongodb://localhost:27017

# JWT secret (change this in production)
JWT_SECRET=your-secret-key-here

# Debug mode
DEBUG=True
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env file")
    else:
        print("✅ .env file already exists")

if __name__ == "__main__":
    print("🚀 Setting up TODO app...")
    create_env_file()
    print("📝 Edit .env file with your MongoDB connection details")
    print("🔧 Run: pip install -r requirements.txt")
    print("🚀 Run: python main.py")
