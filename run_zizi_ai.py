#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 ZiZi AI - Full Stack Launcher
Khởi chạy cả API server và Frontend server cùng lúc
"""

import subprocess
import threading
import time
import sys
import os
import signal
import requests
from typing import List

def print_banner():
    """In banner ZiZi AI"""
    print("=" * 60)
    print("🤖 ZiZi AI - Trợ Lý AI Thông Minh")
    print("=" * 60)
    print("🚀 Starting Full Stack Application...")
    print("📡 API Server: http://localhost:8000")
    print("🌐 Frontend UI: http://localhost:8501")
    print("📚 API Docs: http://localhost:8000/docs")
    print("=" * 60)

def check_dependencies():
    """Kiểm tra dependencies cần thiết"""
    print("🔍 Checking dependencies...")
    
    # Check if requirements are installed
    try:
        import fastapi
        import uvicorn
        import streamlit
        import requests
        import chromadb
        print("✅ All Python dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Please run: pip install -r requirements_api.txt")
        return False
    
    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            
            # Check if qwen2.5:7b is available
            models = response.json().get('models', [])
            qwen_available = any('qwen2.5' in model.get('name', '') for model in models)
            
            if qwen_available:
                print("✅ Qwen2.5 model is available")
            else:
                print("⚠️ Qwen2.5 model not found")
                print("💡 Please run: ollama pull qwen2.5:7b")
                return False
                
        else:
            print("❌ Ollama not responding")
            return False
            
    except requests.exceptions.RequestException:
        print("❌ Ollama not running")
        print("💡 Please start Ollama first: ollama serve")
        return False
    
    # Check if knowledge base exists
    if os.path.exists("chroma_db"):
        print("✅ Knowledge base found")
    else:
        print("⚠️ Knowledge base not found")
        print("💡 Please run: python load_zizi_training.py")
        return False
    
    return True

def run_api_server():
    """Chạy API server"""
    print("🔌 Starting API Server...")
    try:
        # Import here to avoid circular imports
        from api_server_clean import app
        import uvicorn
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
            access_log=False  # Reduce log noise
        )
    except Exception as e:
        print(f"❌ API Server error: {e}")

def run_frontend_server():
    """Chạy Frontend server"""
    print("🌐 Starting Frontend Server...")
    
    # Wait for API server to start
    time.sleep(3)
    
    try:
        # Run streamlit app
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "start_frontend.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--server.address", "0.0.0.0"
        ])
    except Exception as e:
        print(f"❌ Frontend Server error: {e}")

def wait_for_api_ready(max_attempts=30):
    """Đợi API server sẵn sàng"""
    print("⏳ Waiting for API server to be ready...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=2)
            if response.status_code == 200:
                print("✅ API Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(1)
        print(f"⏳ Attempt {attempt + 1}/{max_attempts}...")
    
    print("❌ API Server failed to start")
    return False

def cleanup_processes(processes: List[subprocess.Popen]):
    """Cleanup background processes"""
    print("\n🧹 Cleaning up processes...")
    for process in processes:
        if process.poll() is None:  # Process is still running
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

def main():
    """Main function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n💥 Dependency check failed!")
        print("🔧 Please fix the issues above and try again.")
        sys.exit(1)
    
    print("\n✅ All checks passed! Starting ZiZi AI...")
    
    processes = []
    
    try:
        # Start API server in background
        api_process = subprocess.Popen([
            sys.executable, "start_api_server.py"
        ])
        processes.append(api_process)
        
        # Wait for API to be ready
        if not wait_for_api_ready():
            cleanup_processes(processes)
            sys.exit(1)
        
        # Start frontend server
        print("\n🌐 Starting Frontend...")
        frontend_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", 
            "start_frontend.py",
            "--server.port", "8501",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--server.address", "0.0.0.0"
        ])
        processes.append(frontend_process)
        
        # Wait a bit for frontend to start
        time.sleep(3)
        
        print("\n🎉 ZiZi AI is now running!")
        print("📱 Open your browser and go to:")
        print("   🌐 Frontend: http://localhost:8501")
        print("   📡 API: http://localhost:8000")
        print("   📚 Docs: http://localhost:8000/docs")
        print("\n⏹️  Press Ctrl+C to stop all servers")
        
        # Keep running until interrupted
        try:
            while True:
                # Check if processes are still running
                for i, process in enumerate(processes):
                    if process.poll() is not None:
                        print(f"⚠️ Process {i} stopped unexpectedly")
                        break
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️  Stopping ZiZi AI...")
        
    except Exception as e:
        print(f"💥 Error starting ZiZi AI: {e}")
    
    finally:
        cleanup_processes(processes)
        print("👋 ZiZi AI stopped. Goodbye!")

if __name__ == "__main__":
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n⏹️  Received stop signal...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    main() 