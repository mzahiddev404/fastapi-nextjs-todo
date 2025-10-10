# 🚀 TODO CLI - Python CRUD Application

A standalone Python command-line interface for managing TODO tasks with MongoDB Atlas.

## ✨ Features

- ✅ **Create** new tasks with title, description, and priority
- ✅ **Read** all tasks or filter by status
- ✅ **Update** existing tasks (title, description, priority, status)
- ✅ **Delete** tasks by ID
- ✅ **Search** tasks by keyword
- ✅ **Mark** tasks as completed or pending
- ✅ **Connect** to MongoDB Atlas using `project_db_url` from `.env`
- ✅ **Async** operations with Motor and Beanie ODM
- ✅ **Color-coded** output with emojis for better UX

---

## 📋 Requirements

- Python 3.10+
- MongoDB Atlas account
- Dependencies: `motor`, `beanie`, `python-dotenv`, `pymongo`

---

## 🔧 Setup

### 1. Ensure `.env` file exists in `backend/` directory with:

```env
project_db_url=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
JWT_SECRET=your-secret-key
```

### 2. Install dependencies (if not already installed):

```bash
pip install motor beanie python-dotenv pymongo
```

### 3. Make the CLI executable:

```bash
chmod +x todo_cli.py
```

---

## 🎮 Usage

### View all available commands:

```bash
python3 todo_cli.py --help
```

### List all tasks:

```bash
python3 todo_cli.py list
```

### List tasks by status:

```bash
python3 todo_cli.py list --status pending
python3 todo_cli.py list --status completed
python3 todo_cli.py list --status in_progress
```

### Add a new task:

```bash
python3 todo_cli.py add "Buy groceries"
python3 todo_cli.py add "Finish project" --description "Complete before Friday" --priority high
```

### Get task details:

```bash
python3 todo_cli.py get <task_id>
```

### Update a task:

```bash
python3 todo_cli.py update <task_id> --title "New title"
python3 todo_cli.py update <task_id> --status completed
python3 todo_cli.py update <task_id> --priority high
```

### Mark task as completed:

```bash
python3 todo_cli.py complete <task_id>
```

### Mark task as pending:

```bash
python3 todo_cli.py pending <task_id>
```

### Search tasks:

```bash
python3 todo_cli.py search "groceries"
```

### Delete a task:

```bash
python3 todo_cli.py delete <task_id>
```

### Clear all tasks (⚠️ use with caution):

```bash
python3 todo_cli.py clear
```

---

## 📊 Example Workflow

```bash
# 1. Add some tasks
python3 todo_cli.py add "Buy milk" --priority high
python3 todo_cli.py add "Call mom" --description "Check on her health"
python3 todo_cli.py add "Finish homework" --priority high

# 2. List all tasks
python3 todo_cli.py list

# 3. Mark one as completed
python3 todo_cli.py complete 68e927781a4a5bdbe2264c38

# 4. Search for specific tasks
python3 todo_cli.py search "homework"

# 5. Update a task
python3 todo_cli.py update 68e927781a4a5bdbe2264c38 --priority medium

# 6. List only pending tasks
python3 todo_cli.py list --status pending
```

---

## 🎨 Output Format

The CLI uses color-coded emojis for easy visualization:

- **✓** = Completed task
- **○** = Pending/In-progress task
- **🔴** = High priority
- **🟡** = Medium priority
- **🟢** = Low priority

---

## 🗄️ Database

- **Database Name**: `todo_app`
- **Collection Name**: `cli_tasks` (separate from web app tasks)
- **Connection**: Uses `project_db_url` from `backend/.env`

---

## ⚠️ Notes

1. **Python 3.13 Compatibility**: The CLI includes SSL workarounds for MongoDB Atlas connections with Python 3.13
2. **Async Operations**: All database operations are asynchronous for better performance
3. **Separate Collection**: Uses `cli_tasks` collection to avoid conflicts with the web application
4. **UTC Timestamps**: All timestamps are stored in UTC

---

## 🐛 Troubleshooting

### Error: 'project_db_url' not found in .env file

- Ensure `backend/.env` file exists
- Check that `project_db_url` is defined in the `.env` file

### SSL handshake errors:

- The CLI includes workarounds for Python 3.13 SSL issues
- If problems persist, check MongoDB Atlas IP whitelist settings

### Connection timeout:

- Verify MongoDB Atlas cluster is running
- Check your internet connection
- Ensure correct credentials in `project_db_url`

---

## 🔒 Security

- Never commit `.env` files to version control
- Use strong passwords for MongoDB Atlas
- Rotate JWT secrets regularly

---

## 🎯 Status: ✅ Working & Tested

**Verified Operations:**
- ✅ MongoDB Atlas connection
- ✅ Task creation
- ✅ Task listing
- ✅ Task completion
- ✅ Task search
- ✅ Task update
- ✅ Task deletion

**Test Results:**
```
🔗 Connecting to MongoDB Atlas...
✅ Connected to MongoDB successfully!
✅ Task created successfully!
```

---

## 📝 License

Part of the FastAPI-Next.js TODO application project.

---

## 👨‍💻 Author

Created as a standalone CLI tool for the `fastapi-nextjs-todo` project.

**Date**: October 10, 2025

