import logging
from typing import Dict, Optional, Tuple
from functools import lru_cache
import asyncio

try:
    from langdetect import detect, DetectorFactory
    from langdetect.lang_detect_exception import LangDetectException
    DetectorFactory.seed = 0
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    logging.warning("langdetect not installed")

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    logging.warning("deep-translator not installed")

logger = logging.getLogger(__name__)


class TranslationService:
    """Service for language detection and translation."""
    
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'Hindi', 
        'fr': 'French',
        'de': 'German',
        'es': 'Spanish',
        'it': 'Italian',
        'pt': 'Portuguese',
        'nl': 'Dutch',
        'ru': 'Russian',
        'zh-cn': 'Chinese (Simplified)',
        'ja': 'Japanese',
        'ko': 'Korean',
        'ar': 'Arabic'
    }
    
    MAX_CHUNK_SIZE = 4500
    
    def __init__(self):
        """Initialize translation service."""
        if not LANGDETECT_AVAILABLE:
            raise ImportError(
                "langdetect package required. Install: pip install langdetect"
            )
        if not TRANSLATOR_AVAILABLE:
            raise ImportError(
                "deep-translator package required. Install: pip install deep-translator"
            )
    
    async def detect_language(self, text: str) -> Tuple[str, float]:
        """Detect language of text."""
        try:
            loop = asyncio.get_event_loop()
            lang_code = await loop.run_in_executor(None, detect, text[:10000])
            return lang_code, 1.0
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}")
            return 'unknown', 0.0
        except Exception as e:
            logger.error(f"Unexpected error in language detection: {e}")
            return 'error', 0.0
    
    def _split_text_into_chunks(self, text: str) -> list:
        """Split text into chunks for translation."""
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 > self.MAX_CHUNK_SIZE:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = para
            else:
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    async def translate_text(
        self, 
        text: str, 
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> Dict:
        """Translate text to target language."""
        try:
            if source_lang == target_lang:
                return {
                    "original_text": text,
                    "translated_text": text,
                    "source_language": source_lang,
                    "target_language": target_lang,
                    "was_translated": False
                }
            
            chunks = self._split_text_into_chunks(text)
            loop = asyncio.get_event_loop()
            translated_chunks = []
            
            for chunk in chunks:
                translator = GoogleTranslator(
                    source=source_lang, 
                    target=target_lang
                )
                translated = await loop.run_in_executor(
                    None,
                    translator.translate,
                    chunk
                )
                translated_chunks.append(translated)
            
            translated_text = "\n\n".join(translated_chunks)
            
            return {
                "original_text": text,
                "translated_text": translated_text,
                "source_language": source_lang,
                "target_language": target_lang,
                "was_translated": True,
                "chunks_processed": len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise ValueError(f"Translation failed: {str(e)}")
    
    async def process_resume_with_translation(
        self, 
        text: str,
        target_lang: str = 'en'
    ) -> Dict:
        """Detect language and translate resume if needed."""
        detected_lang, confidence = await self.detect_language(text)
        
        logger.info(
            f"Detected language: {detected_lang} "
            f"({self.SUPPORTED_LANGUAGES.get(detected_lang, 'Unknown')})"
        )
        
        if detected_lang != target_lang and detected_lang != 'unknown':
            translation_result = await self.translate_text(
                text,
                source_lang=detected_lang,
                target_lang=target_lang
            )
            processed_text = translation_result["translated_text"]
            was_translated = True
        else:
            processed_text = text
            was_translated = False
        
        return {
            "original_text": text,
            "processed_text": processed_text,
            "detected_language": detected_lang,
            "language_name": self.SUPPORTED_LANGUAGES.get(detected_lang, 'Unknown'),
            "confidence": confidence,
            "was_translated": was_translated,
            "target_language": target_lang
        }


@lru_cache()
def get_translation_service() -> TranslationService:
    """Get singleton translation service instance."""
    return TranslationService()
