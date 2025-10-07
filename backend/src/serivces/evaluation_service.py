# import torch
# from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
# from transformers import AutoModelForCausalLM, AutoTokenizer

# class EvaluationService:
#     def __init__(self):
#         """Initializes the evaluation service."""
#         self.perplexity_tokenizer = AutoTokenizer.from_pretrained("gpt2")
#         self.perplexity_model = AutoModelForCausalLM.from_pretrained("gpt2")
#         if torch.cuda.is_available():
#             self.perplexity_model = self.perplexity_model.cuda()
#         self.perplexity_model.eval()
#         self.max_length = 1024  # Maximum sequence length for gpt2

#     def calculate_bleu(self, reference_text: str, generated_text: str) -> float:
#         """
#         Calculates the BLEU score between a generated text and a reference.
#         """
#         reference_tokens = [reference_text.split()]
#         generated_tokens = generated_text.split()
#         smoother = SmoothingFunction().method4
#         score = sentence_bleu(reference_tokens, generated_tokens, smoothing_function=smoother)
#         return score

#     def calculate_perplexity(self, text: str) -> float:
#         """
#         Calculates the perplexity of a given text to measure fluency.
#         Lower is better.
#         """
#         # Encode the text and truncate to max_length
#         inputs = self.perplexity_tokenizer(
#             text,
#             return_tensors="pt",
#             max_length=self.max_length,
#             truncation=True
#         )
#         input_ids = inputs.input_ids
#         if torch.cuda.is_available():
#             input_ids = input_ids.cuda()

#         with torch.no_grad():
#             outputs = self.perplexity_model(input_ids, labels=input_ids)
#             loss = outputs.loss
        
#         return torch.exp(loss).item()









import asyncio
import logging
from typing import Optional, Union
from functools import lru_cache

import torch
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from transformers import AutoModelForCausalLM, AutoTokenizer

logger = logging.getLogger(__name__)


class EvaluationService:
    """Service for evaluating generated text using BLEU scores and perplexity metrics."""
    
    def __init__(self, model_name: str = "gpt2", max_length: int = 1024):
        """
        Initializes the evaluation service.
        
        Args:
            model_name: HuggingFace model name for perplexity calculation
            max_length: Maximum sequence length for the model
        """
        self.model_name = model_name
        self.max_length = max_length
        self._tokenizer: Optional[AutoTokenizer] = None
        self._model: Optional[AutoModelForCausalLM] = None
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize models lazily
        self._initialize_models()
        
    def _initialize_models(self) -> None:
        """Initialize tokenizer and model for perplexity calculation."""
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self._model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
            # Add padding token if not present
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token
            
            # Move model to appropriate device
            self._model = self._model.to(self._device)
            self._model.eval()
            
            logger.info(f"Evaluation model '{self.model_name}' loaded successfully on {self._device}")
            
        except Exception as e:
            logger.error(f"Failed to initialize evaluation models: {e}")
            raise RuntimeError(f"Could not load evaluation models: {e}")

    @property
    def tokenizer(self) -> AutoTokenizer:
        """Lazy access to tokenizer."""
        if self._tokenizer is None:
            self._initialize_models()
        return self._tokenizer

    @property 
    def model(self) -> AutoModelForCausalLM:
        """Lazy access to model."""
        if self._model is None:
            self._initialize_models()
        return self._model

    async def calculate_bleu(self, reference_text: str, generated_text: str) -> float:
        """
        Calculates the BLEU score between a generated text and a reference.
        
        Args:
            reference_text: Ground truth text to compare against
            generated_text: AI-generated text to evaluate
            
        Returns:
            BLEU score between 0.0 and 1.0 (higher is better)
        """
        if not reference_text.strip() or not generated_text.strip():
            logger.warning("Empty text provided for BLEU calculation")
            return 0.0
            
        try:
            # Run tokenization in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            reference_tokens, generated_tokens = await loop.run_in_executor(
                None,
                self._tokenize_texts,
                reference_text,
                generated_text
            )
            
            smoother = SmoothingFunction().method4
            score = sentence_bleu(
                [reference_tokens], 
                generated_tokens, 
                smoothing_function=smoother
            )
            
            return float(score)
            
        except Exception as e:
            logger.error(f"Error calculating BLEU score: {e}")
            return 0.0

    def _tokenize_texts(self, reference_text: str, generated_text: str) -> tuple:
        """Helper method to tokenize texts (runs in thread pool)."""
        reference_tokens = reference_text.split()
        generated_tokens = generated_text.split()
        return reference_tokens, generated_tokens

    async def calculate_perplexity(self, text: str) -> float:
        """
        Calculates the perplexity of a given text to measure fluency.
        Lower perplexity indicates better fluency.
        
        Args:
            text: Text to evaluate for fluency
            
        Returns:
            Perplexity score (lower is better)
        """
        if not text.strip():
            logger.warning("Empty text provided for perplexity calculation")
            return float('inf')
            
        try:
            # Run model inference in thread pool to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            perplexity = await loop.run_in_executor(
                None,
                self._compute_perplexity,
                text
            )
            
            return perplexity
            
        except Exception as e:
            logger.error(f"Error calculating perplexity: {e}")
            return float('inf')

    def _compute_perplexity(self, text: str) -> float:
        """
        Helper method to compute perplexity (runs in thread pool).
        
        Args:
            text: Input text to analyze
            
        Returns:
            Perplexity score
        """
        # Encode the text and truncate to max_length
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            max_length=self.max_length,
            truncation=True,
            padding=True
        )
        
        input_ids = inputs.input_ids.to(self._device)
        attention_mask = inputs.attention_mask.to(self._device)
        
        with torch.no_grad():
            outputs = self.model(
                input_ids=input_ids, 
                attention_mask=attention_mask,
                labels=input_ids
            )
            loss = outputs.loss
        
        return torch.exp(loss).item()

    async def evaluate_text_quality(self, 
                                  generated_text: str, 
                                  reference_text: Optional[str] = None) -> dict:
        """
        Comprehensive text quality evaluation combining multiple metrics.
        
        Args:
            generated_text: Text to evaluate
            reference_text: Optional reference text for BLEU calculation
            
        Returns:
            Dictionary containing evaluation metrics
        """
        results = {
            "perplexity": await self.calculate_perplexity(generated_text),
            "text_length": len(generated_text.split()),
            "character_count": len(generated_text)
        }
        
        if reference_text:
            results["bleu_score"] = await self.calculate_bleu(reference_text, generated_text)
            
        return results

    async def batch_evaluate(self, 
                           texts: list[str], 
                           references: Optional[list[str]] = None) -> list[dict]:
        """
        Evaluate multiple texts concurrently for better performance.
        
        Args:
            texts: List of texts to evaluate
            references: Optional list of reference texts for BLEU scores
            
        Returns:
            List of evaluation results for each text
        """
        if references and len(texts) != len(references):
            raise ValueError("Number of texts and references must match")
            
        tasks = []
        for i, text in enumerate(texts):
            reference = references[i] if references else None
            task = self.evaluate_text_quality(text, reference)
            tasks.append(task)
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Handle any exceptions that occurred during evaluation
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error evaluating text {i}: {result}")
                processed_results.append({
                    "error": str(result),
                    "perplexity": float('inf'),
                    "text_length": len(texts[i].split()),
                    "character_count": len(texts[i])
                })
            else:
                processed_results.append(result)
                
        return processed_results

    def cleanup(self) -> None:
        """Clean up GPU memory if using CUDA."""
        if torch.cuda.is_available() and self._model is not None:
            del self._model
            del self._tokenizer
            torch.cuda.empty_cache()
            logger.info("Cleaned up GPU memory")


# Dependency function for FastAPI
@lru_cache()
def get_evaluation_service() -> EvaluationService:
    """
    Dependency function to get a singleton EvaluationService instance.
    Uses LRU cache to ensure only one instance is created.
    """
    return EvaluationService()
