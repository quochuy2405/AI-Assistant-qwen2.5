# 🤖 ZiZi AI - Trợ Lý AI Thông Minh

**ZiZi AI** là một hệ thống trợ lý AI thông minh được phát triển với Qwen2.5, hỗ trợ streaming chat và tích hợp knowledge base từ tài liệu text.

![ZiZi AI](https://img.shields.io/badge/ZiZi-AI-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red?style=for-the-badge)
![Qwen2.5](https://img.shields.io/badge/Qwen2.5-7B-orange?style=for-the-badge)

## ✨ Tính Năng Chính

- 🤖 **AI Assistant**: Sử dụng Qwen2.5 qua Ollama
- 💬 **Streaming Chat**: Trả lời real-time với SSE
- 📚 **Knowledge Base**: Tích hợp tài liệu training từ txt files
- 🌐 **Web UI**: Giao diện chat hiện đại, thân thiện
- 🔌 **REST API**: OpenAI-compatible endpoints
- 🇻🇳 **Tiếng Việt**: Hỗ trợ hoàn toàn tiếng Việt

## 🚀 Cài Đặt Nhanh

### 1. Yêu Cầu Hệ Thống
```bash
# Python 3.8+
python --version

# Ollama (để chạy Qwen2.5)
# Tải tại: https://ollama.ai
```

### 2. Setup Project
```bash
# Clone repository
git clone <repository-url>
cd AI-Support

# Cài đặt dependencies
pip install -r requirements_api.txt

# Cài đặt Ollama model
ollama pull qwen2.5:7b
```

### 3. Load Training Data
```bash
# Load tài liệu Zizi vào knowledge base
python load_zizi_training.py
```

### 4. Khởi Chạy Hệ Thống

#### Option 1: Full Stack (API + Frontend)
```bash
python run_zizi_ai.py
```

#### Option 2: Chạy Riêng Lẻ
```bash
# Terminal 1: API Server
python start_api_server.py

# Terminal 2: Frontend Server  
python start_frontend.py
```

## 🌐 Truy Cập

- **Frontend UI**: http://localhost:8501
- **API Server**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Cấu Trúc Project

```
ZiZi-AI/
├── 🤖 api/                          # API Backend
│   ├── models.py                    # Data models
│   ├── responses.py                 # AI response logic
│   ├── config.py                    # Configuration
│   └── utils.py                     # Utilities
├── 🌐 frontend/                     # Web Frontend
│   ├── index.html                   # Main chat UI
│   ├── chat.js                      # Chat functionality
│   └── style.css                    # Modern UI styles
├── 📚 knowledge_base.py             # Knowledge base management
├── 📄 huong-dan-su-dung-zizi-project-day-du.txt  # Training data
├── 🚀 start_api_server.py           # API launcher
├── 🌐 start_frontend.py             # Frontend launcher
├── 📖 load_zizi_training.py         # Training script
└── 🏃 run_zizi_ai.py               # Full stack launcher
```

## 🔌 API Endpoints

### Chat Completions
```bash
POST /chat/completions
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "ZiZi project là gì?"}
  ],
  "stream": true
}
```

### Health Check
```bash
GET /health
```

### Models List
```bash
GET /models
```

### Statistics
```bash
GET /stats
```

## 💬 Cách Sử Dụng

### 1. Chat với ZiZi AI
- Mở http://localhost:8501
- Nhập câu hỏi về Zizi Project
- Nhận phản hồi thông minh với knowledge base

### 2. API Integration
```python
import requests

response = requests.post("http://localhost:8000/chat/completions", 
    json={
        "messages": [{"role": "user", "content": "Hướng dẫn cài đặt Zizi?"}],
        "stream": False
    })

print(response.json())
```

### 3. Streaming Chat
```javascript
const eventSource = new EventSource('/chat/completions?stream=true');
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log(data.choices[0].delta.content);
};
```

## 🛠️ Configuration

### API Settings (api/config.py)
```python
# Ollama settings
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "qwen2.5:7b"

# API settings  
API_HOST = "0.0.0.0"
API_PORT = 8000
```

### Frontend Settings (start_frontend.py)
```python
# Frontend server
FRONTEND_PORT = 8501
```

## 📚 Knowledge Base

ZiZi AI sử dụng ChromaDB để lưu trữ và tìm kiếm knowledge base:

- **Embedding**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **Vector Store**: ChromaDB
- **Chunking**: 1000 characters với overlap 200

### Thêm Tài Liệu Mới
```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()
kb.load_txt("new_document.txt")
```

## 🔧 Troubleshooting

### Lỗi Ollama Connection
```bash
# Kiểm tra Ollama running
ollama list

# Restart Ollama
ollama serve
```

### Lỗi Knowledge Base
```bash
# Reset knowledge base
rm -rf chroma_db/
python load_zizi_training.py
```

### Lỗi Port Conflicts
```bash
# Kiểm tra port sử dụng
lsof -i :8000
lsof -i :8501

# Kill process
kill -9 <PID>
```

## 🤝 Contributing

1. Fork project
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Contact

**ZiZi AI Team**
- 📧 Email: support@zizi-ai.com
- 🌐 Website: https://zizi-ai.com
- 📱 Discord: ZiZi AI Community

## 🙏 Acknowledgments

- [Qwen2.5](https://github.com/QwenLM/Qwen2.5) - Powerful LLM
- [Ollama](https://ollama.ai) - Local LLM runtime
- [FastAPI](https://fastapi.tiangolo.com) - Modern API framework
- [ChromaDB](https://www.trychroma.com) - Vector database
- [Streamlit](https://streamlit.io) - Web UI framework

---

<div align="center">
  <strong>🤖 ZiZi AI - Trợ Lý AI Thông Minh Cho Mọi Người 🇻🇳</strong>
</div> 