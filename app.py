import streamlit as st
import ollama
import tempfile
import os
from pathlib import Path
import json
from datetime import datetime

# Import các module tự tạo
from pdf_processor import PDFProcessor
from knowledge_base import KnowledgeBase
from ai_assistant import AIAssistant

# Prompt tối ưu cho Qwen2.5 và hướng dẫn tiếng Việt
OPTIMIZED_SYSTEM_PROMPT = """Bạn là một trợ lý AI thông minh chuyên hướng dẫn sử dụng ứng dụng. 

QUAN TRỌNG: 
- LUÔN trả lời bằng tiếng Việt
- Đưa ra hướng dẫn rõ ràng, từng bước
- Sử dụng thông tin từ tài liệu đã được tải lên
- Nếu không có thông tin, hãy nói "Tôi cần thêm thông tin để trả lời chính xác"

Phong cách trả lời:
- Thân thiện và dễ hiểu
- Chia thành các bước cụ thể
- Đưa ra ví dụ khi cần thiết
- Sử dụng emoji để làm rõ ràng hơn"""

def main():
    st.set_page_config(
        page_title="AI Hỗ Trợ KOC - Hướng Dẫn App",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 AI Hỗ Trợ KOC - Hướng Dẫn App")
    st.markdown("**Sử dụng LLAMA miễn phí để trả lời câu hỏi về hướng dẫn app**")
    
    # Sidebar cho cấu hình
    with st.sidebar:
        st.header("⚙️ Cấu Hình")
        
        # Kiểm tra Ollama
        if check_ollama_connection():
            st.success("✅ Ollama đã kết nối")
        else:
            st.error("❌ Không thể kết nối Ollama")
            st.info("Hãy cài đặt và chạy Ollama trước")
            return
        
        # Chọn model
        available_models = get_available_models()
        if available_models:
            selected_model = st.selectbox(
                "Chọn Model LLAMA:",
                available_models,
                index=0  # Luôn chọn model đầu tiên trong danh sách
            )
            st.info(f"🤖 Đang sử dụng: {selected_model}")
        else:
            st.error("Không tìm thấy model nào")
            return
    
    # Tab chính
    tab1, tab2, tab3 = st.tabs(["📚 Tải Tài Liệu", "💬 Trò Chuyện", "📊 Thống Kê"])
    
    with tab1:
        handle_document_upload(selected_model)
    
    with tab2:
        handle_chat_interface(selected_model)
    
    with tab3:
        handle_statistics()

def check_ollama_connection():
    """Kiểm tra kết nối với Ollama"""
    try:
        response = ollama.list()
        return True
    except Exception:
        return False

def get_available_models():
    """Lấy danh sách models có sẵn"""
    try:
        response = ollama.list()
        models = []
        for model in response.models:
            if hasattr(model, 'name'):
                models.append(model.name)
            elif hasattr(model, 'model'):
                models.append(model.model)
            elif isinstance(model, dict):
                models.append(model.get('name', model.get('model', 'unknown')))
        
        # Ưu tiên Qwen và các model tốt
        qwen_models = [m for m in models if 'qwen' in m.lower()]
        llama_models = [m for m in models if 'llama' in m.lower()]
        other_models = [m for m in models if 'qwen' not in m.lower() and 'llama' not in m.lower()]
        
        return qwen_models + llama_models + other_models
        
    except Exception as e:
        print(f"Error getting models: {e}")  # Debug
        # Fallback với models đã cài đặt
        return ["qwen2.5:7b", "llama2:7b-chat", "llama2:latest"]

def handle_document_upload(model_name):
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
            process_documents(uploaded_files, model_name)

def process_documents(uploaded_files, model_name):
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

def handle_chat_interface(model_name):
    """Xử lý giao diện chat với KOC"""
    st.header("💬 Trò Chuyện với AI Assistant")
    
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
        
        # Tạo phản hồi từ AI
        with st.chat_message("assistant"):
            response = get_ai_response(prompt, model_name)
            st.markdown(response)
            
        # Thêm phản hồi vào lịch sử
        st.session_state.messages.append({"role": "assistant", "content": response})

def get_ai_response(question, model_name):
    """Lấy phản hồi từ AI với Qwen2.5 tối ưu hóa"""
    
    # Context từ tài liệu
    context_docs = KnowledgeBase().search(question, k=5)
    
    # Tạo prompt optimized cho Qwen
    messages = [
        {
            "role": "system", 
            "content": OPTIMIZED_SYSTEM_PROMPT
        }
    ]
    
    # Thêm lịch sử hội thoại (giới hạn 2 lượt gần nhất)
    conversation_history = st.session_state.messages[-4:] if "messages" in st.session_state else []
    for msg in conversation_history:
        messages.append(msg)
    
    # Context message
    if context_docs:
        context = "\n".join([doc['content'] for doc in context_docs])
        messages.append({
            "role": "system",
            "content": f"Thông tin tham khảo từ tài liệu:\n{context}"
        })
    
    # Câu hỏi người dùng
    messages.append({
        "role": "user",
        "content": question
    })
    
    try:
        # Tối ưu hóa cho Qwen2.5
        response = ollama.chat(
            model=model_name,
            messages=messages,
            options={
                "temperature": 0.3,
                "top_p": 0.9,
                "num_predict": 400,
                "repeat_penalty": 1.1
            }
        )
        
        if response:
            answer = response.get('message', {}).get('content', '')
            
            # Đảm bảo luôn có tiếng Việt
            if answer and not any(ord(char) > 127 for char in answer[:50]):
                answer = "Xin chào! 😊 " + answer
                
            return answer
        else:
            return "❌ Lỗi kết nối với AI. Vui lòng thử lại."
            
    except Exception as e:
        return f"❌ Có lỗi xảy ra: {str(e)}"

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

if __name__ == "__main__":
    main() 