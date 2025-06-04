#!/usr/bin/env python3
import sys
import os
import time
import requests

# Add current directory to path
sys.path.append('.')

try:
    from api.responses import (
        get_smart_response, 
        test_ollama_connection,
        clear_cache,
        RESPONSE_CACHE,
        get_quick_pattern_response
    )
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Chạy test cơ bản...")

def test_speed_improvements():
    """Test các cải tiến tốc độ"""
    print("🚀 **TEST TỐC ĐỘ AI RESPONSE**\n")
    
    # Test quick pattern responses
    print("1️⃣ **Quick Pattern Matching:**")
    test_questions = [
        "xin chào",
        "app chậm quá", 
        "cách đăng ký",
        "thanh toán như thế nào"
    ]
    
    for question in test_questions:
        start = time.time()
        try:
            response = get_quick_pattern_response(question.lower())
            end = time.time()
            
            if response:
                print(f"   ⚡ '{question}' → {(end-start)*1000:.1f}ms")
                print(f"      {response[:50]}...")
            else:
                print(f"   ⏭️ '{question}' → No quick match")
        except:
            print(f"   ❌ Error testing: {question}")
    
    print("\n2️⃣ **Cache Performance:**")
    
    # Test cache
    test_question = "xin chào bạn"
    
    # First call (no cache)
    start = time.time()
    try:
        response1 = get_smart_response(test_question)
        end = time.time()
        first_call_time = end - start
        print(f"   🔄 First call: {first_call_time:.2f}s")
    except Exception as e:
        print(f"   ❌ First call error: {e}")
        return
    
    # Second call (with cache)
    start = time.time()
    try:
        response2 = get_smart_response(test_question)
        end = time.time()
        cached_call_time = end - start
        print(f"   ⚡ Cached call: {cached_call_time:.3f}s")
        
        if cached_call_time < 0.01:
            print("   ✅ Cache hoạt động hoàn hảo!")
        
        speedup = first_call_time / cached_call_time if cached_call_time > 0 else float('inf')
        print(f"   📈 Speedup: {speedup:.1f}x faster")
        
    except Exception as e:
        print(f"   ❌ Cached call error: {e}")
    
    print(f"\n3️⃣ **Cache Status:**")
    print(f"   📦 Cached responses: {len(RESPONSE_CACHE)}")
    if RESPONSE_CACHE:
        print("   🔑 Cached keys:")
        for key in list(RESPONSE_CACHE.keys())[:3]:
            print(f"      • {key[:30]}...")

def test_ollama_speed():
    """Test Ollama connection và model speed"""
    print("\n4️⃣ **Ollama Performance:**")
    
    try:
        success = test_ollama_connection()
        return success
    except Exception as e:
        print(f"   ❌ Ollama test error: {e}")
        return False

def show_optimization_summary():
    """Hiển thị tóm tắt tối ưu"""
    print("\n" + "="*50)
    print("📊 **TÓM TẮT TỐI ƯU HÓA**")
    print("="*50)
    
    optimizations = [
        ("⚡ Quick Pattern Match", "Instant response cho câu hỏi phổ biến"),
        ("💾 Response Cache", "Lưu trữ để tái sử dụng"),
        ("🎯 Model Parameters", "num_predict: 100→80, temp: 0.7→0.3"),
        ("⏱️ Timeout Reduction", "Connection: 5s→2s, API: 30s→15s"),
        ("📝 Shorter Prompts", "System prompt ngắn gọn hơn"),
        ("🔍 Limited Search", "Knowledge base results: 3→2")
    ]
    
    for title, desc in optimizations:
        print(f"{title:<25} {desc}")
    
    print("\n🎯 **KẾT QUẢ MONG ĐỢI:**")
    print("• Response time: < 3s (tốt) | < 8s (trung bình)")
    print("• Quick patterns: < 10ms")
    print("• Cached responses: < 5ms")
    print("• Fallback responses: Instant")

if __name__ == "__main__":
    try:
        test_speed_improvements()
        test_ollama_speed()
        show_optimization_summary()
        
        print(f"\n🧪 **TEST HOÀN TẤT!**")
        print("💡 Chạy lại để thấy cache performance!")
        
    except KeyboardInterrupt:
        print("\n\n⏸️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Vẫn có thể test cơ bản...") 