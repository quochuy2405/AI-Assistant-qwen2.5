#!/bin/bash

echo "🚀 SETUP AI HỖ TRỢ KOC - HOÀN CHỈNH"
echo "===================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check OS
OS="Unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="Mac"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
fi

print_info "Hệ điều hành: $OS"
echo ""

# Step 1: Check Python
echo "🐍 Bước 1: Kiểm tra Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_status "Python3 đã cài đặt: $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    print_status "Python đã cài đặt: $PYTHON_VERSION"
else
    print_error "Python chưa cài đặt!"
    print_info "Hãy cài đặt Python 3.8+ trước khi tiếp tục"
    exit 1
fi
echo ""

# Step 2: Install Ollama
echo "🤖 Bước 2: Cài đặt Ollama..."
if command -v ollama &> /dev/null; then
    print_status "Ollama đã cài đặt"
else
    print_info "Đang cài đặt Ollama..."
    if [ "$OS" = "Mac" ]; then
        if command -v brew &> /dev/null; then
            brew install ollama
        else
            print_error "Cần Homebrew để cài đặt. Hoặc tải từ: https://ollama.com/download/macos"
            exit 1
        fi
    elif [ "$OS" = "Linux" ]; then
        curl -fsSL https://ollama.com/install.sh | sh
    else
        print_error "Tải thủ công từ: https://ollama.com/download"
        exit 1
    fi
fi

# Verify Ollama installation
if command -v ollama &> /dev/null; then
    print_status "Ollama đã sẵn sàng"
else
    print_error "Cài đặt Ollama thất bại"
    exit 1
fi
echo ""

# Step 3: Start Ollama
echo "🚀 Bước 3: Khởi động Ollama..."
if [ "$OS" = "Mac" ]; then
    brew services start ollama
    sleep 3
else
    ollama serve &
    sleep 5
fi

if ollama list &> /dev/null; then
    print_status "Ollama đang chạy"
else
    print_warning "Ollama có thể chưa sẵn sàng, nhưng tiếp tục..."
fi
echo ""

# Step 4: Install LLAMA model
echo "📦 Bước 4: Cài đặt model LLAMA..."
print_info "Đang tải model llama2 (khuyên dùng)..."
ollama pull llama2

if ollama list | grep -q llama2; then
    print_status "Model llama2 đã sẵn sàng"
else
    print_error "Tải model thất bại"
    exit 1
fi
echo ""

# Step 5: Install Python dependencies
echo "📦 Bước 5: Cài đặt Python packages..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        print_status "Dependencies đã cài đặt"
    else
        print_error "Cài đặt dependencies thất bại"
        exit 1
    fi
else
    print_error "Không tìm thấy requirements.txt"
    exit 1
fi
echo ""

# Step 6: Test setup
echo "🧪 Bước 6: Test cài đặt..."
python -c "
try:
    import streamlit
    import ollama
    from sentence_transformers import SentenceTransformer
    print('✅ Import thành công')
except ImportError as e:
    print(f'❌ Import thất bại: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    print_status "Tất cả packages hoạt động"
else
    print_error "Có package bị lỗi"
    exit 1
fi
echo ""

# Final success message
echo "🎉 SETUP HOÀN THÀNH!"
echo "==================="
echo ""
print_status "Tất cả đã sẵn sàng!"
echo ""
echo "📋 Để chạy ứng dụng:"
echo "   python run_app.py"
echo "   hoặc: streamlit run app.py"
echo ""
echo "🌐 Sau đó truy cập: http://localhost:8501"
echo ""
print_info "Lưu ý:"
echo "   - Upload file PDF trong tab 'Tải Tài Liệu'"
echo "   - Chat với AI trong tab 'Trò Chuyện'"
echo "   - Xem thống kê trong tab 'Thống Kê'"
echo ""

# Ask if want to run now
read -p "Có muốn chạy ứng dụng ngay bây giờ? (y/n): " run_now

if [[ $run_now == "y" || $run_now == "Y" ]]; then
    print_info "Đang khởi động ứng dụng..."
    python run_app.py
fi 