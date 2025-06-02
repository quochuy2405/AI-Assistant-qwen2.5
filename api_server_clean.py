from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from datetime import datetime

# Import từ các module đã tách
from api.models import (
    ChatCompletionRequest, 
    ChatCompletionResponse, 
    ChatCompletionChoice,
    ChatMessage,
    HealthResponse,
    StatsResponse,
    ModelsResponse,
    ModelInfo
)
from api.responses import get_smart_response, SMART_RESPONSES
from api.utils import (
    stream_response, 
    generate_chat_id, 
    get_current_timestamp,
    extract_user_message
)
from api.config import *

# Import logic từ app hiện tại
from knowledge_base import KnowledgeBase

# Khởi tạo FastAPI app
app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

@app.get("/")
async def root():
    """Root endpoint với thông tin API"""
    return {
        "message": "AI KOC Support API Server", 
        "version": API_VERSION,
        "docs": "/docs",
        "health": "/health",
        "models": "/models",
        "chat": "/chat/completions"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        uptime=UPTIME
    )

@app.get("/models", response_model=ModelsResponse)
async def list_models():
    """List available models - OpenAI compatible"""
    return ModelsResponse(
        object="list",
        data=[
            ModelInfo(
                id=DEFAULT_MODEL,
                object="model",
                created=get_current_timestamp(),
                owned_by=MODEL_OWNER,
                permission=[],
                root=DEFAULT_MODEL,
                parent=None
            )
        ]
    )

@app.post("/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """Main chat completion endpoint với SSE streaming"""
    
    try:
        # Lấy message cuối cùng từ user
        user_message = extract_user_message(request.messages)
        
        if not user_message:
            raise HTTPException(status_code=400, detail="No user message found")
        
        # Generate response
        ai_response = get_smart_response(user_message)
        
        if request.stream:
            # Streaming response
            return StreamingResponse(
                stream_response(ai_response, DEFAULT_CHUNK_SIZE),
                media_type="text/plain",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "text/plain; charset=utf-8"
                }
            )
        else:
            # Non-streaming response
            response = ChatCompletionResponse(
                id=generate_chat_id(),
                object="chat.completion",
                created=get_current_timestamp(),
                model=request.model,
                choices=[
                    ChatCompletionChoice(
                        index=0,
                        message=ChatMessage(role="assistant", content=ai_response),
                        finish_reason="stop"
                    )
                ]
            )
            return response
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/upload")
async def upload_documents():
    """Endpoint để upload tài liệu PDF (có thể implement sau)"""
    return {"message": "Document upload endpoint - Coming soon"}

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get system statistics"""
    try:
        knowledge_base = KnowledgeBase()
        stats = knowledge_base.get_statistics()
        
        return StatsResponse(
            total_documents=stats.get('total_documents', 0),
            total_chunks=stats.get('total_chunks', 0),
            supported_topics=len(SMART_RESPONSES),
            uptime=UPTIME,
            response_time=RESPONSE_TIME,
            accuracy=ACCURACY
        )
    except:
        return StatsResponse(
            total_documents=0,
            total_chunks=0,
            supported_topics=len(SMART_RESPONSES),
            uptime=UPTIME,
            response_time=RESPONSE_TIME,
            accuracy=ACCURACY
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, reload=RELOAD) 