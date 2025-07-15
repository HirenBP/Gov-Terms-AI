#!/usr/bin/env python3
"""
Development server launcher for Gov Terms AI.
This script starts both backend and frontend servers for development.
"""

import os
import subprocess
import sys
import time
import signal
from pathlib import Path
import threading

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log(message, color=Colors.OKBLUE):
    """Print colored log message."""
    print(f"{color}{message}{Colors.ENDC}")

def run_backend():
    """Run the FastAPI backend server."""
    log("🚀 Starting Backend Server...", Colors.OKGREEN)
    
    # Check if virtual environment exists (check both venv and .venv)
    venv_path = Path("venv")
    dot_venv_path = Path(".venv")
    
    if venv_path.exists():
        if os.name == 'nt':  # Windows
            python_cmd = "venv\\Scripts\\python.exe"
        else:  # Unix/MacOS
            python_cmd = "venv/bin/python"
    elif dot_venv_path.exists():
        if os.name == 'nt':  # Windows
            python_cmd = ".venv\\Scripts\\python.exe"
        else:  # Unix/MacOS
            python_cmd = ".venv/bin/python"
    else:
        log("❌ Virtual environment not found. Run setup.py first.", Colors.FAIL)
        return
    
    try:
        subprocess.run([python_cmd, "backend/app.py"], check=True)
    except subprocess.CalledProcessError as e:
        log(f"❌ Backend server failed: {e}", Colors.FAIL)
    except KeyboardInterrupt:
        log("🛑 Backend server stopped", Colors.WARNING)

def run_frontend():
    """Run the React frontend server."""
    log("⚛️ Starting Frontend Server...", Colors.OKGREEN)
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        log("❌ Frontend directory not found.", Colors.FAIL)
        return
    
    # Check if node_modules exists
    if not (frontend_path / "node_modules").exists():
        log("📦 Installing frontend dependencies...", Colors.WARNING)
        try:
            # Try different npm commands for Windows compatibility
            npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
            subprocess.run([npm_cmd, "install"], cwd=frontend_path, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            log(f"❌ Failed to install dependencies: {e}", Colors.FAIL)
            return
        except FileNotFoundError:
            log("❌ npm not found. Please install Node.js and npm.", Colors.FAIL)
            return
    
    try:
        npm_cmd = "npm.cmd" if os.name == 'nt' else "npm"
        subprocess.run([npm_cmd, "start"], cwd=frontend_path, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        log(f"❌ Frontend server failed: {e}", Colors.FAIL)
    except KeyboardInterrupt:
        log("🛑 Frontend server stopped", Colors.WARNING)
    except FileNotFoundError:
        log("❌ npm not found. Please install Node.js and npm.", Colors.FAIL)

def check_env_file():
    """Check if .env file exists and has required variables."""
    if not os.path.exists(".env"):
        log("⚠️  .env file not found. Creating from template...", Colors.WARNING)
        if os.path.exists(".env.example"):
            if os.name == 'nt':
                subprocess.run(["copy", ".env.example", ".env"], shell=True)
            else:
                subprocess.run(["cp", ".env.example", ".env"])
            log("📝 Please edit .env file with your API keys before starting servers.", Colors.WARNING)
            return False
        else:
            log("❌ .env.example not found. Cannot create .env file.", Colors.FAIL)
            return False
    return True

def main():
    """Main function to start development servers."""
    log("🏗️  Gov Terms AI Development Server", Colors.HEADER)
    
    # Check environment file
    if not check_env_file():
        log("❌ Environment setup incomplete. Please check .env file.", Colors.FAIL)
        sys.exit(1)
    
    # Get mode from command line argument
    mode = sys.argv[1] if len(sys.argv) > 1 else "both"
    
    if mode == "backend":
        run_backend()
    elif mode == "frontend":
        run_frontend()
    elif mode == "both":
        log("🔄 Starting both servers...", Colors.OKCYAN)
        log("💡 Backend will start on http://localhost:8000", Colors.OKBLUE)
        log("💡 Frontend will start on http://localhost:3000", Colors.OKBLUE)
        log("💡 Press Ctrl+C to stop both servers", Colors.WARNING)
        
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        # Wait a bit for backend to start
        time.sleep(3)
        
        # Start frontend (this will block)
        try:
            run_frontend()
        except KeyboardInterrupt:
            log("🛑 Stopping all servers...", Colors.WARNING)
            sys.exit(0)
    else:
        log("❌ Invalid mode. Use: python scripts/dev.py [backend|frontend|both]", Colors.FAIL)
        sys.exit(1)

if __name__ == "__main__":
    main()
