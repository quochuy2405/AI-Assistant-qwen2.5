#!/usr/bin/env python3
"""
Script chạy ứng dụng AI Hỗ Trợ KOC
Kiểm tra dependencies và khởi động ứng dụng
"""

import sys
import subprocess
import importlib
import os
from pathlib import Path

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 8):
        print("❌ Cần Python 3.8 trở lên")
        print(f"Phiên bản hiện tại: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Kiểm tra các dependencies cần thiết"""
    required_packages = [
        'streamlit',
        'ollama', 
        'chromadb',
        'sentence_transformers',
        'PyPDF2',
        'fitz'  # PyMuPDF
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'fitz':
                importlib.import_module('fitz')
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Các package bị thiếu: {', '.join(missing_packages)}")
        print("Chạy: pip install -r requirements.txt")
        return False
    
    return True

def check_ollama():
    """Kiểm tra Ollama có chạy không"""
    try:
        import ollama
        response = ollama.list()
        print("✅ Ollama đang chạy")
        
        # Kiểm tra có model nào không
        if hasattr(response, 'models') and response.models:
            print(f"✅ Có {len(response.models)} model(s) sẵn sàng")
            for model in response.models:
                # Thử nhiều cách truy cập tên model
                model_name = getattr(model, 'name', None) or getattr(model, 'model', None) or str(model)
                print(f"   - {model_name}")
        elif isinstance(response, dict) and response.get('models'):
            print(f"✅ Có {len(response['models'])} model(s) sẵn sàng")
            for model in response['models']:
                model_name = model.get('name') or model.get('model') or str(model)
                print(f"   - {model_name}")
        else:
            print("⚠️  Chưa có model nào được tải")
            print("Chạy: ollama pull qwen2.5:7b")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Không thể kết nối Ollama: {e}")
        print("Hãy chạy: ollama serve")
        return False

def check_config():
    """Kiểm tra cấu hình"""
    try:
        from config import Config
        validation = Config.validate()
        
        if validation['valid']:
            print("✅ Cấu hình hợp lệ")
        else:
            print("❌ Cấu hình có lỗi:")
            for error in validation['errors']:
                print(f"   - {error}")
            return False
        
        if validation['warnings']:
            print("⚠️  Cảnh báo cấu hình:")
            for warning in validation['warnings']:
                print(f"   - {warning}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi kiểm tra cấu hình: {e}")
        return False

def setup_directories():
    """Tạo các thư mục cần thiết"""
    directories = [
        './chroma_db',
        './logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Thư mục {directory}")

def main():
    """Hàm chính"""
    print("🤖 AI Hỗ Trợ KOC - Khởi Động Ứng Dụng")
    print("=" * 50)
    
    # Kiểm tra Python
    print("\n🐍 Kiểm tra Python:")
    if not check_python_version():
        sys.exit(1)
    
    # Kiểm tra dependencies
    print("\n📦 Kiểm tra Dependencies:")
    if not check_dependencies():
        sys.exit(1)
    
    # Tạo thư mục
    print("\n📁 Tạo Thư Mục:")
    setup_directories()
    
    # Kiểm tra cấu hình
    print("\n🔧 Kiểm tra Cấu Hình:")
    if not check_config():
        sys.exit(1)
    
    # Kiểm tra Ollama
    print("\n🦙 Kiểm tra Ollama:")
    if not check_ollama():
        print("\n💡 Hướng dẫn khởi động Ollama:")
        print("1. Mở terminal mới")
        print("2. Chạy: ollama serve")
        print("3. Tải model: ollama pull qwen2.5:7b")
        print("4. Chạy lại script này")
        sys.exit(1)
    
    print("\n🎉 Tất cả kiểm tra đã PASS!")
    print("🚀 Đang khởi động ứng dụng Streamlit...")
    print("🌐 Ứng dụng sẽ mở tại: http://localhost:8501")
    print("\n" + "=" * 50)
    
    # Khởi động Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Ứng dụng đã dừng!")
    except Exception as e:
        print(f"\n❌ Lỗi khởi động ứng dụng: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 