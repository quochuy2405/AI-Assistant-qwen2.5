#!/usr/bin/env python3
"""
Script để chạy ZiZi AI API Server
"""

import uvicorn
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='ZiZi AI API Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    parser.add_argument('--port', type=int, default=8000, help='Port number')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    parser.add_argument('--workers', type=int, default=1, help='Number of workers')
    
    args = parser.parse_args()
    
    print("🤖 Starting ZiZi AI API Server...")
    print(f"📡 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"🔄 Reload: {args.reload}")
    print(f"👥 Workers: {args.workers}")
    print("=" * 50)
    
    try:
        # Chạy server với cấu hình modular
        uvicorn.run(
            "api_server_clean:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            workers=args.workers if not args.reload else 1,
            access_log=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 ZiZi AI API Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 