# 🚀 HƯỚNG DẪN SETUP NHANH - AI HỖ TRỢ KOC

## ⚡ Setup 1 dòng lệnh (Khuyên dùng)

```bash
chmod +x setup.sh && ./setup.sh
```

## 📋 Setup thủ công (Từng bước)

### 1️⃣ Cài đặt Ollama

**macOS:**
```bash
brew install ollama
brew services start ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve &
```

**Windows:** Tải từ https://ollama.com/download/windows

### 2️⃣ Tải model LLAMA

```bash
ollama pull llama2
```

### 3️⃣ Cài Python packages

```bash
pip install -r requirements.txt
```

### 4️⃣ Chạy app

```bash
python run_app.py
```

## 🌐 Truy cập

Mở trình duyệt: **http://localhost:8501**

## ✅ Kiểm tra cài đặt

```bash
# Kiểm tra Ollama
ollama list

# Kiểm tra Python packages
python -c "import streamlit, ollama; print('✅ OK')"

# Test app
python run_app.py
```

## 🐛 Xử lý lỗi nhanh

### Lỗi: "Cannot connect to Ollama"
```bash
ollama serve &
sleep 5
ollama pull llama2
```

### Lỗi: "Module not found"
```bash
pip install -r requirements.txt --force-reinstall
```

### Lỗi: "Model not found"
```bash
ollama list
ollama pull llama2
```

## 📁 Cấu trúc files quan trọng

```
AI-Support/
├── app.py              # App chính
├── requirements.txt    # Dependencies
├── setup.sh           # Script setup tự động
├── run_app.py         # Launcher với check
└── README_SETUP.md    # Hướng dẫn này
```

## 🎯 Sử dụng app

1. **Upload PDF** → Tab "Tải Tài Liệu"
2. **Chat AI** → Tab "Trò Chuyện"  
3. **Xem stats** → Tab "Thống Kê"

## 📞 Hỗ trợ

- **GitHub Issues:** Tạo issue mới
- **Email:** Gửi kèm log lỗi
- **Docs:** Xem README.md đầy đủ

---
⭐ **Chúc bạn setup thành công!** ⭐ 