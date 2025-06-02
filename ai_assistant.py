import ollama
from typing import List, Dict, Optional
import json
import time
from datetime import datetime

class AIAssistant:
    """AI Assistant sử dụng LLAMA để trả lời câu hỏi KOC"""
    
    def __init__(self, model_name: str = "llama2:latest"):
        self.model_name = model_name
        self.conversation_history = []
        
        # Template prompt cho việc trả lời câu hỏi
        self.system_prompt = """AI hỗ trợ người Việt. 

QUAN TRỌNG: Chỉ trả lời bằng tiếng Việt. Cấm tiếng Anh.

🎯 NHIỆM VỤ: Trả lời ngắn gọn, thân thiện về hướng dẫn app."""
    
    def generate_response(self, question: str, context: str = "", conversation_history: List[Dict] = None) -> str:
        """
        Tạo phản hồi cho câu hỏi của KOC
        
        Args:
            question: Câu hỏi của KOC
            context: Ngữ cảnh từ tài liệu liên quan
            conversation_history: Lịch sử hội thoại
            
        Returns:
            Phản hồi của AI
        """
        try:
            # Xây dựng prompt
            prompt = self._build_prompt(question, context, conversation_history)
            
            # Gọi LLAMA
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt + "\n\nQUAN TRỌNG: Trả lời hoàn toàn bằng TIẾNG VIỆT. Không được dùng tiếng Anh."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": "Xin chào! 😊 "}  # Force start in Vietnamese
                ],
                options={
                    "temperature": 0.3,      # Giảm từ 0.7 để nhanh hơn
                    "top_p": 0.8,           # Giảm từ 0.9
                    "max_tokens": 300,      # Giảm từ 1024 để nhanh hơn
                    "num_predict": 300,     # Limit prediction
                    "repeat_penalty": 1.1,  # Tránh lặp lại
                    "stop": ["English:", "In English", "[English]"],
                }
            )
            
            # Lấy nội dung phản hồi
            answer = "Xin chào! 😊 " + response['message']['content'].strip()
            
            # Lưu vào lịch sử
            self.conversation_history.append({
                "question": question,
                "answer": answer,
                "context_used": bool(context),
                "timestamp": datetime.now().isoformat()
            })
            
            return answer
            
        except Exception as e:
            return f"Xin lỗi, tôi gặp lỗi khi xử lý câu hỏi của bạn: {str(e)}"
    
    def _build_prompt(self, question: str, context: str, conversation_history: List[Dict] = None) -> str:
        """Xây dựng prompt ngắn gọn cho LLAMA"""
        
        prompt_parts = []
        
        # Thêm context nếu có
        if context:
            prompt_parts.append("TÀI LIỆU:")
            prompt_parts.append(context[:500] + "...")  # Giới hạn context
            prompt_parts.append("")
        
        # Câu hỏi
        prompt_parts.append("CÂU HỎI:")
        prompt_parts.append(question)
        prompt_parts.append("")
        
        # Hướng dẫn ngắn
        prompt_parts.append("Trả lời ngắn gọn bằng tiếng Việt:")
        
        return "\n".join(prompt_parts)
    
    def generate_follow_up_questions(self, question: str, answer: str) -> List[str]:
        """Tạo câu hỏi tiếp theo có thể hữu ích"""
        try:
            prompt = f"""
Dựa trên câu hỏi và câu trả lời sau, hãy đề xuất 3 câu hỏi tiếp theo mà KOC có thể quan tâm:

Câu hỏi gốc: {question}
Câu trả lời: {answer}

Đề xuất 3 câu hỏi tiếp theo (mỗi câu một dòng, bắt đầu bằng dấu -):
"""
            
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.8, "max_tokens": 200}
            )
            
            # Xử lý phản hồi
            content = response['message']['content'].strip()
            questions = []
            
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('-'):
                    questions.append(line[1:].strip())
                elif line and not line.startswith('Đề xuất') and not line.startswith('Câu hỏi'):
                    questions.append(line)
            
            return questions[:3]  # Chỉ lấy tối đa 3 câu
            
        except Exception:
            return []
    
    def summarize_conversation(self, messages: List[Dict]) -> str:
        """Tóm tắt cuộc hội thoại"""
        try:
            # Tạo text từ lịch sử hội thoại
            conversation_text = ""
            for msg in messages:
                role = "KOC" if msg['role'] == 'user' else "AI"
                conversation_text += f"{role}: {msg['content']}\n"
            
            prompt = f"""
Hãy tóm tắt cuộc hội thoại sau giữa KOC và AI Assistant về hướng dẫn app:

{conversation_text}

Tóm tắt (2-3 câu ngắn gọn):
"""
            
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.5, "max_tokens": 150}
            )
            
            return response['message']['content'].strip()
            
        except Exception:
            return "Không thể tóm tắt cuộc hội thoại."
    
    def check_question_relevance(self, question: str) -> Dict[str, any]:
        """Kiểm tra câu hỏi có liên quan đến hướng dẫn app không"""
        try:
            prompt = f"""
Câu hỏi: {question}

Hãy đánh giá câu hỏi này:
1. Có liên quan đến hướng dẫn sử dụng app không? (có/không)
2. Loại câu hỏi (hướng dẫn/troubleshooting/tính năng/khác)
3. Mức độ cụ thể (cao/trung bình/thấp)

Trả lời bằng JSON format:
{{"relevant": true/false, "type": "...", "specificity": "..."}}
"""
            
            response = ollama.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.3, "max_tokens": 100}
            )
            
            content = response['message']['content'].strip()
            
            # Thử parse JSON
            try:
                return json.loads(content)
            except:
                # Fallback
                return {
                    "relevant": True,
                    "type": "general",
                    "specificity": "medium"
                }
                
        except Exception:
            return {
                "relevant": True,
                "type": "unknown",
                "specificity": "unknown"
            }
    
    def get_conversation_stats(self) -> Dict[str, any]:
        """Lấy thống kê cuộc hội thoại"""
        if not self.conversation_history:
            return {
                "total_questions": 0,
                "avg_response_time": 0,
                "context_usage": 0
            }
        
        total_questions = len(self.conversation_history)
        questions_with_context = sum(1 for item in self.conversation_history if item.get('context_used', False))
        
        return {
            "total_questions": total_questions,
            "context_usage_rate": round(questions_with_context / total_questions * 100, 1) if total_questions > 0 else 0,
            "last_question_time": self.conversation_history[-1]['timestamp'] if self.conversation_history else None
        }
    
    def clear_history(self):
        """Xóa lịch sử hội thoại"""
        self.conversation_history = []
    
    def set_model(self, model_name: str):
        """Thay đổi model LLAMA"""
        self.model_name = model_name 