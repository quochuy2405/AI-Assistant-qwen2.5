# 🤖 AI KOC Support với Qwen2.5

Hệ thống AI hỗ trợ khách hàng thông minh sử dụng **Qwen2.5-7B-Instruct** local model.

## ✨ Tính Năng

### 🧠 AI Thông Minh
- **Qwen2.5-7B-Instruct**: Model AI tiên tiến của Alibaba
- **Local Processing**: Chạy hoàn toàn offline, bảo mật tuyệt đối
- **Vietnamese Support**: Tối ưu cho tiếng Việt
- **Context Aware**: Hiểu ngữ cảnh và trả lời thông minh

### 🚀 Performance
- **GPU Acceleration**: Tự động detect CUDA
- **Lazy Loading**: Load model khi cần thiết
- **Memory Efficient**: Tối ưu RAM và VRAM
- **Fallback System**: Backup responses khi model lỗi

## 📋 Yêu Cầu Hệ Thống

### 💻 Hardware
- **RAM**: Tối thiểu 16GB (khuyến nghị 32GB)
- **GPU**: NVIDIA GPU với 8GB+ VRAM (tùy chọn)
- **Storage**: 15GB+ cho model
- **CPU**: Multi-core processor

### 🐍 Software
- **Python**: 3.8+
- **CUDA**: 11.8+ (nếu dùng GPU)
- **Git LFS**: Để download model

## 🛠️ Cài Đặt

### 1. Clone Repository
```bash
git clone <your-repo>
cd AI-Support
```

### 2. Cài Dependencies
```bash
# Cài packages cần thiết
pip install -r requirements_api.txt

# Nếu có GPU NVIDIA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 3. Download Qwen2.5 Model

#### Option A: Từ HuggingFace (Recommended)
```bash
# Cài git-lfs nếu chưa có
git lfs install

# Clone model
git clone https://huggingface.co/Qwen/Qwen2.5-7B-Instruct
```

#### Option B: Từ Local Path
```bash
# Nếu bạn đã có model local
export QWEN_MODEL_PATH="/path/to/your/qwen2.5/model"
```

### 4. Cấu Hình Environment
```bash
# Tạo file .env
cp .env.example .env

# Chỉnh sửa path model
echo "QWEN_MODEL_PATH=./Qwen2.5-7B-Instruct" > .env
```

## 🚀 Chạy Hệ Thống

### 1. Start API Server
```bash
# Với auto-reload
python start_api_server.py --reload

# Production mode
python start_api_server.py --workers 4
```

### 2. Start Frontend
```bash
# Terminal mới
python start_frontend.py
```

### 3. Truy Cập
- **Chat Interface**: http://localhost:3000
- **API Demo**: http://localhost:3000/demo.html
- **API Docs**: http://localhost:8000/docs

## 🎯 Cách Sử Dụng

### 💬 Chat Interface
1. Mở http://localhost:3000
2. Nhập câu hỏi tiếng Việt
3. AI sẽ trả lời thông minh với Qwen2.5

### 🧪 Test API
```bash
curl -X POST "http://localhost:8000/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-assistant",
    "messages": [{"role": "user", "content": "Xin chào"}],
    "stream": false
  }'
```

### 📊 Streaming Response
```javascript
const response = await fetch('/chat/completions', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    model: 'qwen2.5-assistant',
    messages: [{role: 'user', content: 'App chạy chậm quá'}],
    stream: true
  })
});

// Process SSE stream
const reader = response.body.getReader();
// ... handle streaming
```

## ⚙️ Cấu Hình

### 🎛️ Model Settings
```python
# Trong api/responses.py
QWEN_MODEL_PATH = "./Qwen2.5-7B-Instruct"  # Model path
DEVICE = "cuda"  # hoặc "cpu"

# Generation parameters
max_new_tokens=300,
temperature=0.7,
do_sample=True
```

### 🔧 Performance Tuning
```python
# GPU Memory optimization
torch_dtype=torch.float16  # Cho GPU
torch_dtype=torch.float32  # Cho CPU

# Device mapping
device_map="auto"  # Tự động phân bổ GPU
```

## 🐛 Troubleshooting

### ❌ "CUDA out of memory"
```bash
# Giảm batch size hoặc dùng CPU
export CUDA_VISIBLE_DEVICES=""  # Force CPU
```

### ❌ "Model not found"
```bash
# Kiểm tra path model
ls -la ./Qwen2.5-7B-Instruct/
# Hoặc download lại
git clone https://huggingface.co/Qwen/Qwen2.5-7B-Instruct
```

### ❌ "Slow response"
```bash
# Kiểm tra GPU
nvidia-smi

# Hoặc dùng smaller model
# Qwen2.5-3B-Instruct thay vì 7B
```

## 📈 Performance Benchmarks

### 🖥️ Hardware Specs
| Component | Recommended | Minimum |
|-----------|-------------|---------|
| GPU | RTX 4090 24GB | GTX 1080 8GB |
| RAM | 32GB | 16GB |
| CPU | 16 cores | 8 cores |

### ⚡ Response Times
| Setup | First Load | Subsequent |
|-------|------------|------------|
| GPU (RTX 4090) | ~10s | ~2-3s |
| GPU (RTX 3080) | ~15s | ~3-5s |
| CPU (16 cores) | ~30s | ~10-15s |

## 🔄 Model Updates

### Cập Nhật Qwen2.5
```bash
cd Qwen2.5-7B-Instruct
git pull origin main
```

### Thay Đổi Model
```bash
# Trong .env
QWEN_MODEL_PATH=./Qwen2.5-14B-Instruct  # Larger model
# hoặc
QWEN_MODEL_PATH=./Qwen2.5-3B-Instruct   # Smaller model
```

## 🎨 Customization

### 🎯 System Prompt
```python
# Chỉnh sửa trong api/responses.py
SYSTEM_PROMPT = """
Bạn là AI Assistant chuyên nghiệp...
[Tùy chỉnh theo nhu cầu]
"""
```

### 🔧 Generation Parameters
```python
# Fine-tune response quality
temperature=0.7,      # Creativity (0.1-1.0)
max_new_tokens=300,   # Response length
do_sample=True,       # Enable sampling
top_p=0.9,           # Nucleus sampling
```

## 📚 API Documentation

### 🔗 Endpoints
- `GET /health` - Health check
- `GET /models` - Available models
- `POST /chat/completions` - Chat với AI
- `GET /stats` - System statistics

### 📝 Request Format
```json
{
  "model": "qwen2.5-assistant",
  "messages": [
    {"role": "user", "content": "Your question"}
  ],
  "stream": true,
  "temperature": 0.7,
  "max_tokens": 300
}
```

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push và tạo PR

## 📄 License

MIT License - Xem file LICENSE

---

## 🚀 Quick Start Commands

```bash
# 1. Setup
git clone <repo> && cd AI-Support
pip install -r requirements_api.txt
git clone https://huggingface.co/Qwen/Qwen2.5-7B-Instruct

# 2. Run
python start_api_server.py --reload  # Terminal 1
python start_frontend.py             # Terminal 2

# 3. Test
curl -X POST localhost:8000/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5","messages":[{"role":"user","content":"Xin chào"}]}'
```

**Ready to chat with Qwen2.5! 🤖✨** 