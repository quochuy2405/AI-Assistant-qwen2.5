import streamlit as st
import tempfile
import os
from pathlib import Path
import json
from datetime import datetime
import re
from collections import Counter

# Import các module tự tạo
from pdf_processor import PDFProcessor
from knowledge_base import KnowledgeBase

# Câu trả lời mẫu cho các câu hỏi thường gặp
PREDEFINED_RESPONSES = {
    "đăng ký": "📝 **Hướng dẫn đăng ký tài khoản:**\n\n1. 🔗 Mở app và tìm nút 'Đăng ký'\n2. 📧 Nhập email và mật khẩu\n3. 📱 Xác nhận qua SMS hoặc email\n4. ✅ Hoàn thành thông tin cá nhân\n\n💡 **Lưu ý:** Mật khẩu nên có ít nhất 8 ký tự!",
    
    "đăng nhập": "🔐 **Hướng dẫn đăng nhập:**\n\n1. 📱 Mở app\n2. 📧 Nhập email/số điện thoại\n3. 🔑 Nhập mật khẩu\n4. 👆 Nhấn 'Đăng nhập'\n\n❓ **Quên mật khẩu?** Nhấn 'Quên mật khẩu' để đặt lại!",
    
    "thanh toán": "💳 **Hướng dẫn thanh toán:**\n\n**Phương thức hỗ trợ:**\n• 💳 Thẻ tín dụng/ghi nợ\n• 🏦 Chuyển khoản ngân hàng\n• 📱 Ví điện tử (Momo, ZaloPay)\n• 💰 Thanh toán khi nhận hàng\n\n**Các bước:**\n1. Chọn sản phẩm → Giỏ hàng\n2. Chọn phương thức thanh toán\n3. Nhập thông tin thanh toán\n4. Xác nhận đơn hàng",
    
    "đổi mật khẩu": "🔒 **Hướng dẫn đổi mật khẩu:**\n\n1. 👤 Vào 'Tài khoản của tôi'\n2. ⚙️ Chọn 'Cài đặt bảo mật'\n3. 🔑 Nhấn 'Đổi mật khẩu'\n4. 📝 Nhập mật khẩu cũ\n5. 🆕 Nhập mật khẩu mới (2 lần)\n6. ✅ Lưu thay đổi\n\n🛡️ **Bảo mật:** Dùng mật khẩu mạnh với chữ, số và ký tự đặc biệt!",
    
    "quên mật khẩu": "🔓 **Khôi phục mật khẩu:**\n\n1. 📱 Ở màn hình đăng nhập, nhấn 'Quên mật khẩu'\n2. 📧 Nhập email đã đăng ký\n3. 📨 Kiểm tra email nhận link reset\n4. 🔗 Click link trong email\n5. 🆕 Tạo mật khẩu mới\n6. ✅ Đăng nhập với mật khẩu mới",
    
    "cập nhật": "🔄 **Cập nhật ứng dụng:**\n\n**Android:**\n1. 📱 Mở CH Play\n2. 🔍 Tìm tên app\n3. 🔄 Nhấn 'Cập nhật'\n\n**iOS:**\n1. 📱 Mở App Store\n2. 👤 Vào tab 'Cập nhật'\n3. 🔄 Tìm app và cập nhật\n\n✨ **Lưu ý:** Luôn cập nhật để có tính năng mới nhất!",
    
    "liên hệ": "📞 **Thông tin liên hệ hỗ trợ:**\n\n📧 **Email:** support@yourapp.com\n📱 **Hotline:** 1900-xxxx\n💬 **Chat:** Trong app → Menu → 'Hỗ trợ'\n🕐 **Giờ làm việc:** 8:00 - 22:00 (T2-CN)\n\n🚀 **Phản hồi nhanh:** Dùng chat trong app!"
}

def main():
    st.set_page_config(
        page_title="AI Hỗ Trợ KOC - Offline Mode",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 AI Hỗ Trợ KOC - Offline Mode")
    st.markdown("**Phiên bản không cần API key - Tìm kiếm thông minh trong tài liệu**")
    
    # Sidebar cho cấu hình
    with st.sidebar:
        st.header("⚙️ Chế Độ Offline")
        st.success("✅ Hoạt động không cần internet")
        st.info("🔍 Tìm kiếm trong tài liệu đã tải")
        st.info("🤖 Câu trả lời thông minh sẵn có")
        
        st.markdown("---")
        st.subheader("💡 Câu Hỏi Thường Gặp")
        for topic in PREDEFINED_RESPONSES.keys():
            st.text(f"• {topic.title()}")
    
    # Tab chính
    tab1, tab2, tab3 = st.tabs(["📚 Tải Tài Liệu", "💬 Trò Chuyện", "📊 Thống Kê"])
    
    with tab1:
        handle_document_upload()
    
    with tab2:
        handle_chat_interface_offline()
    
    with tab3:
        handle_statistics()

def handle_document_upload():
    """Xử lý upload và học tài liệu PDF"""
    st.header("📚 Tải Tài Liệu Hướng Dẫn")
    
    uploaded_files = st.file_uploader(
        "Chọn file PDF hướng dẫn app:",
        type=['pdf'],
        accept_multiple_files=True,
        help="Có thể tải lên nhiều file PDF cùng lúc"
    )
    
    if uploaded_files:
        st.success(f"Đã chọn {len(uploaded_files)} file(s)")
        
        if st.button("🔄 Xử Lý và Học Tài Liệu", type="primary"):
            process_documents(uploaded_files)

def process_documents(uploaded_files):
    """Xử lý và học các tài liệu PDF"""
    processor = PDFProcessor()
    knowledge_base = KnowledgeBase()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_files = len(uploaded_files)
    
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Đang xử lý {uploaded_file.name}...")
        
        # Lưu file tạm
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        try:
            # Trích xuất text từ PDF
            text_chunks = processor.extract_and_chunk_pdf(tmp_path)
            
            # Thêm vào knowledge base
            knowledge_base.add_documents(text_chunks, uploaded_file.name)
            
            progress_bar.progress((i + 1) / total_files)
            
        except Exception as e:
            st.error(f"Lỗi xử lý {uploaded_file.name}: {str(e)}")
        finally:
            # Xóa file tạm
            os.unlink(tmp_path)
    
    status_text.text("✅ Hoàn thành!")
    st.success("Đã học xong tất cả tài liệu!")

def handle_chat_interface_offline():
    """Xử lý giao diện chat offline"""
    st.header("💬 Trò Chuyện với AI Assistant (Offline)")
    
    # Khởi tạo chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Hiển thị lịch sử chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Input cho câu hỏi mới
    if prompt := st.chat_input("Hỏi về hướng dẫn app..."):
        # Thêm câu hỏi của user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Tạo phản hồi offline
        with st.chat_message("assistant"):
            with st.spinner("🔍 Đang tìm kiếm..."):
                response = get_offline_response(prompt)
                st.markdown(response)
            
        # Thêm phản hồi vào lịch sử
        st.session_state.messages.append({"role": "assistant", "content": response})

def get_offline_response(question):
    """Tạo phản hồi offline thông minh"""
    
    question_lower = question.lower()
    
    # 1. Kiểm tra câu trả lời sẵn có
    for keyword, response in PREDEFINED_RESPONSES.items():
        if keyword in question_lower:
            return f"🤖 **Trả lời từ kiến thức sẵn có:**\n\n{response}"
    
    # 2. Tìm kiếm trong tài liệu đã tải
    try:
        knowledge_base = KnowledgeBase()
        context_docs = knowledge_base.search(question, k=3)
        
        if context_docs:
            # Tạo phản hồi từ context
            context_text = "\n\n".join([f"📄 **{doc.get('source', 'Tài liệu')}:**\n{doc['content']}" for doc in context_docs])
            
            response = f"🔍 **Tìm thấy thông tin liên quan:**\n\n{context_text}\n\n"
            response += "💡 **Gợi ý:** Dựa vào thông tin trên để thực hiện theo hướng dẫn."
            
            return response
            
    except Exception as e:
        pass
    
    # 3. Phản hồi mặc định với gợi ý
    suggestions = generate_suggestions(question_lower)
    
    response = f"🤔 **Xin lỗi, tôi cần thêm thông tin để trả lời chính xác về '{question}'**\n\n"
    
    if suggestions:
        response += "💡 **Có thể bạn muốn hỏi về:**\n"
        for suggestion in suggestions:
            response += f"• {suggestion}\n"
    
    response += "\n📚 **Để được hỗ trợ tốt hơn:**\n"
    response += "• Tải lên tài liệu PDF hướng dẫn ở tab '📚 Tải Tài Liệu'\n"
    response += "• Sử dụng từ khóa cụ thể hơn\n"
    response += "• Xem các câu hỏi thường gặp ở sidebar"
    
    return response

def generate_suggestions(question_lower):
    """Tạo gợi ý dựa trên câu hỏi"""
    suggestions = []
    
    keywords_map = {
        ["tài khoản", "account"]: "Đăng ký/Đăng nhập tài khoản",
        ["mật khẩu", "password"]: "Đổi mật khẩu hoặc quên mật khẩu", 
        ["thanh toán", "payment", "tiền"]: "Các phương thức thanh toán",
        ["lỗi", "error", "không hoạt động"]: "Khắc phục lỗi ứng dụng",
        ["cập nhật", "update"]: "Cập nhật phiên bản mới",
        ["hỗ trợ", "help", "liên hệ"]: "Thông tin liên hệ hỗ trợ"
    }
    
    for keywords, suggestion in keywords_map.items():
        if any(keyword in question_lower for keyword in keywords):
            suggestions.append(suggestion)
    
    return suggestions[:3]  # Tối đa 3 gợi ý

def handle_statistics():
    """Hiển thị thống kê sử dụng"""
    st.header("📊 Thống Kê Sử Dụng")
    
    knowledge_base = KnowledgeBase()
    stats = knowledge_base.get_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Số tài liệu", stats.get('total_documents', 0))
    
    with col2:
        st.metric("Số đoạn text", stats.get('total_chunks', 0))
    
    with col3:
        st.metric("Số câu hỏi đã trả lời", len(st.session_state.get('messages', [])) // 2)
    
    # Hiển thị danh sách tài liệu
    if stats.get('documents'):
        st.subheader("📋 Danh Sách Tài Liệu")
        for doc in stats['documents']:
            st.text(f"• {doc}")
    
    # Offline Info
    st.subheader("🔧 Thông Tin Hệ Thống")
    st.info("🔍 Chế độ: Offline - Không cần API key")
    st.info("🤖 AI: Rule-based + Document search")
    st.info("🌐 Deployment: Streamlit Cloud compatible")
    
    # Quick Help
    st.subheader("💡 Hướng Dẫn Nhanh")
    st.markdown("""
    **Để có trải nghiệm tốt nhất:**
    1. 📚 Tải lên file PDF hướng dẫn ở tab đầu tiên
    2. 💬 Hỏi câu hỏi cụ thể trong tab chat
    3. 🔍 Sử dụng từ khóa rõ ràng (đăng ký, thanh toán, etc.)
    
    **Nâng cấp lên AI thật:**
    - Lấy Hugging Face API key miễn phí
    - Sử dụng `app_cloud.py` thay vì file này
    """)

if __name__ == "__main__":
    main() 