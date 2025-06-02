# API Configuration
API_TITLE = "ZiZi AI API"
API_DESCRIPTION = "API Trợ Lý AI Thông Minh với Qwen2.5 và Streaming SSE"
API_VERSION = "1.0.0"

# Server Configuration
HOST = "0.0.0.0"
PORT = 8000
RELOAD = True

# Model Configuration
DEFAULT_MODEL = "zizi-ai"
MODEL_OWNER = "zizi-team"

# CORS Configuration
CORS_ORIGINS = ["*"]
CORS_CREDENTIALS = True
CORS_METHODS = ["*"]
CORS_HEADERS = ["*"]

# Streaming Configuration
DEFAULT_CHUNK_SIZE = 10
STREAM_DELAY = 0.05  # seconds

# Response Configuration
DEFAULT_MAX_TOKENS = 500
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9

# Knowledge Base Configuration
SEARCH_RESULTS_LIMIT = 3
CONTEXT_MAX_LENGTH = 300

# System Configuration
UPTIME = "100%"
RESPONSE_TIME = "< 1s"
ACCURACY = "95%" 