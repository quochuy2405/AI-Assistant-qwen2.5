import requests
import json
import sseclient

def test_non_streaming():
    """Test API với non-streaming response"""
    print("🧪 Testing Non-Streaming API...")
    
    url = "http://localhost:8000/chat/completions"
    
    payload = {
        "model": "koc-assistant",
        "messages": [
            {"role": "user", "content": "Hướng dẫn đăng ký tài khoản"}
        ],
        "stream": False
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Non-Streaming Success!")
        print(f"📝 Response: {result['choices'][0]['message']['content'][:100]}...")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def test_streaming():
    """Test API với SSE streaming"""
    print("\n🧪 Testing Streaming API...")
    
    url = "http://localhost:8000/chat/completions"
    
    payload = {
        "model": "koc-assistant", 
        "messages": [
            {"role": "user", "content": "Làm sao để thanh toán bằng thẻ?"}
        ],
        "stream": True
    }
    
    try:
        response = requests.post(url, json=payload, stream=True)
        
        if response.status_code == 200:
            print("✅ Streaming Success!")
            print("📡 Receiving streaming response:")
            
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        data_str = line_str[6:]  # Remove 'data: '
                        
                        if data_str == '[DONE]':
                            print("\n🏁 Stream finished!")
                            break
                        
                        try:
                            data = json.loads(data_str)
                            if 'choices' in data and data['choices']:
                                delta = data['choices'][0].get('delta', {})
                                if 'content' in delta:
                                    print(delta['content'], end='', flush=True)
                        except json.JSONDecodeError:
                            pass
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")

def test_health():
    """Test health endpoint"""
    print("\n🧪 Testing Health Endpoint...")
    
    response = requests.get("http://localhost:8000/health")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Health Check Success!")
        print(f"📊 Status: {result['status']}")
        print(f"⏰ Timestamp: {result['timestamp']}")
    else:
        print(f"❌ Error: {response.status_code}")

def test_models():
    """Test models endpoint"""
    print("\n🧪 Testing Models Endpoint...")
    
    response = requests.get("http://localhost:8000/models")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Models Success!")
        print(f"📋 Available models: {[model['id'] for model in result['data']]}")
    else:
        print(f"❌ Error: {response.status_code}")

def test_stats():
    """Test stats endpoint"""
    print("\n🧪 Testing Stats Endpoint...")
    
    response = requests.get("http://localhost:8000/stats")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Stats Success!")
        print(f"📚 Documents: {result['total_documents']}")
        print(f"📝 Chunks: {result['total_chunks']}")
        print(f"🎯 Topics: {result['supported_topics']}")
        print(f"⚡ Response time: {result['response_time']}")
    else:
        print(f"❌ Error: {response.status_code}")

def main():
    """Chạy tất cả test cases"""
    print("🚀 AI KOC Support API Client Test")
    print("=" * 50)
    
    # Test các endpoint
    test_health()
    test_models()
    test_stats()
    test_non_streaming()
    test_streaming()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    main() 