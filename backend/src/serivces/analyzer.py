
# # Working code ----------------------------------

# import os
# import re
# import json
# import hashlib
# import time
# import logging
# from typing import Dict, List, Any


# from openai import OpenAI, RateLimitError
# from ollama import Client as OllamaClient, ResponseError as OllamaResponseError
# import google.generativeai as genai
# from requests.exceptions import RequestException
# from tenacity import retry, stop_after_attempt, wait_exponential, wait_random, retry_if_exception_type

# # Import from src package
# from src.config import config
# from src.analyzer.prompts import get_analyze_cv_prompt, get_cover_letter_prompt, get_customize_content_prompt, get_motivation_prompt

# try:
#     from ollama import Client as OllamaClient, ResponseError as OllamaResponseError
# except ImportError as e:
#     logging.error(f"Failed to import ollama: {e}")
#     OllamaClient = None
#     OllamaResponseError = None

# logger = logging.getLogger(__name__)

# class CVAnalyzer:
#     def __init__(self):
#         """Initializes clients for all configured LLM providers."""
#         self.openai_client = None
#         self.ollama_client = None
#         self.gemini_client = None
#         self.use_mock = config.USE_MOCK

#         # Initialize OpenAI client if the API key is available
#         if config.OPENAI_API_KEY:
#             self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
#             logger.info("OpenAI client initialized.")
        
#         if config.GEMINI_API_KEY:
#             try:
#                 genai.configure(api_key=config.GEMINI_API_KEY)
#                 self.gemini_client = True # Flag success
#                 logger.info("Gemini client initialized.")
#             except Exception as e:
#                 logger.warning(f"Failed to initialize Gemini client: {e}")
#                 self.gemini_client = False

#         # Initialize Ollama client with retry logic
#         if OllamaClient is not None:
#             @retry(
#                 stop=stop_after_attempt(5),
#                 wait=wait_exponential(multiplier=1, min=2, max=10),
#                 retry=retry_if_exception_type((RequestException, ConnectionError)),
#                 reraise=True
#             )
#             def initialize_ollama_client():
#                 logger.debug(f"Attempting to initialize Ollama client with API base: {config.OLLAMA_API_BASE}")
#                 client = OllamaClient(host=config.OLLAMA_API_BASE)
#                 response = client.list()
#                 logger.debug(f"Ollama server responded with models: {response}")
#                 return client

#             try:
#                 self.ollama_client = initialize_ollama_client()
#                 logger.info("Ollama client initialized and server is responsive.")
#             except Exception as e:
#                 logger.warning(f"Could not connect to Ollama server. Local models will be unavailable. Error: {e}")
#                 self.ollama_client = None
#         else:
#             logger.warning("Ollama package not available. Local models will be unavailable.")

#         if not self.openai_client and not self.ollama_client and not self.use_mock:
#             raise ValueError("No API keys or local Ollama server configured. Application cannot proceed.")

#         os.makedirs(config.CACHE_DIR, exist_ok=True)

#     def _mock_analysis(self) -> Dict[str, Any]:
#         """Returns a predefined mock analysis for testing purposes."""
#         return {
#             "overall_score": 85, "requirements_score": 80, "wishes_score": 90,
#             "requirements": [{"id": "req_1", "type": "require", "title": "Python Development", "match": True, "percentage": 85, "explanation": "Strong Python experience"}],
#             "wishes": [{"id": "wish_1", "type": "wish", "title": "Machine Learning", "match": True, "percentage": 75, "explanation": "Some ML experience"}]
#         }

#     def _sanitize_and_truncate_text(self, text: str) -> str:
#         """Sanitizes and truncates input text."""
#         text = re.sub(r'<[^>]+>', '', text)
#         text = text.encode('ascii', 'ignore').decode('ascii')
#         text = re.sub(r'[^\w\s\-.,!?@#&()"\':;/\\]', ' ', text)
#         if len(text) > config.MAX_INPUT_CHARS:
#             logger.warning(f"Input text truncated to {config.MAX_INPUT_CHARS} characters.")
#             return text[:config.MAX_INPUT_CHARS]
#         return text

#     @retry(
#         stop=stop_after_attempt(3),
#         wait=wait_exponential(multiplier=1, min=4, max=30),
#         retry=retry_if_exception_type((RateLimitError, OllamaResponseError, json.JSONDecodeError, RequestException)),
#         reraise=True
#     )
#     def _call_llm(self, prompt: str, system_content: str, model_name: str = None, temperature: float = None, top_p: float = None, use_json_mode: bool = False) -> str:
#         """Makes a robust call to the selected LLM API with retry logic."""
#         if self.use_mock:
#             if use_json_mode: return json.dumps(self._mock_analysis())
#             return "This is a mock response for testing purposes."

#         if model_name is None: model_name = config.DEFAULT_OPENAI_MODEL

#         # --- REFACTORED: Logic to select the correct client and API call format ---
#         if model_name in config.OLLAMA_MODELS:
#             if not self.ollama_client:
#                 raise ConnectionError("Ollama client is not available or the server is not running.")
            
#             model_config = config.OLLAMA_MODELS[model_name]
#             options = {
#                 'temperature': temperature if temperature is not None else model_config.get('temperature', 0.7),
#                 'top_p': top_p if top_p is not None else model_config.get('top_p', 1.0)
#             }
#             logger.debug(f"Calling Ollama API with model: {model_name}")
#             messages = [{"role": "system", "content": system_content}, {"role": "user", "content": prompt}]
#             response = self.ollama_client.chat(model=model_name, messages=messages, options=options)
#             return response['message']['content'].strip()
        
#         elif model_name in config.GEMINI_MODELS:
#             if not self.gemini_client:
#                 raise ConnectionError("Gemini client is not available or API key is missing.")
            
#             model_config = config.GEMINI_MODELS[model_name]
#             gen_config = genai.types.GenerationConfig(
#                 temperature=temperature if temperature is not None else model_config.get('temperature', 0.7),
#                 top_p=top_p if top_p is not None else model_config.get('top_p', 1.0)
#             )
            
#             # Gemini combines system and user prompts
#             full_prompt = f"{system_content}\n\n{prompt}"
#             logger.debug(f"Calling Gemini API with model: {model_name}")
            
#             model = genai.GenerativeModel(model_name)
#             response = model.generate_content(full_prompt, generation_config=gen_config)

#             if not response.parts:
#                 raise ValueError(f"Gemini response was blocked or empty. Reason: {response.prompt_feedback}")
                
#             return response.text.strip()

#         elif model_name in config.OPENAI_MODELS:
#             if not self.openai_client:
#                 raise ValueError("OpenAI API key not configured.")
#             model_config = config.OPENAI_MODELS[model_name]
#             params = {
#                 "model": model_name,
#                 "messages": [{"role": "system", "content": system_content}, {"role": "user", "content": prompt}],
#                 "temperature": temperature if temperature is not None else model_config.get('temperature', 0.7),
#                 "top_p": top_p if top_p is not None else model_config.get('top_p', 1.0),
#             }
#             if use_json_mode and model_name in config.OPENAI_MODELS:
#                 params["response_format"] = {"type": "json_object"}
            
#             logger.debug(f"Calling OpenAI API with model: {model_name}")
#             response = self.openai_client.chat.completions.create(**params)
#             return response.choices[0].message.content.strip()
#         else:
#             raise ValueError(f"Model '{model_name}' is not configured in config.py under OPENAI_MODELS or OLLAMA_MODELS.")

#     def _validate_analysis_result(self, result: Dict) -> Dict:
#         """Validates the structure and content of the AI's analysis response."""
#         required_fields = ['overall_score', 'requirements_score', 'wishes_score', 'requirements', 'wishes']
#         for field in required_fields:
#             if field not in result: raise ValueError(f"Missing required field: {field}")
#         for key in ['overall_score', 'requirements_score', 'wishes_score']:
#             val = result.get(key)
#             if not isinstance(val, (int, float)) or not 0 <= val <= 100:
#                 raise ValueError(f"Invalid score value for {key}: {val}")
#         return result

#     def _get_cache_key(self, cv_text: str, assignment_text: str) -> str:
#         """Generates a unique cache key from the CV and assignment text."""
#         return hashlib.sha256((cv_text + assignment_text).encode()).hexdigest()

#     def _is_cache_valid(self, cache_file: str, ttl_hours: int = 24) -> bool:
#         """Checks if a cache file is still valid based on its age."""
#         if not os.path.exists(cache_file): return False
#         return (time.time() - os.path.getmtime(cache_file)) < (ttl_hours * 3600)

#     def analyze_cv_assignment_match(self, cv_text: str, assignment_text: str, model_name: str = None) -> Dict[str, Any]:
#         """Analyzes a CV against job requirements, with caching."""
#         if self.use_mock: return self._mock_analysis()
#         if not model_name: model_name = config.DEFAULT_OPENAI_MODEL
        
#         cv_text = self._sanitize_and_truncate_text(cv_text)
#         assignment_text = self._sanitize_and_truncate_text(assignment_text)
        
#         cache_key = self._get_cache_key(cv_text, assignment_text)
#         cache_file = os.path.join(config.CACHE_DIR, f"{cache_key}.json")
        
#         if self._is_cache_valid(cache_file):
#             logger.info(f"Returning cached result for key: {cache_key}")
#             with open(cache_file, 'r') as f: return json.load(f)
        
#         prompts = get_analyze_cv_prompt(cv_text, assignment_text, model_name)
#         content = self._call_llm(prompt=prompts['user'], system_content=prompts['system'], model_name=model_name, use_json_mode=True)
        
#         try:
#             clean_content = re.sub(r'``````', '', content).strip()
#             result = json.loads(clean_content)
#             result = self._validate_analysis_result(result)
#         except (json.JSONDecodeError, ValueError) as e:
#             logger.error(f"Failed to parse or validate AI response: {e}\nContent: {content}", exc_info=True)
#             raise ValueError("Failed to get a valid analysis from the AI model.")
            
#         with open(cache_file, 'w') as f: json.dump(result, f)
#         logger.info(f"Cached new analysis result with key: {cache_key}")
#         return result

#     def generate_motivations(self, cv_text: str, requirements: List[Dict], consultant_name: str, model_name: str = None) -> Dict[str, str]:
#         """Generates personalized motivations for each requirement."""
#         if self.use_mock: return {req['id']: "Mock motivation." for req in requirements}
        
#         motivations = {}
#         cv_text = self._sanitize_and_truncate_text(cv_text)
#         model_name = model_name or config.DEFAULT_OPENAI_MODEL
#         prompts = get_motivation_prompt(cv_text, "", model_name)
        
#         for req in requirements:
#             req_prompt = f"Generate a 2-3 sentence motivation for the requirement '{req['title']}' based on this CV..."
#             try:
#                 content = self._call_llm(prompt=req_prompt, system_content=prompts['system'], model_name=model_name)
#                 motivations[req['id']] = content
#             except Exception as e:
#                 logger.error(f"Error generating motivation for {req['id']}: {e}")
#                 motivations[req['id']] = f"Error: {e}"
#         return motivations

#     def generate_cover_letter(self, cv_text: str, assignment_info: Dict, consultant_name: str, analysis_result: Dict, model_name: str = None) -> str:
#         """Generates a professional cover letter."""
#         if self.use_mock: return "Mock cover letter for testing."
#         if not model_name: model_name = config.DEFAULT_OPENAI_MODEL
#         cv_text = self._sanitize_and_truncate_text(cv_text)
#         assignment_description = self._sanitize_and_truncate_text(assignment_info.get('description', ''))
#         prompts = get_cover_letter_prompt(cv_text, assignment_description, model_name)
#         return self._call_llm(prompt=prompts['user'], system_content=prompts['system'], model_name=model_name)

#     def generate_introduction_email(self, consultant_info: Dict, assignment_info: Dict, analysis_result: Dict, model_name: str = None) -> str:
#         """Generates a professional introduction email to a client."""
#         if self.use_mock: return "Mock email for testing."
#         if not model_name: model_name = config.DEFAULT_OPENAI_MODEL
#         email_prompt = f"Write an intro email for {consultant_info.get('name', 'the consultant')}..."
#         system_content = "You are an expert business communicator..."
#         return self._call_llm(prompt=email_prompt, system_content=system_content, model_name=model_name)

#     def customize_content(self, content_type: str, original_content: str, user_prompt: str, context: Dict = None, model_name: str = None) -> str:
#         """Customizes generated content based on user feedback."""
#         if self.use_mock: return f"Mock customized content for {content_type}."
#         if not model_name: model_name = config.DEFAULT_OPENAI_MODEL
#         prompts = get_customize_content_prompt(content_type, original_content, user_prompt, context, model_name)
#         return self._call_llm(prompt=prompts['user'], system_content=prompts['system'], model_name=model_name)











# import os
# import re
# import json
# import hashlib
# import time
# import logging
# from typing import Dict, List, Any, Optional
# import asyncio
# from functools import wraps

# from openai import OpenAI, RateLimitError
# from ollama import Client as OllamaClient, ResponseError as OllamaResponseError
# import google.generativeai as genai
# from requests.exceptions import RequestException
# from tenacity import retry, stop_after_attempt, wait_exponential, wait_random, retry_if_exception_type

# # Import from src package
# from src.config import config
# from src.analyzer.prompts import get_analyze_cv_prompt, get_cover_letter_prompt, get_customize_content_prompt, get_motivation_prompt

# try:
#     from ollama import Client as OllamaClient, ResponseError as OllamaResponseError
# except ImportError as e:
#     logging.error(f"Failed to import ollama: {e}")
#     OllamaClient = None
#     OllamaResponseError = None

# logger = logging.getLogger(__name__)


# def async_retry(*retry_args, **retry_kwargs):
#     """Decorator to make tenacity retry work with async functions."""
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             # Create a sync version for tenacity
#             @retry(*retry_args, **retry_kwargs)
#             def sync_version():
#                 return asyncio.run(func(*args, **kwargs))
            
#             return sync_version()
#         return wrapper
#     return decorator


# class CVAnalyzer:
#     """Service class for CV analysis using multiple LLM providers."""
    
#     def __init__(self):
#         """Initializes clients for all configured LLM providers."""
#         self.openai_client: Optional[OpenAI] = None
#         self.ollama_client: Optional[OllamaClient] = None
#         self.gemini_client: Optional[bool] = None
#         self.use_mock: bool = config.USE_MOCK

#         # Initialize OpenAI client if the API key is available
#         if config.OPENAI_API_KEY:
#             self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
#             logger.info("OpenAI client initialized.")
        
#         if config.GEMINI_API_KEY:
#             try:
#                 genai.configure(api_key=config.GEMINI_API_KEY)
#                 self.gemini_client = True # Flag success
#                 logger.info("Gemini client initialized.")
#             except Exception as e:
#                 logger.warning(f"Failed to initialize Gemini client: {e}")
#                 self.gemini_client = False

#         # Initialize Ollama client with retry logic
#         if OllamaClient is not None:
#             @retry(
#                 stop=stop_after_attempt(5),
#                 wait=wait_exponential(multiplier=1, min=2, max=10),
#                 retry=retry_if_exception_type((RequestException, ConnectionError)),
#                 reraise=True
#             )
#             def initialize_ollama_client():
#                 logger.debug(f"Attempting to initialize Ollama client with API base: {config.OLLAMA_API_BASE}")
#                 client = OllamaClient(host=config.OLLAMA_API_BASE)
#                 response = client.list()
#                 logger.debug(f"Ollama server responded with models: {response}")
#                 return client

#             try:
#                 self.ollama_client = initialize_ollama_client()
#                 logger.info("Ollama client initialized and server is responsive.")
#             except Exception as e:
#                 logger.warning(f"Could not connect to Ollama server. Local models will be unavailable. Error: {e}")
#                 self.ollama_client = None
#         else:
#             logger.warning("Ollama package not available. Local models will be unavailable.")

#         if not self.openai_client and not self.ollama_client and not self.use_mock:
#             raise ValueError("No API keys or local Ollama server configured. Application cannot proceed.")

#         os.makedirs(config.CACHE_DIR, exist_ok=True)

#     def _mock_analysis(self) -> Dict[str, Any]:
#         """Returns a predefined mock analysis for testing purposes."""
#         return {
#             "overall_score": 85, "requirements_score": 80, "wishes_score": 90,
#             "requirements": [{"id": "req_1", "type": "require", "title": "Python Development", "match": True, "percentage": 85, "explanation": "Strong Python experience"}],
#             "wishes": [{"id": "wish_1", "type": "wish", "title": "Machine Learning", "match": True, "percentage": 75, "explanation": "Some ML experience"}]
#         }

#     def _sanitize_and_truncate_text(self, text: str) -> str:
#         """Sanitizes and truncates input text."""
#         text = re.sub(r'<[^>]+>', '', text)
#         text = text.encode('ascii', 'ignore').decode('ascii')
#         text = re.sub(r'[^\w\s\-.,!?@#&()"\':;/\\]', ' ', text)
#         if len(text) > config.MAX_INPUT_CHARS:
#             logger.warning(f"Input text truncated to {config.MAX_INPUT_CHARS} characters.")
#             return text[:config.MAX_INPUT_CHARS]
#         return text

#     async def _call_llm_async(self, prompt: str, system_content: str, model_name: Optional[str] = None, 
#                              temperature: Optional[float] = None, top_p: Optional[float] = None, 
#                              use_json_mode: bool = False) -> str:
#         """Async wrapper for LLM calls - runs sync calls in thread pool."""
#         loop = asyncio.get_event_loop()
#         return await loop.run_in_executor(
#             None, 
#             self._call_llm, 
#             prompt, system_content, model_name, temperature, top_p, use_json_mode
#         )

#     @retry(
#         stop=stop_after_attempt(3),
#         wait=wait_exponential(multiplier=1, min=4, max=30),
#         retry=retry_if_exception_type((RateLimitError, OllamaResponseError, json.JSONDecodeError, RequestException)),
#         reraise=True
#     )
#     def _call_llm(self, prompt: str, system_content: str, model_name: Optional[str] = None, 
#                   temperature: Optional[float] = None, top_p: Optional[float] = None, 
#                   use_json_mode: bool = False) -> str:
#         """Makes a robust call to the selected LLM API with retry logic."""
#         if self.use_mock:
#             if use_json_mode: 
#                 return json.dumps(self._mock_analysis())
#             return "This is a mock response for testing purposes."

#         if model_name is None: 
#             model_name = config.DEFAULT_OPENAI_MODEL

#         # Logic to select the correct client and API call format
#         if model_name in config.OLLAMA_MODELS:
#             if not self.ollama_client:
#                 raise ConnectionError("Ollama client is not available or the server is not running.")
            
#             model_config = config.OLLAMA_MODELS[model_name]
#             options = {
#                 'temperature': temperature if temperature is not None else model_config.get('temperature', 0.7),
#                 'top_p': top_p if top_p is not None else model_config.get('top_p', 1.0)
#             }
#             logger.debug(f"Calling Ollama API with model: {model_name}")
#             messages = [{"role": "system", "content": system_content}, {"role": "user", "content": prompt}]
#             response = self.ollama_client.chat(model=model_name, messages=messages, options=options)
#             return response['message']['content'].strip()
        
#         elif model_name in config.GEMINI_MODELS:
#             if not self.gemini_client:
#                 raise ConnectionError("Gemini client is not available or API key is missing.")
            
#             model_config = config.GEMINI_MODELS[model_name]
#             gen_config = genai.types.GenerationConfig(
#                 temperature=temperature if temperature is not None else model_config.get('temperature', 0.7),
#                 top_p=top_p if top_p is not None else model_config.get('top_p', 1.0)
#             )
            
#             # Gemini combines system and user prompts
#             full_prompt = f"{system_content}\n\n{prompt}"
#             logger.debug(f"Calling Gemini API with model: {model_name}")
            
#             model = genai.GenerativeModel(model_name)
#             response = model.generate_content(full_prompt, generation_config=gen_config)

#             if not response.parts:
#                 raise ValueError(f"Gemini response was blocked or empty. Reason: {response.prompt_feedback}")
                
#             return response.text.strip()

#         elif model_name in config.OPENAI_MODELS:
#             if not self.openai_client:
#                 raise ValueError("OpenAI API key not configured.")
#             model_config = config.OPENAI_MODELS[model_name]
#             params = {
#                 "model": model_name,
#                 "messages": [{"role": "system", "content": system_content}, {"role": "user", "content": prompt}],
#                 "temperature": temperature if temperature is not None else model_config.get('temperature', 0.7),
#                 "top_p": top_p if top_p is not None else model_config.get('top_p', 1.0),
#             }
#             if use_json_mode and model_name in config.OPENAI_MODELS:
#                 params["response_format"] = {"type": "json_object"}
            
#             logger.debug(f"Calling OpenAI API with model: {model_name}")
#             response = self.openai_client.chat.completions.create(**params)
#             return response.choices[0].message.content.strip()
#         else:
#             raise ValueError(f"Model '{model_name}' is not configured in config.py under OPENAI_MODELS or OLLAMA_MODELS.")

#     def _validate_analysis_result(self, result: Dict) -> Dict:
#         """Validates the structure and content of the AI's analysis response."""
#         required_fields = ['overall_score', 'requirements_score', 'wishes_score', 'requirements', 'wishes']
#         for field in required_fields:
#             if field not in result: 
#                 raise ValueError(f"Missing required field: {field}")
#         for key in ['overall_score', 'requirements_score', 'wishes_score']:
#             val = result.get(key)
#             if not isinstance(val, (int, float)) or not 0 <= val <= 100:
#                 raise ValueError(f"Invalid score value for {key}: {val}")
#         return result

#     def _get_cache_key(self, cv_text: str, assignment_text: str) -> str:
#         """Generates a unique cache key from the CV and assignment text."""
#         return hashlib.sha256((cv_text + assignment_text).encode()).hexdigest()

#     def _is_cache_valid(self, cache_file: str, ttl_hours: int = 24) -> bool:
#         """Checks if a cache file is still valid based on its age."""
#         if not os.path.exists(cache_file): 
#             return False
#         return (time.time() - os.path.getmtime(cache_file)) < (ttl_hours * 3600)

#     async def analyze_cv_assignment_match(self, cv_text: str, assignment_text: str, 
#                                         model_name: Optional[str] = None) -> Dict[str, Any]:
#         """Analyzes a CV against job requirements, with caching. Now async for FastAPI."""
#         if self.use_mock: 
#             return self._mock_analysis()
#         if not model_name: 
#             model_name = config.DEFAULT_OPENAI_MODEL
        
#         cv_text = self._sanitize_and_truncate_text(cv_text)
#         assignment_text = self._sanitize_and_truncate_text(assignment_text)
        
#         cache_key = self._get_cache_key(cv_text, assignment_text)
#         cache_file = os.path.join(config.CACHE_DIR, f"{cache_key}.json")
        
#         if self._is_cache_valid(cache_file):
#             logger.info(f"Returning cached result for key: {cache_key}")
#             with open(cache_file, 'r') as f: 
#                 return json.load(f)
        
#         prompts = get_analyze_cv_prompt(cv_text, assignment_text, model_name)
#         content = await self._call_llm_async(
#             prompt=prompts['user'], 
#             system_content=prompts['system'], 
#             model_name=model_name, 
#             use_json_mode=True
#         )
        
#         try:
#             clean_content = re.sub(r'``````', '', content).strip()
#             result = json.loads(clean_content)
#             result = self._validate_analysis_result(result)
#         except (json.JSONDecodeError, ValueError) as e:
#             logger.error(f"Failed to parse or validate AI response: {e}\nContent: {content}", exc_info=True)
#             raise ValueError("Failed to get a valid analysis from the AI model.")
            
#         with open(cache_file, 'w') as f: 
#             json.dump(result, f)
#         logger.info(f"Cached new analysis result with key: {cache_key}")
#         return result

#     async def generate_motivations(self, cv_text: str, requirements: List[Dict], 
#                                  consultant_name: str, model_name: Optional[str] = None) -> Dict[str, str]:
#         """Generates personalized motivations for each requirement. Now async."""
#         if self.use_mock: 
#             return {req['id']: "Mock motivation." for req in requirements}
        
#         motivations = {}
#         cv_text = self._sanitize_and_truncate_text(cv_text)
#         model_name = model_name or config.DEFAULT_OPENAI_MODEL
#         prompts = get_motivation_prompt(cv_text, "", model_name)
        
#         # Process requirements concurrently
#         async def process_requirement(req):
#             req_prompt = f"Generate a 2-3 sentence motivation for the requirement '{req['title']}' based on this CV..."
#             try:
#                 content = await self._call_llm_async(
#                     prompt=req_prompt, 
#                     system_content=prompts['system'], 
#                     model_name=model_name
#                 )
#                 return req['id'], content
#             except Exception as e:
#                 logger.error(f"Error generating motivation for {req['id']}: {e}")
#                 return req['id'], f"Error: {e}"
        
#         # Execute all requirement processing concurrently
#         tasks = [process_requirement(req) for req in requirements]
#         results = await asyncio.gather(*tasks)
        
#         for req_id, content in results:
#             motivations[req_id] = content
            
#         return motivations

#     async def generate_cover_letter(self, cv_text: str, assignment_info: Dict, consultant_name: str, 
#                                   analysis_result: Dict, model_name: Optional[str] = None) -> str:
#         """Generates a professional cover letter. Now async."""
#         if self.use_mock: 
#             return "Mock cover letter for testing."
#         if not model_name: 
#             model_name = config.DEFAULT_OPENAI_MODEL
#         cv_text = self._sanitize_and_truncate_text(cv_text)
#         assignment_description = self._sanitize_and_truncate_text(assignment_info.get('description', ''))
#         prompts = get_cover_letter_prompt(cv_text, assignment_description, model_name)
#         return await self._call_llm_async(
#             prompt=prompts['user'], 
#             system_content=prompts['system'], 
#             model_name=model_name
#         )

#     async def generate_introduction_email(self, consultant_info: Dict, assignment_info: Dict, 
#                                         analysis_result: Dict, model_name: Optional[str] = None) -> str:
#         """Generates a professional introduction email to a client. Now async."""
#         if self.use_mock: 
#             return "Mock email for testing."
#         if not model_name: 
#             model_name = config.DEFAULT_OPENAI_MODEL
#         email_prompt = f"Write an intro email for {consultant_info.get('name', 'the consultant')}..."
#         system_content = "You are an expert business communicator..."
#         return await self._call_llm_async(
#             prompt=email_prompt, 
#             system_content=system_content, 
#             model_name=model_name
#         )

#     async def customize_content(self, content_type: str, original_content: str, user_prompt: str, 
#                               context: Optional[Dict] = None, model_name: Optional[str] = None) -> str:
#         """Customizes generated content based on user feedback. Now async."""
#         if self.use_mock: 
#             return f"Mock customized content for {content_type}."
#         if not model_name: 
#             model_name = config.DEFAULT_OPENAI_MODEL
#         prompts = get_customize_content_prompt(content_type, original_content, user_prompt, context, model_name)
#         return await self._call_llm_async(
#             prompt=prompts['user'], 
#             system_content=prompts['system'], 
#             model_name=model_name
#         )





import os
import re
import json
import hashlib
import time
import logging
from typing import Dict, List, Any, Optional
import asyncio
from functools import wraps

from openai import OpenAI, RateLimitError
from ollama import Client as OllamaClient, ResponseError as OllamaResponseError
import google.generativeai as genai
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential, wait_random, retry_if_exception_type

# Import from src package
from src.config import config
from src.analyzer.prompts import get_analyze_cv_prompt, get_cover_letter_prompt, get_customize_content_prompt, get_motivation_prompt

try:
    from ollama import Client as OllamaClient, ResponseError as OllamaResponseError
except ImportError as e:
    logging.error(f"Failed to import ollama: {e}")
    OllamaClient = None
    OllamaResponseError = None

logger = logging.getLogger(__name__)

def async_retry(*retry_args, **retry_kwargs):
    """Decorator to make tenacity retry work with async functions."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create a sync version for tenacity
            @retry(*retry_args, **retry_kwargs)
            def sync_version():
                return asyncio.run(func(*args, **kwargs))
            
            return sync_version()
        return wrapper
    return decorator

class CVAnalyzer:
    """Service class for CV analysis using multiple LLM providers."""
    
    def __init__(self):
        """Initializes clients for all configured LLM providers."""
        self.openai_client: Optional[OpenAI] = None
        self.ollama_client: Optional[OllamaClient] = None
        self.gemini_client: Optional[bool] = None
        self.use_mock: bool = config.USE_MOCK

        # Initialize OpenAI client if the API key is available
        if config.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=config.OPENAI_API_KEY)
            logger.info("OpenAI client initialized.")
        
        if config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=config.GEMINI_API_KEY)
                self.gemini_client = True # Flag success
                logger.info("Gemini client initialized.")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini client: {e}")
                self.gemini_client = False

        # Initialize Ollama client with retry logic
        if OllamaClient is not None:
            @retry(
                stop=stop_after_attempt(5),
                wait=wait_exponential(multiplier=1, min=2, max=10),
                retry=retry_if_exception_type((RequestException, ConnectionError)),
                reraise=True
            )
            def initialize_ollama_client():
                logger.debug(f"Attempting to initialize Ollama client with API base: {config.OLLAMA_API_BASE}")
                client = OllamaClient(host=config.OLLAMA_API_BASE)
                response = client.list()
                logger.debug(f"Ollama server responded with models: {response}")
                return client

            try:
                self.ollama_client = initialize_ollama_client()
                logger.info("Ollama client initialized and server is responsive.")
            except Exception as e:
                logger.warning(f"Could not connect to Ollama server. Local models will be unavailable. Error: {e}")
                self.ollama_client = None
        else:
            logger.warning("Ollama package not available. Local models will be unavailable.")

        if not self.openai_client and not self.ollama_client and not self.use_mock:
            raise ValueError("No API keys or local Ollama server configured. Application cannot proceed.")

        os.makedirs(config.CACHE_DIR, exist_ok=True)

    def _mock_analysis(self) -> Dict[str, Any]:
        """Returns a predefined mock analysis for testing purposes."""
        return {
            "overall_score": 85, "requirements_score": 80, "wishes_score": 90,
            "requirements": [{"id": "req_1", "type": "require", "title": "Python Development", "match": True, "percentage": 85, "explanation": "Strong Python experience"}],
            "wishes": [{"id": "wish_1", "type": "wish", "title": "Machine Learning", "match": True, "percentage": 75, "explanation": "Some ML experience"}]
        }

    def _sanitize_and_truncate_text(self, text: str) -> str:
        """Sanitizes and truncates input text."""
        text = re.sub(r'<[^>]+>', '', text)
        text = text.encode('ascii', 'ignore').decode('ascii')
        text = re.sub(r'[^\w\s\-.,!?@#&()"\':;/\\]', ' ', text)
        if len(text) > config.MAX_INPUT_CHARS:
            logger.warning(f"Input text truncated to {config.MAX_INPUT_CHARS} characters.")
            return text[:config.MAX_INPUT_CHARS]
        return text

    async def _call_llm_async(self, prompt: str, system_content: str, model_name: Optional[str] = None, 
                             temperature: Optional[float] = None, top_p: Optional[float] = None, 
                             use_json_mode: bool = False) -> str:
        """Async wrapper for LLM calls - runs sync calls in thread pool."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            self._call_llm, 
            prompt, system_content, model_name, temperature, top_p, use_json_mode
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=30),
        retry=retry_if_exception_type((RateLimitError, OllamaResponseError, json.JSONDecodeError, RequestException)),
        reraise=True
    )
    def _call_llm(self, prompt: str, system_content: str, model_name: Optional[str] = None, 
                  temperature: Optional[float] = None, top_p: Optional[float] = None, 
                  use_json_mode: bool = False) -> str:
        """Makes a robust call to the selected LLM API with retry logic."""
        if self.use_mock:
            if use_json_mode: 
                return json.dumps(self._mock_analysis())
            return "This is a mock response for testing purposes."

        if model_name is None: 
            model_name = config.DEFAULT_OPENAI_MODEL

        # Logic to select the correct client and API call format
        if model_name in config.OLLAMA_MODELS:
            if not self.ollama_client:
                raise ConnectionError("Ollama client is not available or the server is not running.")
            
            model_config = config.OLLAMA_MODELS[model_name]
            options = {
                'temperature': temperature if temperature is not None else model_config.get('temperature', 0.7),
                'top_p': top_p if top_p is not None else model_config.get('top_p', 1.0)
            }
            logger.debug(f"Calling Ollama API with model: {model_name}")
            messages = [{"role": "system", "content": system_content}, {"role": "user", "content": prompt}]
            response = self.ollama_client.chat(model=model_name, messages=messages, options=options)
            return response['message']['content'].strip()
        
        elif model_name in config.GEMINI_MODELS:
            if not self.gemini_client:
                raise ConnectionError("Gemini client is not available or API key is missing.")
            
            model_config = config.GEMINI_MODELS[model_name]
            gen_config = genai.types.GenerationConfig(
                temperature=temperature if temperature is not None else model_config.get('temperature', 0.7),
                top_p=top_p if top_p is not None else model_config.get('top_p', 1.0)
            )
            
            # Gemini combines system and user prompts
            full_prompt = f"{system_content}\n\n{prompt}"
            logger.debug(f"Calling Gemini API with model: {model_name}")
            
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(full_prompt, generation_config=gen_config)

            if not response.parts:
                raise ValueError(f"Gemini response was blocked or empty. Reason: {response.prompt_feedback}")
                
            return response.text.strip()

        elif model_name in config.OPENAI_MODELS:
            if not self.openai_client:
                raise ValueError("OpenAI API key not configured.")
            model_config = config.OPENAI_MODELS[model_name]
            params = {
                "model": model_name,
                "messages": [{"role": "system", "content": system_content}, {"role": "user", "content": prompt}],
                "temperature": temperature if temperature is not None else model_config.get('temperature', 0.7),
                "top_p": top_p if top_p is not None else model_config.get('top_p', 1.0),
            }
            if use_json_mode and model_name in config.OPENAI_MODELS:
                params["response_format"] = {"type": "json_object"}
            
            logger.debug(f"Calling OpenAI API with model: {model_name}")
            response = self.openai_client.chat.completions.create(**params)
            return response.choices[0].message.content.strip()
        else:
            # Fallback for unknown models - try OpenAI first
            logger.warning(f"Unknown model '{model_name}', attempting to use with OpenAI API")
            if not self.openai_client:
                raise ValueError(f"Model '{model_name}' is not configured and OpenAI client is not available.")
            
            # Try with OpenAI
            params = {
                "model": model_name,
                "messages": [{"role": "system", "content": system_content}, {"role": "user", "content": prompt}],
                "temperature": temperature if temperature is not None else 0.7,
                "top_p": top_p if top_p is not None else 1.0,
            }
            if use_json_mode:
                params["response_format"] = {"type": "json_object"}
            
            logger.debug(f"Calling OpenAI API with unknown model: {model_name}")
            response = self.openai_client.chat.completions.create(**params)
            return response.choices[0].message.content.strip()

    def _validate_analysis_result(self, result: Dict) -> Dict:
        """Validates the structure and content of the AI's analysis response."""
        required_fields = ['overall_score', 'requirements_score', 'wishes_score', 'requirements', 'wishes']
        for field in required_fields:
            if field not in result: 
                raise ValueError(f"Missing required field: {field}")
        for key in ['overall_score', 'requirements_score', 'wishes_score']:
            val = result.get(key)
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
        return (time.time() - os.path.getmtime(cache_file)) < (ttl_hours * 3600)

    async def analyze_cv_assignment_match(self, cv_text: str, assignment_text: str, 
                                        model_name: Optional[str] = None) -> Dict[str, Any]:
        """Analyzes a CV against job requirements, with caching. Now async for FastAPI."""
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
        
        prompts = get_analyze_cv_prompt(cv_text, assignment_text, model_name)
        content = await self._call_llm_async(
            prompt=prompts['user'], 
            system_content=prompts['system'], 
            model_name=model_name, 
            use_json_mode=True
        )
        
        try:
            clean_content = re.sub(r'``````', '', content).strip()
            result = json.loads(clean_content)
            result = self._validate_analysis_result(result)
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Failed to parse or validate AI response: {e}\nContent: {content}", exc_info=True)
            raise ValueError("Failed to get a valid analysis from the AI model.")
            
        with open(cache_file, 'w') as f: 
            json.dump(result, f)
        logger.info(f"Cached new analysis result with key: {cache_key}")
        return result

    async def generate_motivations(self, cv_text: str, requirements: List[Dict], 
                                 consultant_name: str, model_name: Optional[str] = None) -> Dict[str, str]:
        """Generates personalized motivations for each requirement. Now async."""
        if self.use_mock: 
            return {req['id']: "Mock motivation for testing." for req in requirements}
        
        motivations = {}
        cv_text = self._sanitize_and_truncate_text(cv_text)
        model_name = model_name or config.DEFAULT_OPENAI_MODEL
        
        # Process requirements concurrently
        async def process_requirement(req):
            # Create a specific prompt that includes the CV content
            system_content = f"""You are an expert at writing compelling professional motivations for job applications. 
            Write a personalized 2-3 sentence motivation that shows how the candidate's experience aligns with the specific requirement. 
            Be specific, professional, and confident. Do not ask for more information - use the provided CV content."""
            
            user_prompt = f"""Based on this CV content, write a compelling motivation for the requirement: "{req['title']}"

CV CONTENT:
{cv_text}

REQUIREMENT DETAILS:
- Title: {req['title']}
- Description: {req.get('description', req['title'])}
- Match Percentage: {req.get('percentage', 0)}%

Write a professional motivation that:
1. Highlights relevant experience from the CV
2. Shows alignment with this specific requirement  
3. Demonstrates confidence and enthusiasm
4. Is 2-3 sentences maximum

Do not ask for more information. Generate the motivation based on the provided CV content."""

            try:
                content = await self._call_llm_async(
                    prompt=user_prompt, 
                    system_content=system_content, 
                    model_name=model_name
                )
                return req['id'], content.strip()
            except Exception as e:
                logger.error(f"Error generating motivation for {req['id']}: {e}")
                return req['id'], f"Strong alignment with {req['title']} based on relevant experience and skills demonstrated in the CV."
        
        # Execute all requirement processing concurrently
        tasks = [process_requirement(req) for req in requirements]
        results = await asyncio.gather(*tasks)
        
        for req_id, content in results:
            motivations[req_id] = content
            
        return motivations

    async def generate_cover_letter(self, cv_text: str, assignment_info: Dict, consultant_name: str, 
                                  analysis_result: Dict, model_name: Optional[str] = None) -> str:
        """Generates a professional cover letter. Now async."""
        if self.use_mock: 
            return "Mock cover letter for testing."
        if not model_name: 
            model_name = config.DEFAULT_OPENAI_MODEL
        
        cv_text = self._sanitize_and_truncate_text(cv_text)
        assignment_description = self._sanitize_and_truncate_text(assignment_info.get('description', ''))
        
        system_content = """You are an expert professional cover letter writer. Create compelling, personalized cover letters that showcase the candidate's qualifications and enthusiasm. Write in a professional tone with proper business letter formatting."""
        
        user_prompt = f"""Write a professional cover letter for {consultant_name} applying for a software developer position.

CANDIDATE CV CONTENT:
{cv_text}

JOB REQUIREMENTS:
{assignment_description}

ANALYSIS RESULTS:
Overall Match: {analysis_result.get('overall_score', 0)}%
Requirements Score: {analysis_result.get('requirements_score', 0)}%

Format the cover letter as follows:
[Your Name]
[Your Address]
[City, State, ZIP Code]
[Your Phone Number]
[Your Email Address]
[LinkedIn Profile]

[Date]

[Hiring Manager]
[Company Name]
[Company Address]
[City, State, ZIP Code]

Dear Hiring Manager,

[Write 3-4 well-structured paragraphs that include:]
1. Strong opening paragraph stating the position and enthusiasm
2. Technical skills and relevant experience paragraph with specific examples from the CV
3. Problem-solving and collaboration achievements paragraph
4. Company alignment and closing with call to action

Sincerely,
{consultant_name}

Make it specific to the candidate's experience and the job requirements. Be professional and confident."""

        return await self._call_llm_async(
            prompt=user_prompt, 
            system_content=system_content, 
            model_name=model_name
        )

    async def generate_introduction_email(self, consultant_info: Dict, assignment_info: Dict, 
                                        analysis_result: Dict, model_name: Optional[str] = None) -> str:
        """Generates a professional introduction email to a client. Now async."""
        if self.use_mock: 
            return "Mock email for testing."
        if not model_name: 
            model_name = config.DEFAULT_OPENAI_MODEL
        
        consultant_name = consultant_info.get('name', 'the consultant')
        company_name = assignment_info.get('company_name', '[Company Name]')
        position = assignment_info.get('position', 'Software Developer')
        
        system_content = """You are an expert at writing professional introduction emails. Create concise, engaging emails that introduce candidates effectively to potential employers or clients. Do not ask for more information."""
        
        user_prompt = f"""Write a professional introduction email for {consultant_name}.

CONSULTANT INFO:
{consultant_info}

POSITION INFO:
Position: {position}
Company: {company_name}
Assignment Details: {assignment_info.get('description', '')}

ANALYSIS RESULTS:
Overall Match: {analysis_result.get('overall_score', 0)}%

Format:
Subject: Introduction: {consultant_name} - {position} Opportunity

Dear [Recipient's Name],

I hope this message finds you well. I am writing to introduce {consultant_name}, a highly qualified software developer who would be an excellent fit for your {position} position.

[2-3 paragraphs highlighting:]
- Key technical qualifications
- Relevant experience and achievements  
- Why they're a strong match for the role
- Professional background and skills

I believe {consultant_name} would be a valuable addition to your team and would welcome the opportunity to discuss this further.

Best regards,

[Your Name]
[Your Title]
[Contact Information]

Make it professional, concise, and compelling. Do not ask for additional information."""

        return await self._call_llm_async(
            prompt=user_prompt, 
            system_content=system_content, 
            model_name=model_name
        )

    async def customize_content(self, content_type: str, original_content: str, user_prompt: str, 
                              context: Optional[Dict] = None, model_name: Optional[str] = None) -> str:
        """Customizes generated content based on user feedback. Now async."""
        if self.use_mock: 
            return f"Mock customized content for {content_type}."
        if not model_name: 
            model_name = config.DEFAULT_OPENAI_MODEL
        prompts = get_customize_content_prompt(content_type, original_content, user_prompt, context, model_name)
        return await self._call_llm_async(
            prompt=prompts['user'], 
            system_content=prompts['system'], 
            model_name=model_name
        )
