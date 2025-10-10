# 🚀 MongoDB Atlas Setup Instructions

## **Step 1: Update Your `backend/.env` File**

Your `.env` file currently has Python code in it. Let's fix that!

### **Open or create `backend/.env` and replace ALL content with these 2 lines:**

```env
MONGODB_URL=mongodb+srv://mzahiddev404_db_user:YOUR_ACTUAL_PASSWORD_HERE@cluster0.sqcjidp.mongodb.net/todo_app?retryWrites=true&w=majority&appName=Cluster0
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production-12345
```

### **⚠️ IMPORTANT: Replace `YOUR_ACTUAL_PASSWORD_HERE` with your real MongoDB Atlas password!**

---

## **Step 2: Get Your MongoDB Atlas Password**

If you don't remember your password:

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Log in to your account
3. Click "Database Access" in the left sidebar
4. Find user `mzahiddev404_db_user`
5. Click "Edit" and set a new password
6. Copy the password

---

## **Step 3: Update the Connection String**

### **If your password has special characters** (like `@`, `%`, `#`, etc.), you need to URL-encode them:

| Character | URL Encoded |
|-----------|-------------|
| `@`       | `%40`       |
| `:`       | `%3A`       |
| `#`       | `%23`       |
| `%`       | `%25`       |
| `/`       | `%2F`       |
| `?`       | `%3F`       |

**Example**: If your password is `MyP@ss#123`, use `MyP%40ss%23123`

---

## **Step 4: Test the Connection**

### **1. Start the backend:**
```bash
cd backend
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **2. You should see:**
```
✅ Beanie initialized successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### **3. If you see an error:**
- ❌ **SSL handshake failed**: Your password might be wrong, or you need to allow network access
- ❌ **Connection refused**: Check your connection string format
- ❌ **Authentication failed**: Wrong username or password

---

## **Step 5: Allow Network Access**

Make sure MongoDB Atlas allows connections from your IP:

1. Go to MongoDB Atlas dashboard
2. Click "Network Access" in the left sidebar
3. Click "Add IP Address"
4. Choose "Allow Access from Anywhere" (for development)
   - Or add your specific IP address
5. Click "Confirm"

---

## **✅ Final `backend/.env` File Example**

Your file should look EXACTLY like this (with your actual password):

```env
MONGODB_URL=mongodb+srv://mzahiddev404_db_user:MySecurePass123@cluster0.sqcjidp.mongodb.net/todo_app?retryWrites=true&w=majority&appName=Cluster0
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production-12345
```

**That's it! Just 2 lines, no Python code, no comments.**

---

## **🐛 Troubleshooting**

### **Issue: "SSL handshake failed"**
**Solution**: This is the Python 3.13 SSL issue we discussed. The code already has a workaround in `backend/core/db.py` with these settings:
- `tlsAllowInvalidCertificates=True`
- `tlsAllowInvalidHostnames=True`

### **Issue: "Authentication failed"**
**Solution**: 
1. Double-check your username: `mzahiddev404_db_user`
2. Reset your password in MongoDB Atlas
3. Make sure you URL-encode special characters

### **Issue: "Connection timeout"**
**Solution**: 
1. Check MongoDB Atlas Network Access settings
2. Allow your IP address or "Allow Access from Anywhere"
3. Check your internet connection

---

## **🎯 Quick Command to Update .env**

Run this command to create the correct `.env` file (replace `YOUR_PASSWORD` with your actual password):

```bash
cat > backend/.env << 'EOF'
MONGODB_URL=mongodb+srv://mzahiddev404_db_user:YOUR_PASSWORD@cluster0.sqcjidp.mongodb.net/todo_app?retryWrites=true&w=majority&appName=Cluster0
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production-12345
EOF
```

Then edit it with your favorite editor:
```bash
nano backend/.env
# or
code backend/.env
# or
vim backend/.env
```

---

## **✨ Once It's Working**

When you see "✅ Beanie initialized successfully!", your app is connected to MongoDB Atlas!

Next steps:
1. Test the API: `curl http://localhost:8000/`
2. Start the frontend: `cd frontend && npx next dev`
3. Open `http://localhost:3000` in your browser
4. Sign up and create your first task! 🎉

