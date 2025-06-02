# Import logic từ app hiện tại
from knowledge_base import KnowledgeBase
import os
import requests
import json
from typing import Optional

# Cấu hình Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
QWEN_MODEL_NAME = os.getenv("QWEN_MODEL_NAME", "qwen2.5:7b")

# SMART_RESPONSES dictionary (để tương thích với import cũ)
SMART_RESPONSES = {
    "greeting": "Chào bạn! 😊 Mình là AI Assistant của KOC Support.",
    "slow_app": "😅 App chạy chậm hả bạn? Mình hướng dẫn fix ngay nhé!",
    "payment": "💳 Hỗ trợ thanh toán: Thẻ tín dụng, chuyển khoản, ví điện tử...",
    "register": "📝 Đăng ký tài khoản siêu dễ với 5 bước đơn giản!"
}

# System prompt cho AI KOC Support
SYSTEM_PROMPT = """Bạn là AI Assistant của KOC Support - hệ thống hỗ trợ khách hàng thông minh.

NHIỆM VỤ:
- Trả lời câu hỏi của khách hàng một cách thân thiện, tự nhiên
- Hỗ trợ về: đăng ký, đăng nhập, thanh toán, bảo mật, lỗi app, tính năng
- Dùng tiếng Việt, giọng điệu thân thiện như bạn bè

PHONG CÁCH:
- Dùng "mình" thay vì "tôi" 
- Emoji phù hợp để tạo không khí vui vẻ
- Trả lời ngắn gọn, dễ hiểu (tối đa 200 từ)
- Đưa ra hướng dẫn cụ thể từng bước

VÍ DỤ TƯƠNG TÁC:
- "Xin chào" → "Chào bạn! 😊 Mình có thể giúp gì cho bạn hôm nay?"
- "App chậm" → "Ôi app chậm hả bạn? 😅 Mình hướng dẫn fix ngay nhé!"

Luôn hỏi thêm thông tin nếu cần để hỗ trợ tốt hơn."""

def check_ollama_connection() -> bool:
    """Kiểm tra kết nối Ollama"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_smart_response(question: str) -> str:
    """AI thông minh với Qwen2.5 qua Ollama"""
    question_lower = question.lower()
    
    # 1. Tìm kiếm trong knowledge base trước
    try:
        knowledge_base = KnowledgeBase()
        context_docs = knowledge_base.search(question, k=3)
        
        if context_docs:
            # Có tài liệu liên quan - dùng AI với context
            context_text = "\n".join([doc['content'][:500] for doc in context_docs])
            
            enhanced_prompt = f"""Dựa vào thông tin sau để trả lời câu hỏi:

THÔNG TIN TÀI LIỆU:
{context_text}

CÂU HỎI: {question}

Hãy trả lời dựa trên thông tin trên, nếu không có thông tin phù hợp thì trả lời theo kiến thức chung về hỗ trợ khách hàng."""

            return get_ollama_response(enhanced_prompt)
            
    except Exception as e:
        print(f"Knowledge base error: {e}")
    
    # 2. Dùng Qwen2.5 qua Ollama thuần túy
    return get_ollama_response(question)

def get_ollama_response(user_message: str) -> str:
    """Gọi Qwen2.5 qua Ollama API"""
    
    # Kiểm tra kết nối Ollama
    if not check_ollama_connection():
        print("⚠️ Ollama không khả dụng, dùng fallback response")
        return get_fallback_response(user_message)
    
    try:
        # Payload cho Ollama API
        payload = {
            "model": QWEN_MODEL_NAME,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 300,
                "top_p": 0.9
            }
        }
        
        # Gọi Ollama API
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get("message", {}).get("content", "").strip()
            
            if ai_response:
                return ai_response
            else:
                return get_fallback_response(user_message)
        else:
            print(f"Ollama API error: {response.status_code}")
            return get_fallback_response(user_message)
            
    except requests.RequestException as e:
        print(f"Ollama connection error: {e}")
        return get_fallback_response(user_message)
    except Exception as e:
        print(f"Ollama unexpected error: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(question: str) -> str:
    """Fallback responses khi Ollama không khả dụng"""
    question_lower = question.lower()
    
    # Chào hỏi cơ bản
    greetings = ["xin chào", "chào", "hello", "hi", "hey"]
    if any(greeting in question_lower for greeting in greetings):
        return "Chào bạn! 😊 Mình là AI Assistant của KOC Support. Có gì mình có thể giúp bạn không?"
    
    # Các từ khóa chính
    if any(word in question_lower for word in ["chậm", "lag", "giật", "lỗi"]):
        return """😅 App chạy chậm hả bạn? Mình hướng dẫn fix ngay:

🔧 **Thử ngay:**
• Tắt app và mở lại
• Restart điện thoại
• Kiểm tra mạng wifi/4G

💡 **Nếu vẫn chậm:**
• Xóa cache app trong Settings
• Cập nhật app lên bản mới nhất
• Giải phóng bộ nhớ điện thoại

Thử xem sao nhé! Còn chậm thì báo mình 😊"""

    if any(word in question_lower for word in ["đăng ký", "tạo tài khoản"]):
        return """📝 **Đăng ký tài khoản siêu dễ:**

1. Mở app → Tìm nút "Đăng ký"
2. Nhập email + mật khẩu (ít nhất 8 ký tự)
3. Xác nhận qua SMS/email
4. Điền thông tin cá nhân
5. Xong! 🎉

💡 **Lưu ý:** Dùng email thật để nhận thông báo quan trọng nhé!"""

    if any(word in question_lower for word in ["thanh toán", "payment", "trả tiền"]):
        return """💳 **Các cách thanh toán:**

🏦 **Hỗ trợ:**
• Thẻ tín dụng/ghi nợ
• Chuyển khoản ngân hàng  
• Ví điện tử (Momo, ZaloPay)
• COD (thanh toán khi nhận)

📱 **Cách thanh toán:**
1. Chọn sản phẩm → Giỏ hàng
2. Chọn phương thức thanh toán
3. Nhập thông tin
4. Xác nhận → Hoàn tất! ✅"""

    # Default response
    return f"""😊 Mình hiểu bạn hỏi về "{question}".

💡 **Mình có thể hỗ trợ:**
• 📝 Đăng ký/đăng nhập tài khoản
• 💳 Thanh toán và giao dịch  
• 🔧 Khắc phục lỗi app chậm
• 🔐 Bảo mật và đổi mật khẩu
• 📞 Thông tin liên hệ

Bạn có thể hỏi cụ thể hơn không? Ví dụ: "App chạy chậm" hoặc "Cách đăng ký" nhé! 😊"""

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

# Test function
def test_ollama_connection():
    """Test Ollama connection và model"""
    print(f"🔍 Testing Ollama connection...")
    print(f"📡 Base URL: {OLLAMA_BASE_URL}")
    print(f"🤖 Model: {QWEN_MODEL_NAME}")
    
    if check_ollama_connection():
        print("✅ Ollama đang chạy!")
        
        # Test model response
        test_response = get_ollama_response("Xin chào")
        print(f"🧪 Test response: {test_response[:100]}...")
        return True
    else:
        print("❌ Ollama không kết nối được. Kiểm tra:")
        print("   • ollama serve")
        print("   • ollama list")
        return False

if __name__ == "__main__":
    test_ollama_connection() 