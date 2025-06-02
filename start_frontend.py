#!/usr/bin/env python3
"""
🌐 Frontend Server for AI KOC Support Chat Interface
Start the web interface to interact with the API
"""

import http.server
import socketserver
import webbrowser
import os
import argparse
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        super().__init__(*args, directory="frontend", **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    parser = argparse.ArgumentParser(description='Start AI KOC Support Frontend Server')
    parser.add_argument('--port', type=int, default=3000, help='Port to serve on (default: 3000)')
    parser.add_argument('--host', default='localhost', help='Host to serve on (default: localhost)')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser automatically')
    
    args = parser.parse_args()
    
    # Check if frontend directory exists
    frontend_dir = Path('frontend')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        print("Make sure you're running this from the project root.")
        return
    
    # Check if index.html exists
    index_file = frontend_dir / 'index.html'
    if not index_file.exists():
        print("❌ index.html not found in frontend directory!")
        return
    
    print("🌐 Starting AI KOC Support Frontend Server...")
    print("=" * 50)
    print(f"🏠 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"📁 Directory: ./frontend")
    print(f"🌍 URL: http://{args.host}:{args.port}")
    print("=" * 50)
    
    try:
        # Create server
        with socketserver.TCPServer((args.host, args.port), CustomHTTPRequestHandler) as httpd:
            url = f"http://{args.host}:{args.port}"
            
            print(f"✅ Server started successfully!")
            print(f"🚀 Open your browser and go to: {url}")
            print("📝 Make sure your API server is running on http://localhost:8000")
            print("🛑 Press Ctrl+C to stop the server")
            
            # Open browser automatically
            if not args.no_browser:
                try:
                    webbrowser.open(url)
                    print("🌐 Browser opened automatically")
                except Exception as e:
                    print(f"⚠️  Could not open browser automatically: {e}")
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {args.port} is already in use!")
            print(f"Try a different port: python start_frontend.py --port {args.port + 1}")
        else:
            print(f"❌ Error starting server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 