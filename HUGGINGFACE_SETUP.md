# 🆓 Hướng Dẫn Lấy Hugging Face API Key Miễn Phí

## 📋 **Các Bước Chi Tiết:**

### **Bước 1: Đăng Ký Tài Khoản**
1. Truy cập: https://huggingface.co/join
2. Đăng ký bằng email hoặc GitHub (miễn phí)
3. Xác nhận email

### **Bước 2: Lấy API Token**
1. Đăng nhập vào https://huggingface.co
2. Click vào avatar ở góc phải → **Settings**
3. Trong menu bên trái, click **"Access Tokens"**
4. Click **"New token"**
5. Đặt tên: `AI-Support-KOC`
6. Chọn **Role: Read** (đủ để sử dụng)
7. Click **"Generate a token"**
8. **COPY token** (chỉ hiện 1 lần!)

### **Bước 3: Cấu Hình Streamlit Cloud**
1. Vào GitHub repository của bạn
2. Deploy trên Streamlit Cloud
3. Trong **"Advanced settings"** → **"Secrets"**
4. Thêm: 
   ```
   HF_TOKEN = "hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ```
5. Deploy!

## ✨ **Lợi Ích Hugging Face API:**
- ✅ **Hoàn toàn miễn phí** 
- ✅ **Không giới hạn requests** cơ bản
- ✅ **Qwen2.5-7B** chất lượng cao
- ✅ **Không cần GPU** local
- ✅ **Stable deployment**

## 🔄 **Thay Thế Nếu Không Muốn Dùng API:**
Xem file `app_offline.py` cho phiên bản không cần API key! 