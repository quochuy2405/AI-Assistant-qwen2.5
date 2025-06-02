import json
import time
import uuid
from typing import Generator

def create_sse_chunk(content: str, is_final: bool = False) -> str:
    """Tạo SSE chunk theo format OpenAI"""
    chunk_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"
    
    if is_final:
        chunk = {
            "id": chunk_id,
            "object": "chat.completion.chunk",
            "created": int(time.time()),
            "model": "koc-assistant",
            "choices": [{
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }]
        }
    else:
        chunk = {
            "id": chunk_id,
            "object": "chat.completion.chunk", 
            "created": int(time.time()),
            "model": "koc-assistant",
            "choices": [{
                "index": 0,
                "delta": {"content": content},
                "finish_reason": None
            }]
        }
    
    return f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"

def stream_response(text: str, chunk_size: int = 10) -> Generator[str, None, None]:
    """Stream response theo chunks như OpenAI"""
    
    # Start chunk
    yield create_sse_chunk("")
    
    # Stream content by chunks
    words = text.split()
    current_chunk = ""
    
    for i, word in enumerate(words):
        current_chunk += word + " "
        
        # Send chunk when reaching chunk_size words or at end
        if (i + 1) % chunk_size == 0 or i == len(words) - 1:
            yield create_sse_chunk(current_chunk)
            current_chunk = ""
            time.sleep(0.05)  # Simulate realistic streaming delay
    
    # Final chunk
    yield create_sse_chunk("", is_final=True)
    yield "data: [DONE]\n\n"

def generate_chat_id() -> str:
    """Generate unique chat completion ID"""
    return f"chatcmpl-{uuid.uuid4().hex[:8]}"

def get_current_timestamp() -> int:
    """Get current Unix timestamp"""
    return int(time.time())

def extract_user_message(messages: list) -> str:
    """Extract the last user message from messages list"""
    for msg in reversed(messages):
        if msg.role == "user":
            return msg.content
    return None 