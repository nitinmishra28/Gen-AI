import os
import re
import json
import hashlib
import time
import logging
from typing import Dict, List, Any

from openai import OpenAI, RateLimitError
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential, wait_random, retry_if_exception_type

# Import from src package
from src.config import config

from src.analyzer.prompts import get_analyze_cv_prompt, get_cover_letter_prompt, get_customize_content_prompt

logger = logging.getLogger(__name__)


class CVAnalyzer:
    """Handles CV analysis, content generation, and caching."""

    def __init__(self):
        """Initializes the analyzer with support for multiple LLM providers."""
        self.clients = {}
        self.use_mock = config.USE_MOCK
        
        # Initialize OpenAI client if key is available
        if config.OPENAI_API_KEY:
            self.clients['gpt-3.5-turbo'] = OpenAI(api_key=config.OPENAI_API_KEY)
            self.clients['gpt-4'] = OpenAI(api_key=config.OPENAI_API_KEY)
            
        # Initialize other model clients here if needed
        # Example: Initialize Gemini client
        if config.GEMINI_API_KEY:
            self.clients['gemini-pro'] = None  # Replace with actual Gemini client initialization
            
        if not self.clients and not self.use_mock:
            raise ValueError("No API keys configured and mock mode disabled.")
        
        # Ensure cache directory exists
        os.makedirs(config.CACHE_DIR, exist_ok=True)
        
        logger.info(f"CVAnalyzer initialized with available models: {', '.join(self.clients.keys())}, Mock: {self.use_mock}")

    def _mock_analysis(self) -> Dict[str, Any]:
        """Returns a predefined mock analysis for testing purposes."""
        return {
            "overall_score": 85,
            "requirements_score": 80,
            "wishes_score": 90,
            "requirements": [
                {"id": "req_1", "type": "require", "title": "Python Development", "description": "Experience with Python programming", "match": True, "percentage": 85, "explanation": "Strong Python experience evident in CV"}
            ],
            "wishes": [
                {"id": "wish_1", "type": "wish", "title": "Machine Learning", "description": "Knowledge of ML frameworks", "match": True, "percentage": 75, "explanation": "Some ML experience mentioned"}
            ]
        }

    def _sanitize_and_truncate_text(self, text: str) -> str:
        """Sanitizes and truncates input text to prevent errors and reduce token usage."""
        text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
        text = re.sub(r'[^\w\s\-.,!?@#&()"\':;/\\]', '', text)  # Keep safe characters
        
        if len(text) > config.MAX_INPUT_CHARS:
            logger.warning(f"Input text truncated to {config.MAX_INPUT_CHARS} characters.")
            return text[:config.MAX_INPUT_CHARS]
        return text

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=30) + wait_random(0, 3),
        retry=retry_if_exception_type((RateLimitError, json.JSONDecodeError, RequestException)),
        reraise=True
    )
    def _call_llm(self, prompt: str, system_content: str, model_name: str = None, temperature: float = None, use_json_mode: bool = False) -> str:
        """Makes a robust call to the selected LLM API with retry logic."""
        if self.use_mock:
            if use_json_mode:
                return json.dumps(self._mock_analysis())
            return "This is a mock response for testing purposes."
            
        # Use default OpenAI model if none specified
        if model_name is None:
            model_name = config.DEFAULT_OPENAI_MODEL
            
        # Get the client for the specified model
        if model_name not in self.clients:
            raise ValueError(f"Model {model_name} not available. Available models: {', '.join(self.clients.keys())}")
            
        client = self.clients[model_name]
        model_config = {}
        
        # Get model-specific configuration
        if model_name in config.OPENAI_MODELS:
            model_config = config.OPENAI_MODELS[model_name]
        elif model_name in config.GEMINI_MODELS:
            model_config = config.GEMINI_MODELS[model_name]
            
        # Use provided temperature or fall back to model config
        if temperature is None:
            temperature = model_config.get('temperature', 0.7)
            
        logger.debug(f"Calling LLM API with model: {model_name}")
        params = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
        }
        if use_json_mode:
            params["response_format"] = {"type": "json_object"}
        
        # Handle different model types
        if model_name in config.OPENAI_MODELS:
            response = self.clients[model_name].chat.completions.create(**params)
            return response.choices[0].message.content.strip()
        elif model_name in config.GEMINI_MODELS:
            # Implement Gemini API call here
            raise NotImplementedError(f"Gemini model {model_name} support not yet implemented")
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    def _validate_analysis_result(self, result: Dict) -> Dict:
        """Validates the structure and content of the AI's analysis response."""
        required_fields = ['overall_score', 'requirements_score', 'wishes_score', 'requirements', 'wishes']
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field: {field} in analysis result.")
        
        for key in ['overall_score', 'requirements_score', 'wishes_score']:
            val = result[key]
            if not isinstance(val, (int, float)) or not 0 <= val <= 100:
                raise ValueError(f"Invalid score value for {key}: {val}")
        
        return result

    def _get_cache_key(self, cv_text: str, assignment_text: str) -> str:
        """Generates a unique cache key from the CV and assignment text."""
        return hashlib.sha256((cv_text + assignment_text).encode()).hexdigest()

    def _is_cache_valid(self, cache_file: str, ttl_hours: int = 24) -> bool:
        """Checks if a cache file is still valid based on its age."""
        if not os.path.exists(cache_file):
            return False
        file_age = time.time() - os.path.getmtime(cache_file)
        return file_age < (ttl_hours * 3600)

    def analyze_cv_assignment_match(self, cv_text: str, assignment_text: str, model_name: str = None) -> Dict[str, Any]:
        """Analyzes a CV against job requirements, with caching to optimize costs."""
        if self.use_mock:
            return self._mock_analysis()
            
        if not model_name:
            model_name = config.DEFAULT_OPENAI_MODEL
        
        cv_text = self._sanitize_and_truncate_text(cv_text)
        assignment_text = self._sanitize_and_truncate_text(assignment_text)
        
        cache_key = self._get_cache_key(cv_text, assignment_text)
        cache_file = os.path.join(config.CACHE_DIR, f"{cache_key}.json")
        
        if self._is_cache_valid(cache_file):
            logger.info(f"Returning cached result for key: {cache_key}")
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        from src.analyzer.prompts import get_analyze_cv_prompt
        prompts = get_analyze_cv_prompt(cv_text, assignment_text, model_name)
        
        content = self._call_llm(
            prompt=prompts['user'], 
            system_content=prompts['system'], 
            model_name=model_name,
            use_json_mode=True
        )
        
        try:
            result = json.loads(content)
            result = self._validate_analysis_result(result)
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse or validate AI response: {e}", exc_info=True)
            raise ValueError("Failed to get a valid analysis from the AI model.")
            
        with open(cache_file, 'w') as f:
            json.dump(result, f)
        logger.info(f"Cached new analysis result with key: {cache_key}")
        
        return result

    def generate_motivations(self, cv_text: str, requirements: List[Dict], consultant_name: str, model_name: str = None) -> Dict[str, str]:
        """Generates personalized motivations for each requirement."""
        if self.use_mock:
            return {req['id']: "Mock motivation for testing." for req in requirements}
        
        motivations = {}
        cv_text = self._sanitize_and_truncate_text(cv_text)
        model_name = model_name or config.DEFAULT_OPENAI_MODEL
        system_content = "You are an expert at writing compelling, specific motivations for job requirements."
        
        for req in requirements:
            prompt = (
                f"Generate a personalized, 2-3 sentence motivation for the requirement below, based on the consultant's CV.\n\n"
                f"CONSULTANT: {consultant_name}\n"
                f"REQUIREMENT: {req['title']} - {req['description']}\n\n"
                f"CV CONTENT:\n"
                f"{cv_text}\n\n"
                "Instructions:\n"
                "1. Analyze the requirement carefully.\n"
                "2. Reference specific skills and experiences from the CV that match the requirement.\n"
                "3. Keep the response concise but compelling, focusing on the strongest matches.\n"
                "4. Write in first person from the consultant's perspective.\n"
                "5. Keep the tone professional and confident."
            )

            try:
                content = self._call_llm(prompt=prompt, system_content=system_content, model_name=model_name)
                motivations[req['id']] = content
            except Exception as e:
                logger.error(f"Error generating motivation for requirement {req['id']}: {e}")
                motivations[req['id']] = f"Error generating motivation: {e}"
        
        return motivations

    def generate_cover_letter(self, cv_text: str, assignment_info: Dict, consultant_name: str, analysis_result: Dict, model_name: str = None) -> str:
        """Generates a professional cover letter."""
        if self.use_mock:
            return "Mock cover letter for testing."
        
        if not model_name:
            model_name = config.DEFAULT_OPENAI_MODEL
            
        cv_text = self._sanitize_and_truncate_text(cv_text)
        assignment_description = self._sanitize_and_truncate_text(assignment_info.get('description', ''))
        
        from src.analyzer.prompts import get_cover_letter_prompt
        prompts = get_cover_letter_prompt(cv_text, assignment_description, model_name)
        
        return self._call_llm(prompt=prompts['user'], system_content=prompts['system'], model_name=model_name)

    def generate_introduction_email(self, consultant_info: Dict, assignment_info: Dict, analysis_result: Dict, model_name: str = None) -> str:
        """Generates a professional introduction email to a client."""
        if self.use_mock:
            return "Mock email for testing."
        
        if not model_name:
            model_name = config.DEFAULT_OPENAI_MODEL
        
        prompt = (
            f"Write a professional introduction email from a staffing agency to a client.\n\n"
            f"CONSULTANT: {consultant_info.get('name', 'the consultant')}\n"
            f"CONTACT PERSON AT CLIENT: {consultant_info.get('contactPerson', 'Hiring Manager')}\n"
            f"MATCH SCORE: {analysis_result.get('overall_score', 0)}%\n"
            f"KEY REQUIREMENTS MET: {', '.join([r['title'] for r in analysis_result.get('requirements', []) if r.get('match')])}\n\n"
            "Instructions:\n"
            "1. Write a formal yet engaging email introducing the consultant.\n"
            "2. Highlight the strong match between requirements and consultant's experience.\n"
            "3. Keep it concise but informative, focusing on the most relevant qualifications.\n"
            "4. Include next steps or a call to action.\n"
            "5. Use a professional business email format."
        )

        system_content = "You are an expert business communicator for a recruitment agency. Your tone is professional, efficient, and client-focused."
        
        return self._call_llm(prompt=prompt, system_content=system_content, model_name=model_name)

    def customize_content(self, content_type: str, original_content: str, user_prompt: str, context: Dict = None, model_name: str = None) -> str:
        """Customizes generated content based on user feedback."""
        if self.use_mock:
            return f"Mock customized content for {content_type}."
        
        if not model_name:
            model_name = config.DEFAULT_OPENAI_MODEL
            
        prompts = get_customize_content_prompt(content_type, original_content, user_prompt, context, model_name)
        
        return self._call_llm(prompt=prompts['user'], system_content=prompts['system'], model_name=model_name)