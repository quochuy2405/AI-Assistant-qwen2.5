import os
from typing import Optional
from pathlib import Path

class Config:
    """Cấu hình cho ứng dụng AI Hỗ Trợ KOC"""
    
    # Ollama Configuration
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    DEFAULT_MODEL: str = os.getenv("OLLAMA_MODEL", "llama2")
    
    # PDF Processing
    PDF_CHUNK_SIZE: int = int(os.getenv("PDF_CHUNK_SIZE", "1000"))
    PDF_CHUNK_OVERLAP: int = int(os.getenv("PDF_CHUNK_OVERLAP", "200"))
    MAX_PDF_SIZE_MB: int = int(os.getenv("MAX_PDF_SIZE_MB", "100"))
    
    # Vector Database
    VECTOR_DB_PATH: str = os.getenv("VECTOR_DB_PATH", "./chroma_db")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    
    # AI Assistant
    AI_TEMPERATURE: float = float(os.getenv("AI_TEMPERATURE", "0.7"))
    AI_MAX_TOKENS: int = int(os.getenv("AI_MAX_TOKENS", "1024"))
    AI_TOP_P: float = float(os.getenv("AI_TOP_P", "0.9"))
    
    # Search Settings
    SEARCH_RESULTS_COUNT: int = int(os.getenv("SEARCH_RESULTS_COUNT", "5"))
    SEARCH_SIMILARITY_THRESHOLD: float = float(os.getenv("SEARCH_SIMILARITY_THRESHOLD", "0.5"))
    
    # Streamlit Configuration
    STREAMLIT_SERVER_PORT: int = int(os.getenv("STREAMLIT_SERVER_PORT", "8501"))
    STREAMLIT_SERVER_ADDRESS: str = os.getenv("STREAMLIT_SERVER_ADDRESS", "localhost")
    STREAMLIT_THEME_BASE: str = os.getenv("STREAMLIT_THEME_BASE", "light")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "app.log")
    
    # Security
    ENABLE_FILE_UPLOAD_LIMITS: bool = os.getenv("ENABLE_FILE_UPLOAD_LIMITS", "true").lower() == "true"
    ALLOWED_FILE_TYPES: list = os.getenv("ALLOWED_FILE_TYPES", "pdf").split(",")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "50"))
    
    # Performance
    ENABLE_CACHING: bool = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
    
    # UI Customization
    APP_TITLE: str = os.getenv("APP_TITLE", "AI Hỗ Trợ KOC - Hướng Dẫn App")
    APP_ICON: str = os.getenv("APP_ICON", "🤖")
    SIDEBAR_EXPANDED: bool = os.getenv("SIDEBAR_EXPANDED", "true").lower() == "true"
    
    @classmethod
    def load_from_env_file(cls, env_file: str = ".env"):
        """Tải cấu hình từ file .env"""
        env_path = Path(env_file)
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
    
    @classmethod
    def validate(cls) -> dict:
        """Kiểm tra cấu hình có hợp lệ không"""
        errors = []
        warnings = []
        
        # Kiểm tra các giá trị bắt buộc
        if cls.PDF_CHUNK_SIZE <= 0:
            errors.append("PDF_CHUNK_SIZE phải lớn hơn 0")
        
        if cls.PDF_CHUNK_OVERLAP < 0:
            errors.append("PDF_CHUNK_OVERLAP không được âm")
        
        if cls.PDF_CHUNK_OVERLAP >= cls.PDF_CHUNK_SIZE:
            warnings.append("PDF_CHUNK_OVERLAP không nên lớn hơn hoặc bằng PDF_CHUNK_SIZE")
        
        if cls.AI_TEMPERATURE < 0 or cls.AI_TEMPERATURE > 2:
            warnings.append("AI_TEMPERATURE nên trong khoảng 0-2")
        
        if cls.AI_TOP_P < 0 or cls.AI_TOP_P > 1:
            errors.append("AI_TOP_P phải trong khoảng 0-1")
        
        if cls.SEARCH_SIMILARITY_THRESHOLD < 0 or cls.SEARCH_SIMILARITY_THRESHOLD > 1:
            errors.append("SEARCH_SIMILARITY_THRESHOLD phải trong khoảng 0-1")
        
        # Kiểm tra đường dẫn
        try:
            Path(cls.VECTOR_DB_PATH).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            errors.append(f"Không thể tạo thư mục VECTOR_DB_PATH: {e}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    @classmethod
    def to_dict(cls) -> dict:
        """Chuyển cấu hình thành dictionary"""
        return {
            key: getattr(cls, key)
            for key in dir(cls)
            if key.isupper() and not key.startswith('_')
        }
    
    @classmethod
    def print_config(cls):
        """In ra cấu hình hiện tại"""
        print("🔧 Cấu Hình Ứng Dụng")
        print("=" * 50)
        
        config_dict = cls.to_dict()
        for section in [
            ("Ollama", ["OLLAMA_HOST", "DEFAULT_MODEL"]),
            ("PDF Processing", ["PDF_CHUNK_SIZE", "PDF_CHUNK_OVERLAP", "MAX_PDF_SIZE_MB"]),
            ("Vector Database", ["VECTOR_DB_PATH", "EMBEDDING_MODEL"]),
            ("AI Assistant", ["AI_TEMPERATURE", "AI_MAX_TOKENS", "AI_TOP_P"]),
            ("Search", ["SEARCH_RESULTS_COUNT", "SEARCH_SIMILARITY_THRESHOLD"]),
            ("UI", ["APP_TITLE", "APP_ICON", "SIDEBAR_EXPANDED"])
        ]:
            section_name, keys = section
            print(f"\n📋 {section_name}:")
            for key in keys:
                if key in config_dict:
                    print(f"  {key}: {config_dict[key]}")

# Tải cấu hình từ .env nếu có
Config.load_from_env_file() 