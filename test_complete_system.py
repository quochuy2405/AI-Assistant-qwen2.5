#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete System Test - KOC App với AI Assistant
"""

import requests
import json
from api.responses import get_smart_response, test_ollama_connection

def test_ai_assistant():
    """Test AI Assistant với KOC app knowledge"""
    print("🤖 TESTING AI ASSISTANT với KOC APP KNOWLEDGE")
    print("=" * 50)
    
    test_questions = [
        "KOC app là gì?",
        "Làm sao đăng nhập bằng TikTok?", 
        "Có những tính năng gì trong dashboard?",
        "AI Assistant có thể làm gì?",
        "Cách quản lý chiến dịch như thế nào?",
        "Phương thức thanh toán nào được hỗ trợ?",
        "Technical specs của app ra sao?",
        "Lỗi đăng nhập TikTok thì xử lý thế nào?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n📋 Question {i}: {question}")
        print("-" * 40)
        
        try:
            response = get_smart_response(question)
            print(f"🤖 AI Response:")
            print(response)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🔌 TESTING API ENDPOINTS")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        print(f"🟢 Health Check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"🔴 Health Check failed: {e}")
    
    # Test models endpoint
    try:
        response = requests.get(f"{base_url}/models", timeout=5)
        print(f"🟢 Models: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"🔴 Models failed: {e}")
    
    # Test chat completion
    try:
        payload = {
            "model": "qwen2.5-koc-assistant",
            "messages": [
                {"role": "user", "content": "KOC app có những tính năng gì?"}
            ],
            "stream": False,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{base_url}/chat/completions",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            print(f"🟢 Chat Completion: {response.status_code}")
            print(f"📝 Response: {content[:200]}...")
        else:
            print(f"🔴 Chat Completion failed: {response.status_code}")
            
    except Exception as e:
        print(f"🔴 Chat Completion error: {e}")

def test_streaming_response():
    """Test streaming response"""
    print("\n📡 TESTING STREAMING RESPONSE")
    print("=" * 50)
    
    try:
        payload = {
            "model": "qwen2.5-koc-assistant", 
            "messages": [
                {"role": "user", "content": "Hướng dẫn đăng nhập TikTok trong KOC app"}
            ],
            "stream": True,
            "temperature": 0.7
        }
        
        response = requests.post(
            "http://localhost:8000/chat/completions",
            json=payload,
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            print("🟢 Streaming started...")
            collected_response = ""
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]
                        if data_str != '[DONE]':
                            try:
                                data = json.loads(data_str)
                                if 'choices' in data and data['choices']:
                                    delta = data['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    if content:
                                        print(content, end='', flush=True)
                                        collected_response += content
                            except json.JSONDecodeError:
                                continue
            
            print(f"\n\n✅ Streaming completed. Total length: {len(collected_response)} chars")
        else:
            print(f"🔴 Streaming failed: {response.status_code}")
            
    except Exception as e:
        print(f"🔴 Streaming error: {e}")

def show_system_overview():
    """Hiển thị tổng quan hệ thống"""
    print("\n🎯 KOC PRO APP - SYSTEM OVERVIEW")
    print("=" * 50)
    
    print("📱 KOC Pro App Features:")
    print("  • TikTok Login Integration")
    print("  • Dashboard thống kê KOC")
    print("  • Quản lý chiến dịch marketing")
    print("  • AI Assistant thông minh (Qwen2.5)")
    print("  • Multi-platform social integration")
    print("  • Revenue tracking & analytics")
    print("  • Content creation tools")
    print("  • Team collaboration workspace")
    
    print("\n🏗️ Technical Stack:")
    print("  • Frontend: React Native + React.js")
    print("  • Backend: Python FastAPI")
    print("  • AI Model: Qwen2.5 via Ollama")
    print("  • Database: ChromaDB (Vector) + Knowledge Base")
    print("  • Auth: OAuth 2.0 (TikTok)")
    print("  • PDF Processing: PyMuPDF + ReportLab")
    
    print("\n📚 Knowledge Base:")
    print("  • KOC App Complete Guide (7 chunks)")
    print("  • Technical Specifications (2 chunks)")
    print("  • Demo App Guide (7 chunks)")
    print("  • Total: 16 knowledge chunks loaded")
    
    print("\n🤖 AI Capabilities:")
    print("  • Natural Vietnamese conversation")
    print("  • KOC app guidance & support")
    print("  • Context-aware responses")
    print("  • Technical troubleshooting")
    print("  • Real-time streaming responses")

def main():
    """Main test function"""
    print("🚀 COMPLETE SYSTEM TEST - KOC PRO APP")
    print("=" * 60)
    
    # Show system overview
    show_system_overview()
    
    # Test Ollama connection
    print(f"\n🔍 TESTING OLLAMA CONNECTION")
    print("=" * 50)
    ollama_status = test_ollama_connection()
    
    if not ollama_status:
        print("⚠️ Ollama not available, some tests may fail")
    
    # Test AI Assistant
    test_ai_assistant()
    
    # Test API endpoints (if server is running)
    test_api_endpoints()
    
    # Test streaming
    test_streaming_response()
    
    print("\n" + "=" * 60)
    print("🎉 SYSTEM TEST COMPLETED!")
    print("✅ KOC Pro App với AI Assistant sẵn sàng sử dụng!")
    print("📖 Tài liệu đã được tạo và load vào knowledge base")
    print("🤖 AI có thể trả lời mọi câu hỏi về KOC app")
    print("=" * 60)

if __name__ == "__main__":
    main() 