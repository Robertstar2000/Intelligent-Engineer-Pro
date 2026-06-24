---
title: Flask Dashboard with Approval System
name: flask-dashboard-with-approval
description: A comprehensive approach for creating a modern, information-dense web dashboard using Flask that tracks multiple business lines, provides metrics visualization, project management, and an approval workflow system.
---


## 🔍 MemPalace Query (MANDATORY FIRST STEP)
Before proceeding, query MemPalace for existing context:
```python
import sys, os; sys.path.insert(0, os.path.expanduser('~/.hermes/mempalace'))
import embed; embed.init_embedding(os.path.expanduser('~/.hermes/mempalace'))
results = embed.search_embeddings("MIFECO business process", k=5)
```
This retrieves previous decisions, domain-specific context, and lessons learned from the vector memory store.

# Flask Dashboard with Approval System

## Overview
A comprehensive approach for creating a modern, information-dense web dashboard using Flask that tracks multiple business lines, provides metrics visualization, project management, and an approval workflow system. This skill covers the complete implementation from backend API to frontend interactive features.

## Key Components

### 1. Flask Backend with SQLite
- **Database Schema**: Four main tables - business_metrics, projects, approvals, notifications
- **API Endpoints**: 
  - GET /api/metrics - Retrieve business metrics
  - GET /api/projects - Get project list with status and progress
  - GET /api/approvals - Fetch pending approvals
  - GET /api/notifications - Retrieve notifications
  - POST /api/approve/<id> - Approve artifacts
  - POST /api/reject/<id> - Reject artifacts
  - POST /api/update_project/<id> - Update project progress

### 2. Responsive Dashboard Design
- **Layout**: Grid-based responsive design that fits on one screen
- **Sidebar Navigation**: Multi-view navigation (Dashboard, Projects, Approvals, Notifications, Settings)
- **Metric Cards**: Display key metrics with progress bars and targets
- **Project Cards**: Show project status, deadlines, and progress
- **Approval Cards**: Pending items with approve/reject actions
- **Notification System**: Real-time updates with unread indicators

### 3. Interactive Features
- **Modal Dialogs**: For approval/rejection with notes
- **Progress Updates**: Inline project progress editing
- **Data Refresh**: Manual refresh button
- **Responsive Design**: Mobile-friendly with collapsed sidebar on small screens

### 4. Background Data Updates
- **Thread-Safe Updates**: Background thread updates metrics from files
- **File Monitoring**: Automatically updates metrics from manuscript files
- **Scheduled Updates**: Runs every minute to keep data current

## DOX Integration

When working in a project that uses the [DOX (Self-documenting AGENTS.md)](https://github.com/agent0ai/dox) framework:

- **Read Before Editing:** Walk the DOX tree from root to the target path. Read every AGENTS.md along the route before making any changes.
- **Update After Editing:** If the change affects purpose, scope, ownership, structure, workflows, or operating rules, update the closest owning AGENTS.md and refresh the Child DOX Index.
- **Reference:** [agent0ai/dox](https://github.com/agent0ai/dox) — copy `AGENTS.md` from the repo root into your project to initialize.

## Implementation Steps

### Step 1: Setup Project Structure
```bash
mkdir -p /path/to/dashboard/{templates,static,app}
```

### Step 2: Create Flask Application
```python
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import sqlite3
from datetime import datetime
import threading
import time
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
```

### Step 3: Database Schema Setup
```python
def init_db():
    conn = sqlite3.connect('mifeco_dashboard.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS business_metrics (... )''')
    c.execute('''CREATE TABLE IF NOT EXISTS projects (... )''')
    c.execute('''CREATE TABLE IF NOT EXISTS approvals (... )''')
    c.execute('''CREATE TABLE IF NOT EXISTS notifications (... )''')
    conn.commit()
    conn.close()
```

### Step 4: Sample Data Initialization
Pre-populate with sample data for Books, SaaS, and Consulting business lines.

### Step 5: API Endpoints Implementation
Implement RESTful endpoints for all data operations with proper JSON responses.

### Step 6: Frontend HTML/CSS/JS
Create a single dashboard.html with embedded CSS and JavaScript. Use modern design patterns with grid layouts, card components, and interactive elements.

### Step 7: Background Data Thread
Start a daemon thread that updates metrics from files every minute.

### Step 8: Run the Application
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5540, debug=True, threaded=True)
```

## Common Pitfalls & Solutions

### CSS Parsing Issues in Python
**Problem**: CSS variables with decimal values (e.g., `0.1`) cause Python syntax errors when embedded in strings.  
**Solution**: Write HTML/CSS files separately instead of embedding in Python strings. Use `write_file` or direct file writes.

### File Writing Approaches
**Problem**: Heredoc syntax (`<< 'EOF'`) fails in Python execution contexts.  
**Solution**: Use Python's file I/O operations directly:
```python
with open('/path/to/file', 'w') as f:
    f.write(content)
```

### Database Schema Design
**Problem**: Complex queries become slow with large datasets.  
**Solution**: Use proper indexing and keep schema simple. Use `row_factory` for dictionary-like row access.

### Background Thread Safety
**Problem**: Concurrent access to SQLite database from multiple threads.  
**Solution**: Use connection per operation or implement proper locking. For simple dashboards, per-operation connections are sufficient.

## Verification Steps
1. Test all API endpoints with curl or browser
2. Verify dashboard renders correctly in browser
3. Test approval/reject functionality
4. Check background updates from files
5. Verify responsive design on mobile

## Key Decisions
- **Technology Stack**: Flask backend with SQLite for lightweight, persistent storage
- **Responsive Design**: Grid-based layout that adapts to screen size, fits on one screen
- **Approval Workflow**: Modal dialogs with notes for approve/reject actions
- **Background Updates**: Daemon thread updates metrics from files every minute
- **Separation of Concerns**: HTML/CSS files written separately to avoid Python parsing issues
- **Error Handling**: Comprehensive error handling for file operations and database access
- **Security**: Input validation and sanitization for all API endpoints
- **Performance**: Connection per operation for SQLite to avoid threading issues

## Skill Dependencies
- Basic Flask knowledge
- SQLite database operations
- HTML/CSS/JavaScript fundamentals
- Python threading basics

## Maintenance
- Update sample data as business needs change
- Add new metrics/projects as needed
- Monitor background thread for errors
- Regularly backup SQLite database