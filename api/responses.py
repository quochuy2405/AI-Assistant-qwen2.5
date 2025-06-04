# Import logic từ app hiện tại
from knowledge_base import KnowledgeBase
import os
import requests
import json
from typing import Optional

# Cấu hình Ollama - Tối ưu tốc độ
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
QWEN_MODEL_NAME = os.getenv("QWEN_MODEL_NAME", "qwen2.5:7b")

# Cache cho responses phổ biến (tăng tốc độ)
RESPONSE_CACHE = {}

# SMART_RESPONSES dictionary (để tương thích với import cũ)
SMART_RESPONSES = {
    "greeting": "Chào bạn! 😊 Mình là AI Assistant của KOC Support.",
    "slow_app": "😅 App chạy chậm hả bạn? Mình hướng dẫn fix ngay nhé!",
    "payment": "💳 Hỗ trợ thanh toán: Thẻ tín dụng, chuyển khoản, ví điện tử...",
    "register": "📝 Đăng ký tài khoản siêu dễ với 5 bước đơn giản!"
}

# System prompt ngắn gọn hơn - Tối ưu tốc độ
SYSTEM_PROMPT = """Bạn là AI Assistant của KOC Support.

NHIỆM VỤ: Trả lời ngắn gọn, thân thiện về hỗ trợ khách hàng

PHONG CÁCH:
- Dùng "mình" thay "tôi"
- Emoji phù hợp 
- Tối đa 350 từ
- Hướng dẫn cụ thể

CHỦ ĐỀ: đăng ký, đăng nhập, thanh toán, lỗi app, bảo mật."""

def check_ollama_connection() -> bool:
    """Kiểm tra kết nối Ollama - Timeout ngắn hơn"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2)  # Giảm từ 5s xuống 2s
        return response.status_code == 200
    except:
        return False

def get_smart_response(question: str) -> str:
    """AI thông minh với cache và tối ưu tốc độ"""
    question_lower = question.lower()
    
    # 1. Kiểm tra cache trước (siêu nhanh)
    cache_key = question_lower.strip()
    if cache_key in RESPONSE_CACHE:
        return RESPONSE_CACHE[cache_key]
    
    # 2. Quick pattern matching cho câu hỏi phổ biến
    quick_response = get_quick_pattern_response(question_lower)
    if quick_response:
        RESPONSE_CACHE[cache_key] = quick_response
        return quick_response
    
    # 3. Tìm kiếm trong knowledge base với multiple search terms
    try:
        knowledge_base = KnowledgeBase()
        context_docs = []
        
        # Thử nhiều search terms cho câu hỏi về chiến dịch
        if any(word in question_lower for word in ["chiến dịch", "campaign"]):
            search_terms = [
                question,  # Original question
                "chiến dịch review sản phẩm",  # Specific campaign type
                "loại chiến dịch",  # Types of campaigns
                "CÁC LOẠI CHIẾN DỊCH"  # Exact heading
            ]
            
            for term in search_terms:
                docs = knowledge_base.search(term, k=2)
                context_docs.extend(docs)
                # Nếu tìm được kết quả tốt (distance < 0.82), dừng tìm kiếm
                if docs and docs[0].get('distance', 1.0) < 0.82:
                    break
        else:
            # Search thông thường cho các câu hỏi khác
            context_docs = knowledge_base.search(question, k=2)
        
        if context_docs:
            # Loại bỏ duplicate và lấy unique content
            unique_contents = []
            seen_contents = set()
            for doc in context_docs:
                content_key = doc['content'][:100]  # First 100 chars as key
                if content_key not in seen_contents:
                    unique_contents.append(doc['content'][:800])  # Tăng lên 800 để thấy đủ 3 loại
                    seen_contents.add(content_key)
            
            context_text = "\n".join(unique_contents)
            
            enhanced_prompt = f"""Bạn là AI Assistant của KOC Support. Trả lời ngắn gọn và chính xác.

Context: {context_text}

Câu hỏi: {question}

Trả lời chỉ về câu hỏi được hỏi, không đưa thông tin thừa. Tối đa 100 từ."""

            response = get_ollama_response(enhanced_prompt)
            RESPONSE_CACHE[cache_key] = response
            return response
            
    except Exception as e:
        print(f"Knowledge base error: {e}")
    
    # 4. Dùng Qwen2.5 qua Ollama
    response = get_ollama_response(question)
    RESPONSE_CACHE[cache_key] = response
    return response

def get_quick_pattern_response(question_lower: str) -> Optional[str]:
    """Pattern matching nhanh cho câu hỏi phổ biến"""
    
    # Chỉ giữ lại chào hỏi cơ bản, còn lại để AI xử lý
    if any(word in question_lower for word in ["xin chào", "chào", "hello", "hi"]) and len(question_lower.split()) <= 3:
        return "Chào bạn! 😊 Mình là AI Assistant của KOC Support. Có gì cần hỗ trợ không?"
    
    # Loại bỏ tất cả hardcode patterns khác - để AI tự trả lời
    return None

def get_ollama_response(user_message: str) -> str:
    """Gọi Qwen2.5 qua Ollama API - Tối ưu tốc độ"""
    
    # Kiểm tra kết nối Ollama nhanh
    if not check_ollama_connection():
        return get_fallback_response(user_message)
    
    try:
        # Payload tối ưu tốc độ
        payload = {
            "model": QWEN_MODEL_NAME,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "stream": False,
            "options": {
                "temperature": 0.3,      # Giảm từ 0.7 - ít ngẫu nhiên hơn
                "num_predict": 150,      # Tăng từ 80 lên 150 để đủ content
                "top_p": 0.8,           # Giảm từ 0.9 - tập trung hơn
                "num_ctx": 1024,        # Giới hạn context
                "repeat_penalty": 1.1    # Tránh lặp từ
            }
        }
        
        # Gọi Ollama API với timeout ngắn
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=15  # Giảm từ 30s xuống 15s
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get("message", {}).get("content", "").strip()
            
            if ai_response:
                return ai_response
            else:
                return get_fallback_response(user_message)
        else:
            return get_fallback_response(user_message)
            
    except requests.RequestException:
        return get_fallback_response(user_message)
    except Exception:
        return get_fallback_response(user_message)

def get_fallback_response(question: str) -> str:
    """Fallback responses khi Ollama không khả dụng"""
    question_lower = question.lower()
    
    # Chào hỏi cơ bản
    greetings = ["xin chào", "chào", "hello", "hi", "hey"]
    if any(greeting in question_lower for greeting in greetings) and len(question_lower.split()) <= 3:
        return "Chào bạn! 😊 Mình là AI Assistant của KOC Support. Có gì mình có thể giúp bạn không?"
    
    # Default response - không hardcode các chủ đề cụ thể
    return f"""😊 Mình hiểu bạn hỏi về "{question}".

💡 **Mình có thể hỗ trợ nhiều vấn đề khác nhau:**
• 📝 Đăng ký và quản lý tài khoản
• 💳 Thanh toán và giao dịch  
• 🔧 Khắc phục lỗi kỹ thuật
• 🔐 Bảo mật và quyền riêng tư
• 📢 Chiến dịch và marketing
• 📞 Thông tin liên hệ

Bạn có thể hỏi cụ thể hơn hoặc diễn đạt lại câu hỏi không? Mình sẽ cố gắng hỗ trợ tốt nhất! 😊"""

# Các helper functions (giữ nguyên để tương thích)
def get_related_suggestions(question):
    """Gợi ý liên quan"""
    related_map = {
        "đăng ký": ["Đăng nhập", "Quên mật khẩu", "Xác thức tài khoản"],
        "thanh toán": ["Hoàn tiền", "Lịch sử giao dịch", "Phương thức thanh toán"],
        "lỗi": ["Cập nhật app", "Liên hệ hỗ trợ", "Khắc phục sự cố"],
        "mật khẩu": ["Bảo mật tài khoản", "Đăng nhập", "Xác thực 2 bước"]
    }
    
    for keyword, suggestions in related_map.items():
        if keyword in question:
            return suggestions[:2]
    
    return []

def get_additional_tips(keyword):
    """Tips bổ sung thân thiện"""
    tips_map = {
        "đăng ký": "🔐 Nhớ dùng email thật để nhận thông báo quan trọng nhé!",
        "thanh toán": "💳 Kiểm tra kỹ thông tin thẻ trước khi xác nhận",
        "mật khẩu": "🛡️ Bật xác thực 2 bước để bảo mật tối đa",
        "lỗi": "📱 Restart điện thoại thường xuyên để app chạy mượt hơn!",
        "liên hệ": "💬 Chat trong app sẽ được phản hồi nhanh nhất đấy!",
        "cập nhật": "🔔 Bật thông báo auto-update để không bỏ lỡ tính năng mới"
    }
    
    return tips_map.get(keyword, "")

def generate_smart_suggestions(question):
    """Tạo gợi ý thông minh"""
    suggestions = []
    
    # Enhanced keyword detection with casual phrases
    keywords_mapping = [
        (["tài khoản", "account", "user", "profile"], "Quản lý tài khoản và đăng nhập"),
        (["mật khẩu", "password", "pass", "khẩu"], "Đổi mật khẩu và bảo mật"),
        (["thanh toán", "payment", "tiền", "pay", "nạp"], "Các phương thức thanh toán"),
        (["lỗi", "error", "chậm", "lag", "crash", "giật"], "Khắc phục lỗi và app chậm"),
        (["cập nhật", "update", "mới", "upgrade"], "Cập nhật ứng dụng"),
        (["hỗ trợ", "help", "liên hệ", "support", "contact"], "Thông tin liên hệ và hỗ trợ"),
        (["tính năng", "feature", "chức năng", "có gì"], "Khám phá tính năng mới")
    ]
    
    for keywords, suggestion in keywords_mapping:
        if any(keyword in question for keyword in keywords):
            suggestions.append(suggestion)
    
    if not suggestions:
        suggestions = [
            "Hướng dẫn đăng ký tài khoản mới",
            "Khắc phục app chạy chậm", 
            "Cách thanh toán trong app"
        ]
    
    return suggestions[:3]

# Test function với kiểm tra tốc độ
def test_ollama_connection():
    """Test Ollama connection và đo tốc độ"""
    import time
    
    print(f"🔍 Testing Ollama connection...")
    print(f"📡 Base URL: {OLLAMA_BASE_URL}")
    print(f"🤖 Model: {QWEN_MODEL_NAME}")
    
    if check_ollama_connection():
        print("✅ Ollama đang chạy!")
        
        # Test tốc độ phản hồi
        start_time = time.time()
        test_response = get_ollama_response("Xin chào")
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"🧪 Test response: {test_response[:100]}...")
        print(f"⚡ Response time: {response_time:.2f}s")
        
        if response_time < 3:
            print("🚀 Tốc độ tốt!")
        elif response_time < 8:
            print("⚠️ Tốc độ trung bình")
        else:
            print("🐌 Cần tối ưu thêm")
            
        return True
    else:
        print("❌ Ollama không kết nối được. Kiểm tra:")
        print("   • ollama serve")
        print("   • ollama list")
        return False

def clear_cache():
    """Xóa cache để làm mới responses"""
    global RESPONSE_CACHE
    RESPONSE_CACHE.clear()
    print("🗑️ Cache đã được xóa!")

if __name__ == "__main__":
    test_ollama_connection() 