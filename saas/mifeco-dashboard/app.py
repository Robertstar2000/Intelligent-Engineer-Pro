#!/usr/bin/env python3
"""MIFECO Virtual Operations Dashboard"""
from flask import Flask, render_template, jsonify
from flask_cors import CORS
import subprocess, os, json, time, threading
from pathlib import Path
from datetime import datetime

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# ── Data ──────────────────────────────────────────────────────────────────

SAAS_APPS = [
    {
        "name": "Project Hypatia Pro",
        "slug": "hypatia-pro",
        "description": "AI-assisted Scientific Research Protocol",
        "local_port": 3001,
        "prod_url": "https://project-hypatia-pro-1064319572465.us-west1.run.app/",
        "repo": "https://github.com/Robertstar2000/https-github.com-Robertstar2000-HypatiaPro",
        "icon": "🔬"
    },
    {
        "name": "Project Management Accelerator",
        "slug": "pma",
        "description": "Hyper-Agile Project Lifecycle Management",
        "local_port": 3002,
        "prod_url": "https://project-management-accelerator-845075991286.us-west1.run.app/",
        "repo": "https://github.com/Robertstar2000/Project-management-accelerator",
        "icon": "📊"
    },
    {
        "name": "VibraEngineer",
        "slug": "vibraengineer",
        "description": "VIBE Engineering Protocol — HMAP Lifecycle",
        "local_port": 3003,
        "prod_url": "https://vibraengineer-845075991286.us-west1.run.app/",
        "repo": "https://github.com/Robertstar2000/Intelligent-Engineer",
        "icon": "🔧"
    }
]

BOOKS = [
    {"title": "First Generation", "status": "Published", "icon": "🌄", "path": "First_Generation"},
    {"title": "Second Generation", "status": "Published", "icon": "🕳️", "path": "Second_Generation"},
    {"title": "Third Generation", "status": "Published", "icon": "👽", "path": "Third_Generation"},
    {"title": "The Future is Unwritten", "status": "Published", "icon": "🌙", "path": "The_Unwritten_Future"},
    {"title": "AI for Small Business", "status": "Published", "icon": "🤖", "path": "MIFECO_AI_Playbook"},
]

def check_port(port):
    try:
        r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
                           f"http://localhost:{port}"], capture_output=True, text=True, timeout=3)
        return r.stdout.strip() == "200"
    except:
        return False

def get_service_status():
    statuses = {}
    for app_info in SAAS_APPS:
        statuses[app_info["slug"]] = {
            "running": check_port(app_info["local_port"]),
            "port": app_info["local_port"]
        }
    return statuses

# ── Routes ────────────────────────────────────────────────────────────────

@app.route('/')
def dashboard():
    return render_template('dashboard.html', 
                          saas_apps=SAAS_APPS, 
                          books=BOOKS,
                          year=datetime.now().year)

@app.route('/api/status')
def api_status():
    return jsonify(get_service_status())

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "time": datetime.now().isoformat()})

if __name__ == '__main__':
    # Ensure templates dir exists
    os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'static'), exist_ok=True)
    print("🚀 MIFECO Operations Dashboard starting on :5540")
    app.run(host='0.0.0.0', port=5540, debug=False, threaded=True)
