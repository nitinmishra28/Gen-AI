import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration from environment variables."""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DEFAULT_OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    OPENAI_MODELS = {
        'gpt-3.5-turbo': {
            'max_tokens': 4096, 'temperature': 0.3, 'top_p': 0.9
        },
        # 'gpt-4': {
        #     'max_tokens': 8192, 'temperature': 0.3, 'top_p': 0.9
        # },
        'gpt-4.1': {
            'max_tokens': 128000, 'temperature': 0.3, 'top_p': 0.9
        }
    }

    # Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    GEMINI_MODELS = {
        'gemini-1.5-flash': {
            'temperature': 0.7,
            'top_p': 1.0
        },
        'gemini-1.5-pro': {
            'temperature': 0.7,
            'top_p': 1.0
        }
    }

    # Ollama Configuration
    OLLAMA_API_BASE = os.getenv('OLLAMA_API_BASE', "http://localhost:11434")
    OLLAMA_MODELS = {
        'gemma2:9b-instruct-q4_K_M': {
            'max_tokens': 4096, 'temperature': 0.3, 'top_p': 0.9
        },
        'gemma3:1b': {
            'max_tokens': 2048, 'temperature': 0.3, 'top_p': 0.9
        },
        'llama3': {
            'max_tokens': 4096, 'temperature': 0.3, 'top_p': 0.9
        }
    }

    # General Configuration
    USE_MOCK = os.getenv('USE_MOCK', 'False').lower() == 'true'
    CACHE_DIR = os.getenv('CACHE_DIR', 'cache')
    MAX_INPUT_CHARS = int(os.getenv('MAX_INPUT_CHARS', os.getenv('MAX_TEXT_LENGTH', '50000')))
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '10'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Cache settings
    CACHE_TTL_HOURS = int(os.getenv('CACHE_TTL_HOURS', '24'))
    
    # Debug settings
    DEBUG = os.getenv('DEBUG_MODE', os.getenv('FLASK_DEBUG', 'False')).lower() == 'true'

    @property
    def all_available_models(self):
        """Returns a flat list of all available models."""
        all_models = []
        all_models.extend(self.OPENAI_MODELS.keys())
        all_models.extend(self.GEMINI_MODELS.keys())
        all_models.extend(self.OLLAMA_MODELS.keys())
        return all_models

# Create a config instance for the app to use
config = Config()
