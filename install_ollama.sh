#!/bin/bash

# Script tự động cài đặt Ollama và LLAMA
# Cho dự án AI Hỗ Trợ KOC

echo "🤖 Cài Đặt AI Hỗ Trợ KOC - Ollama + LLAMA"
echo "==========================================="

# Detect OS
OS="Unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="Mac"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="Windows"
fi

echo "Hệ điều hành: $OS"

# Install Ollama based on OS
echo "📥 Đang cài đặt Ollama..."

if [ "$OS" = "Mac" ]; then
    # Check if Homebrew is available
    if command -v brew &> /dev/null; then
        echo "Sử dụng Homebrew để cài đặt..."
        brew install ollama
    else
        echo "❌ Homebrew không có. Hãy cài đặt thủ công:"
        echo "1. Truy cập: https://ollama.com/download/macos"
        echo "2. Tải file .dmg và cài đặt"
        echo "3. Chạy lại script này"
        exit 1
    fi
elif [ "$OS" = "Linux" ]; then
    curl -fsSL https://ollama.com/install.sh | sh
elif [ "$OS" = "Windows" ]; then
    echo "❌ Windows: Hãy tải từ https://ollama.com/download/windows"
    exit 1
else
    echo "❌ OS không được hỗ trợ: $OSTYPE"
    exit 1
fi

# Check if installation successful
if command -v ollama &> /dev/null; then
    echo "✅ Ollama đã cài đặt thành công"
else
    echo "❌ Cài đặt Ollama thất bại"
    exit 1
fi

# Start Ollama service
echo "🚀 Khởi động Ollama..."
if [ "$OS" = "Mac" ]; then
    brew services start ollama
else
    ollama serve &
    sleep 3
fi

# Install models
echo "📥 Đang tải model LLAMA..."
echo "Chọn model để tải (Khuyến nghị 2024):"
echo "1) qwen2.5:7b (Khuyên dùng - Tốt nhất cho hướng dẫn đa ngôn ngữ)"
echo "2) llama3.1 (Chất lượng cao, instruction-following xuất sắc)"
echo "3) mistral:instruct (Ổn định, function calling tốt)"
echo "4) phi3 (Nhỏ gọn, hiệu quả)"
echo "5) gemma2:9b (Google, chất lượng cao)"
echo "6) Tất cả models tốt nhất"

read -p "Nhập lựa chọn (1-6): " choice

case $choice in
    1)
        ollama pull qwen2.5:7b
        echo "✅ Qwen2.5 7B - Tốt nhất cho hướng dẫn tiếng Việt!"
        ;;
    2)
        ollama pull llama3.1
        echo "✅ Llama 3.1 - Instruction-following xuất sắc!"
        ;;
    3)
        ollama pull mistral:instruct
        echo "✅ Mistral Instruct - Đáng tin cậy!"
        ;;
    4)
        ollama pull phi3
        echo "✅ Phi-3 - Nhỏ gọn, hiệu quả!"
        ;;
    5)
        ollama pull gemma2:9b
        echo "✅ Gemma2 9B - Chất lượng Google!"
        ;;
    6)
        echo "📦 Đang tải tất cả models tốt nhất..."
        ollama pull qwen2.5:7b
        ollama pull llama3.1
        ollama pull mistral:instruct
        ollama pull phi3
        ollama pull gemma2:9b
        echo "✅ Đã tải tất cả models hàng đầu 2024!"
        ;;
    *)
        echo "Mặc định: Tải Qwen2.5:7b (khuyên dùng)"
        ollama pull qwen2.5:7b
        ;;
esac

# Verify installation
echo "🔍 Kiểm tra cài đặt..."
ollama list

echo ""
echo "✅ Cài đặt hoàn tất!"
echo ""
echo "📋 Bước tiếp theo:"
echo "1. Cài đặt Python dependencies: pip install -r requirements.txt"
echo "2. Chạy ứng dụng: python run_app.py"
echo "3. Hoặc trực tiếp: streamlit run app.py"
echo ""
echo "🌐 Truy cập: http://localhost:8501" 