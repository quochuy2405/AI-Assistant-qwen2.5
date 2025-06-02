#!/bin/bash

echo "🚀 AI KOC Support API - cURL Examples"
echo "=================================="

# Health Check
echo "📊 1. Health Check:"
curl -X GET "http://localhost:8000/health" \
  -H "Content-Type: application/json" | jq

echo -e "\n📋 2. List Models:"
curl -X GET "http://localhost:8000/models" \
  -H "Content-Type: application/json" | jq

echo -e "\n📈 3. Get Stats:"
curl -X GET "http://localhost:8000/stats" \
  -H "Content-Type: application/json" | jq

echo -e "\n💬 4. Non-Streaming Chat:"
curl -X POST "http://localhost:8000/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "koc-assistant",
    "messages": [
      {"role": "user", "content": "Hướng dẫn đăng ký tài khoản"}
    ],
    "stream": false
  }' | jq

echo -e "\n📡 5. Streaming Chat:"
curl -X POST "http://localhost:8000/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "koc-assistant", 
    "messages": [
      {"role": "user", "content": "Làm sao để thanh toán bằng thẻ?"}
    ],
    "stream": true
  }'

echo -e "\n✅ All examples completed!" 