# 🌐 AI KOC Support - Chat Interface

Giao diện web đẹp để tương tác với AI KOC Support API với tính năng streaming real-time.

## ✨ Tính Năng

### 🎯 Core Features
- **💬 Chat Interface**: Giao diện chat hiện đại giống ChatGPT
- **🔄 SSE Streaming**: Phản hồi real-time từ AI
- **📱 Responsive Design**: Tương thích mobile và desktop
- **🎨 Beautiful UI**: Thiết kế đẹp với gradient và animation

### 🚀 Interactive Features
- **⚡ Quick Questions**: Các câu hỏi nhanh được định sẵn
- **🔧 Streaming Toggle**: Bật/tắt chế độ streaming
- **📊 Real-time Stats**: Hiển thị thống kê API
- **🧪 API Testing**: Test các endpoint trực tiếp từ UI

### 💡 Smart Features
- **🤖 Typing Indicator**: Hiển thị khi AI đang trả lời
- **⏱️ Response Timing**: Đo thời gian phản hồi
- **📱 Auto-resize Input**: Textarea tự động điều chỉnh
- **🌐 Connection Status**: Hiển thị trạng thái kết nối

## 🚀 Cách Chạy

### 1. Chuẩn bị
```bash
# Make sure API server is running
python start_api_server.py --reload

# API sẽ chạy trên http://localhost:8000
```

### 2. Start Frontend Server
```bash
# Cách 1: Dùng Python script (Recommended)
python start_frontend.py

# Cách 2: Với custom port
python start_frontend.py --port 3001

# Cách 3: Không mở browser tự động
python start_frontend.py --no-browser
```

### 3. Truy cập Web Interface
- 🌍 URL: http://localhost:3000
- 🚀 Browser sẽ tự động mở
- 📱 Tương thích mobile/tablet

## 📁 Cấu Trúc Files

```
frontend/
├── index.html      # Main chat interface
├── style.css       # Beautiful styling
├── chat.js         # JavaScript logic + streaming
└── README.md       # This file
```

## 🎯 Cách Sử Dụng

### 💬 Chat Interface
1. **Nhập tin nhắn** vào ô input
2. **Enter** hoặc click **Send** để gửi
3. **AI sẽ phản hồi** streaming real-time
4. **Quick buttons** cho câu hỏi nhanh

### ⚡ Quick Questions
- 🐌 **"App chậm"** - Khắc phục app chậm
- 📝 **"Đăng ký"** - Hướng dẫn đăng ký
- 💳 **"Thanh toán"** - Cách thanh toán
- 🔐 **"Quên MK"** - Quên mật khẩu

### 🔧 Settings
- **Streaming Toggle**: Bật/tắt streaming mode
- **Test Buttons**: Test Health, Models, Stats API

## 🎨 UI Features

### 🌈 Design Elements
- **Gradient Background**: Purple-blue gradient
- **Glass Effect**: Backdrop blur cho modern look
- **Smooth Animations**: Fade in/out transitions
- **Responsive Layout**: Grid layout tự động

### 📱 Mobile Friendly
- **Touch Optimized**: Buttons và inputs thân thiện mobile
- **Auto Layout**: Sidebar ẩn trên mobile
- **Swipe Gestures**: Smooth scrolling

### 🎯 UX Features
- **Loading States**: Spinner khi đang gửi
- **Error Handling**: Thông báo lỗi user-friendly
- **Notifications**: Toast notifications cho actions
- **Connection Status**: Online/offline indicator

## 🔧 Customization

### 🎨 Thay đổi Theme
```css
/* Trong style.css, thay đổi gradient colors */
body {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### 🔗 Thay đổi API URL
```javascript
// Trong chat.js
this.apiBase = 'http://your-api-server:8000';
```

### ⚡ Quick Questions
```html
<!-- Trong index.html, thêm quick buttons -->
<button class="quick-btn" data-question="Your question">Button Text</button>
```

## 🧪 Testing Features

### 🩺 Health Check
- Click **Health** button
- Kiểm tra API server status

### 🧠 Models List
- Click **Models** button  
- Xem available models

### 📊 Stats Display
- Click **Stats** button
- Load real-time statistics

## 🌟 Tính Năng Nâng Cao

### 🔄 Streaming Mode
- **ON**: Real-time response streaming (default)
- **OFF**: Wait for complete response

### 📱 Auto-Features
- **Auto-scroll**: Tự động scroll xuống tin nhắn mới
- **Auto-resize**: Input tự động điều chỉnh height
- **Auto-connect**: Tự động kết nối lại khi mất mạng

### 🎯 Smart Formatting
- **Markdown Support**: Bold text, headers, lists
- **Emoji Display**: Native emoji rendering
- **Code Highlighting**: Inline code với background

## 🐛 Troubleshooting

### ❌ "Connection Failed"
```bash
# Check API server
python start_api_server.py --reload

# Check URL trong chat.js
this.apiBase = 'http://localhost:8000';
```

### 🔥 "Port Already in Use"
```bash
# Dùng port khác
python start_frontend.py --port 3001
```

### 📱 "Mobile Layout Issues"
- Refresh browser
- Clear cache (Ctrl+F5)
- Kiểm tra viewport meta tag

## 💡 Pro Tips

### ⚡ Performance
- Dùng **streaming mode** cho response nhanh hơn
- **Clear cache** nếu có vấn đề UI
- **Keep API server running** để tránh lỗi

### 🎯 Best Experience
- **Desktop browser** recommended
- **Chrome/Safari** for best compatibility
- **Fast internet** cho streaming smooth

### 🔧 Development
- F12 để mở DevTools
- Check Console để debug
- Network tab để monitor API calls

---

## 🚀 Quick Start Commands

```bash
# 1. Start API Server
python start_api_server.py --reload

# 2. Start Frontend (in new terminal)
python start_frontend.py

# 3. Open http://localhost:3000 và enjoy! 🎉
```

**Ready to chat with AI! 🤖💬** 