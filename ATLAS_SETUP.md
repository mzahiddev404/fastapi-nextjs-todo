# MongoDB Atlas Setup Guide

## Quick Setup Steps

1. **Create Account**: Go to https://www.mongodb.com/atlas
2. **Create Cluster**: Choose FREE tier (M0 Sandbox)
3. **Database User**: Create username/password
4. **Network Access**: Allow access from anywhere (0.0.0.0/0)
5. **Get Connection String**: Copy from "Connect your application"

## Update Configuration

Once you have your connection string, replace the placeholder in `app/core/config.py`:

```python
# Replace this line:
mongodb_uri: str = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"

# With your actual connection string:
mongodb_uri: str = "mongodb+srv://yourusername:yourpassword@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

## Test Connection

After updating the configuration, test the connection:

```bash
python3 test_mongo_connection.py
```

## Run the App

```bash
uvicorn app.main:app --reload
```

The app will be available at http://localhost:8000
