import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration from environment variables."""
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    DEFAULT_OPENAI_MODEL = 'gpt-3.5-turbo'
    OPENAI_MODELS = {
        'gpt-3.5-turbo': {
            'max_tokens': 4096,
            'temperature': 0.7
        },
        'gpt-4': {
            'max_tokens': 8192,
            'temperature': 0.7
        }
    }
    
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODELS = {
        'gemini-pro': {
            'max_tokens': 4096,
            'temperature': 0.7
        }
    }
    
    # General Configuration
    USE_MOCK = os.getenv('USE_MOCK', 'False').lower() == 'true'
    CACHE_DIR = os.getenv('CACHE_DIR', 'cache')
    MAX_INPUT_CHARS = int(os.getenv('MAX_INPUT_CHARS', '50000'))
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', '10'))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Available Models Configuration
    AVAILABLE_MODELS = {
        'openai': list(OPENAI_MODELS.keys()),
        'gemini': list(GEMINI_MODELS.keys())
    }
    
    @property
    def all_available_models(self):
        """Returns a flat list of all available models."""
        return sum(self.AVAILABLE_MODELS.values(), [])

# Create a config instance for the app to use
config = Config()
