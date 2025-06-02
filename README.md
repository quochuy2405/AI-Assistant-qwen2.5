# 🤖 AI Hỗ Trợ KOC - Qwen2.5 Edition

**Hệ thống AI hỗ trợ KOC (Key Opinion Consumer) sử dụng Qwen2.5 để học từ tài liệu PDF và trả lời câu hỏi hướng dẫn app bằng tiếng Việt.**

## ✨ Tính Năng Chính

### 🧠 **AI Model: Qwen2.5-7B**
- **Đa ngôn ngữ xuất sắc** - Tiếng Việt tự nhiên
- **Instruction-following** - Hiểu và làm theo hướng dẫn chính xác  
- **Context window lớn** - Xử lý tài liệu dài
- **Reasoning mạnh** - Phân tích và giải thích chi tiết
- **Hoàn toàn miễn phí** - Chạy local, không cần internet

### 📚 **Xử Lý Tài Liệu**
- Upload nhiều file PDF cùng lúc
- Trích xuất và phân đoạn text thông minh
- Vector database với ChromaDB
- Tìm kiếm semantic với SentenceTransformer

### 💬 **Chat Interface**
- Giao diện thân thiện với Streamlit
- Chat real-time với AI
- Lịch sử hội thoại
- Context-aware responses

### 📊 **Thống Kê & Quản Lý**
- Theo dõi số lượng tài liệu
- Thống kê sử dụng
- Quản lý knowledge base

## 🚀 Cài Đặt Nhanh

### **Cách 1: Setup Tự Động (Khuyên dùng)**
```bash
chmod +x setup.sh && ./setup.sh
```

### **Cách 2: Từng Bước**

#### 1. Cài đặt Ollama và Qwen2.5
```bash
# macOS
brew install ollama
brew services start ollama

# Linux  
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &

# Tải model Qwen2.5
ollama pull qwen2.5:7b
```

#### 2. Cài đặt Python Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Chạy ứng dụng
```bash
python run_app.py
```

## 🌐 Sử Dụng

1. **Truy cập**: http://localhost:8501
2. **Tab "📚 Tải Tài Liệu"**: Upload file PDF hướng dẫn
3. **Tab "💬 Trò Chuyện"**: Chat với AI bằng tiếng Việt
4. **Tab "📊 Thống Kê"**: Xem thông tin sử dụng

## 🎯 Ví Dụ Câu Hỏi

- "Hướng dẫn đăng ký tài khoản mới"
- "Cách thanh toán trong app"  
- "Làm sao để đổi mật khẩu?"
- "Tính năng nào mới nhất?"

## 📦 Cấu Trúc Dự Án

```
AI-Support/
├── app.py                 # Ứng dụng Streamlit chính
├── ai_assistant.py        # AI Assistant với Qwen2.5
├── pdf_processor.py       # Xử lý PDF
├── knowledge_base.py      # Vector database
├── config.py             # Cấu hình
├── run_app.py            # Script khởi động
├── requirements.txt       # Dependencies
├── setup.sh              # Script setup tự động
├── install_ollama.sh     # Script cài Ollama
└── README.md             # Tài liệu này
```

## 🔧 Cấu Hình

### Models được hỗ trợ:
- **qwen2.5:7b** (Khuyên dùng - Tiếng Việt xuất sắc)
- llama3.1 (Chất lượng cao)
- mistral:instruct (Ổn định)
- phi3 (Nhỏ gọn)
- gemma2 (Google)

### Tối ưu hóa Qwen2.5:
- Temperature: 0.3 (ổn định)
- Max tokens: 400 (đầy đủ)
- Context search: 5 documents
- Vietnamese-optimized prompts

## 📋 Yêu Cầu Hệ Thống

- **Python**: 3.8+
- **RAM**: 8GB+ 
- **Disk**: 10GB+ (cho models)
- **OS**: Windows/macOS/Linux

## 🐛 Xử Lý Lỗi

### Lỗi Ollama không kết nối:
```bash
ollama serve
ollama pull qwen2.5:7b
```

### Lỗi Module not found:
```bash
pip install -r requirements.txt --force-reinstall
```

### Lỗi Model không tìm thấy:
```bash
ollama list
ollama pull qwen2.5:7b
```

## 🤝 Đóng Góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Hỗ Trợ

- **GitHub Issues**: Tạo issue mới
- **Email**: Gửi kèm log lỗi
- **Docs**: Xem README_SETUP.md cho hướng dẫn chi tiết

---

⭐ **Made with ❤️ for Vietnamese KOC Community**

🤖 **Powered by Qwen2.5 - The Best Open Source Model for Vietnamese** 🇻🇳 