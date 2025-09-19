# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from openai import OpenAI, RateLimitError
# import os
# from typing import Dict, List, Any
# import json
# import PyPDF2
# import docx
# from io import BytesIO
# import logging
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
# from dotenv import load_dotenv
# import hashlib

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# class CVAnalyzer:
#     def __init__(self):
#         api_key = os.getenv('OPENAI_API_KEY')
#         if not api_key:
#             raise ValueError("OPENAI_API_KEY not set in .env file")
#         self.client = OpenAI(api_key=api_key)
#         self.use_mock = os.getenv('USE_MOCK', 'False').lower() == 'true'

#     def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
#         """Extract text from uploaded file based on file type"""
#         try:
#             if filename.lower().endswith('.pdf'):
#                 return self._extract_from_pdf(file_content)
#             elif filename.lower().endswith(('.doc', '.docx')):
#                 return self._extract_from_docx(file_content)
#             elif filename.lower().endswith('.txt'):
#                 return file_content.decode('utf-8')
#             else:
#                 raise ValueError(f"Unsupported file type: {filename}")
#         except Exception as e:
#             raise Exception(f"Error extracting text from {filename}: {str(e)}")

#     def _extract_from_pdf(self, file_content: bytes) -> str:
#         """Extract text from PDF file"""
#         pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
#         text = ""
#         for page in pdf_reader.pages:
#             extracted = page.extract_text()
#             if extracted:
#                 text += extracted + "\n"
#         return text

#     def _extract_from_docx(self, file_content: bytes) -> str:
#         """Extract text from DOCX file"""
#         doc = docx.Document(BytesIO(file_content))
#         text = ""
#         for paragraph in doc.paragraphs:
#             text += paragraph.text + "\n"
#         return text

#     def _mock_analysis(self) -> Dict[str, Any]:
#         """Mock response for testing without API"""
#         return {
#             "overall_score": 85,
#             "requirements_score": 90,
#             "wishes_score": 80,
#             "requirements": [
#                 {
#                     "id": "req1",
#                     "type": "require",
#                     "title": "SQL Proficiency",
#                     "description": "Advanced SQL skills",
#                     "match": True,
#                     "percentage": 95,
#                     "explanation": "CV shows 5+ years of SQL experience in data analysis projects."
#                 }
#             ],
#             "wishes": [
#                 {
#                     "id": "wish1",
#                     "type": "wish",
#                     "title": "Power BI Experience",
#                     "description": "Familiarity with Power BI",
#                     "match": True,
#                     "percentage": 80,
#                     "explanation": "CV mentions dashboard creation with Power BI."
#                 }
#             ]
#         }

#     @retry(
#         stop=stop_after_attempt(5),  # Increased retries
#         wait=wait_exponential(multiplier=2, min=4, max=60),  # Longer backoff
#         retry=retry_if_exception_type((RateLimitError, json.JSONDecodeError))
#     )
#     def _call_openai(self, prompt: str, system_content: str, temperature: float = 0.3) -> str:
#         """Internal API call with retry"""
#         try:
#             response = self.client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": system_content},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=temperature
#             )
#             content = response.choices[0].message.content.strip()
#             logging.debug(f"Raw OpenAI response: {content}")
#             return content
#         except RateLimitError as e:
#             logging.error(f"Rate limit exceeded: {str(e)}")
#             raise
#         except Exception as e:
#             logging.error(f"OpenAI API error: {str(e)}")
#             raise

#     def analyze_cv_assignment_match(self, cv_text: str, assignment_text: str) -> Dict[str, Any]:
#         """Analyze CV against assignment requirements using GPT-3.5-turbo"""
#         if self.use_mock:
#             logging.debug("Using mock analysis response")
#             return self._mock_analysis()

#         # Validate assignment_text
#         if not assignment_text or assignment_text.isspace():
#             logging.error("Assignment requirements are empty")
#             return {
#                 "overall_score": 0,
#                 "requirements_score": 0,
#                 "wishes_score": 0,
#                 "requirements": [],
#                 "wishes": [],
#                 "error": "Assignment requirements cannot be empty"
#             }

#         # Truncate inputs to reduce tokens (reduced to 1000)
#         cv_text = cv_text[:1000]
#         assignment_text = assignment_text[:1000]

#         # Cache key based on inputs
#         cache_key = hashlib.md5((cv_text + assignment_text).encode()).hexdigest()
#         cache_file = f"cache/{cache_key}.json"
#         if os.path.exists(cache_file):
#             logging.debug(f"Returning cached result for key: {cache_key}")
#             with open(cache_file, 'r') as f:
#                 return json.load(f)

#         prompt = f"""
#         You are an expert HR consultant specializing in data professional recruitment.
#         Analyze the provided CV against the assignment requirements and return a response in **valid JSON format only**.
#         Do not include any text outside the JSON object, such as explanations or code fences.

#         ASSIGNMENT REQUIREMENTS:
#         {assignment_text}

#         CONSULTANT CV:
#         {cv_text}

#         Return a JSON object with the following structure:
#         {{
#             "overall_score": <number 0-100>,
#             "requirements_score": <number 0-100>,
#             "wishes_score": <number 0-100>,
#             "requirements": [
#                 {{
#                     "id": "<unique_id>",
#                     "type": "require",
#                     "title": "<requirement_title>",
#                     "description": "<requirement_description>",
#                     "match": <boolean>,
#                     "percentage": <number 0-100>,
#                     "explanation": "<detailed_explanation>"
#                 }}
#             ],
#             "wishes": [
#                 {{
#                     "id": "<unique_id>",
#                     "type": "wish",
#                     "title": "<wish_title>",
#                     "description": "<wish_description>",
#                     "match": <boolean>,
#                     "percentage": <number 0-100>,
#                     "explanation": "<detailed_explanation>"
#                 }}
#             ]
#         }}

#         Focus on:
#         - Technical skills matching (e.g., Azure, SQL, Power BI)
#         - Experience relevance
#         - Education requirements
#         - Soft skills and cultural fit
#         - Provide specific examples from the CV

#         If no requirements are provided, return an empty requirements and wishes list with scores of 0.
#         Ensure the response is a valid JSON object with no additional text or code fences.
#         """

#         try:
#             content = self._call_openai(
#                 prompt,
#                 "You are an expert HR consultant. Return only valid JSON with no additional text or code fences."
#             )
#             result = json.loads(content)

#             # Cache result
#             os.makedirs("cache", exist_ok=True)
#             with open(cache_file, 'w') as f:
#                 json.dump(result, f)
#             logging.debug(f"Cached result for key: {cache_key}")

#             return result
#         except json.JSONDecodeError as e:
#             logging.error(f"JSON parsing error: {e}, raw content: {content}")
#             return {
#                 "overall_score": 0,
#                 "requirements_score": 0,
#                 "wishes_score": 0,
#                 "requirements": [],
#                 "wishes": [],
#                 "error": f"Invalid JSON response from OpenAI: {str(e)}"
#             }
#         except RateLimitError as e:
#             logging.error(f"Rate limit error: {str(e)}")
#             return {
#                 "overall_score": 0,
#                 "requirements_score": 0,
#                 "wishes_score": 0,
#                 "requirements": [],
#                 "wishes": [],
#                 "error": "Rate limit exceeded. Please try again later or upgrade your OpenAI plan."
#             }
#         except Exception as e:
#             logging.error(f"API error: {str(e)}")
#             return {
#                 "overall_score": 0,
#                 "requirements_score": 0,
#                 "wishes_score": 0,
#                 "requirements": [],
#                 "wishes": [],
#                 "error": f"Error in CV analysis: {str(e)}"
#             }

#     def generate_motivations(self, cv_text: str, requirements: List[Dict], consultant_name: str) -> Dict[str, str]:
#         """Generate personalized motivations for each requirement"""
#         if self.use_mock:
#             return {req['id']: "Mock motivation for testing." for req in requirements}

#         motivations = {}
#         cv_text = cv_text[:1000]  # Truncate

#         for req in requirements:
#             prompt = f"""
#             Generate a personalized motivation for the following requirement based on the consultant's CV.
            
#             CONSULTANT: {consultant_name}
#             REQUIREMENT: {req['title']} - {req['description']}
#             MATCH PERCENTAGE: {req['percentage']}%
            
#             CV CONTENT:
#             {cv_text}
            
#             Write a 2-3 sentence motivation that:
#             - Specifically addresses this requirement
#             - Uses concrete examples from the CV
#             - Shows relevant experience and skills
#             - Maintains professional tone
            
#             If the match is low, acknowledge the gap but highlight transferable skills.
#             """

#             try:
#                 content = self._call_openai(
#                     prompt,
#                     "You are an expert at writing compelling, specific motivations for job requirements.",
#                     temperature=0.4
#                 )
#                 motivations[req['id']] = content
#             except RateLimitError:
#                 motivations[req['id']] = "Rate limit exceeded. Please try again later."
#             except Exception as e:
#                 motivations[req['id']] = f"Error generating motivation: {str(e)}"

#         return motivations

#     def generate_cover_letter(self, cv_text: str, assignment_info: Dict, consultant_name: str, analysis_result: Dict) -> str:
#         """Generate a personalized cover letter"""
#         if self.use_mock:
#             return "Mock cover letter for testing."

#         cv_text = cv_text[:1000]  # Reduced truncation
#         prompt = f"""
#         Write a professional cover letter for the following consultant and assignment.
        
#         CONSULTANT: {consultant_name}
#         CLIENT: {assignment_info.get('client', 'the client')}
#         POSITION: {assignment_info.get('title', 'the position')}
#         OVERALL MATCH SCORE: {analysis_result.get('overall_score', 0)}%
        
#         CV CONTENT:
#         {cv_text}
        
#         ASSIGNMENT DESCRIPTION:
#         {assignment_info.get('description', '')[:1000]}
        
#         Write a compelling cover letter that:
#         - Opens with a strong, personalized introduction
#         - Highlights the most relevant experience and skills
#         - Addresses any potential concerns (like education gaps) proactively
#         - Shows enthusiasm for the specific role and company
#         - Maintains professional yet personal tone
#         - Ends with a clear call to action
#         - Is approximately 300-400 words
        
#         Use specific examples from the CV and make it feel authentic to the consultant's background.
#         """

#         try:
#             content = self._call_openai(
#                 prompt,
#                 "You are an expert at writing compelling, personalized cover letters for data professionals.",
#                 temperature=0.5
#             )
#             return content
#         except RateLimitError:
#             return "Rate limit exceeded. Please try again later."
#         except Exception as e:
#             return f"Error generating cover letter: {str(e)}"

#     def generate_introduction_email(self, consultant_info: Dict, assignment_info: Dict, analysis_result: Dict) -> str:
#         """Generate a professional introduction email"""
#         if self.use_mock:
#             return "Mock email for testing."

#         consultant_name = consultant_info.get('name', 'the consultant')
#         client_name = assignment_info.get('client', 'the client')
#         position_title = assignment_info.get('title', 'the position')
#         contact_person = consultant_info.get('contactPerson', 'Sir/Madam')
#         overall_score = analysis_result.get('overall_score', 0)

#         prompt = f"""
#         Write a professional introduction email from a staffing agency to a client.
        
#         CONSULTANT: {consultant_name}
#         CLIENT: {client_name}
#         POSITION: {position_title}
#         CONTACT PERSON: {contact_person}
#         MATCH SCORE: {overall_score}%
        
#         Write an email that:
#         - Has a clear, professional subject line
#         - Addresses the contact person by name
#         - Introduces the consultant with key strengths
#         - Mentions the high match score and relevant experience
#         - Includes standard terms of offer section (with placeholders)
#         - Lists attachments (motivation, cover letter)
#         - Ends with professional closing and contact information
#         - Maintains business-appropriate tone
#         - Is concise but informative (200-300 words)
        
#         Use "Wanita Bajnath" as the sender name.
#         """

#         try:
#             content = self._call_openai(
#                 prompt,
#                 "You are an expert at writing professional business emails for staffing agencies."
#             )
#             return content
#         except RateLimitError:
#             return "Rate limit exceeded. Please try again later."
#         except Exception as e:
#             return f"Error generating email: {str(e)}"
        
# # Initialize analyzer
# analyzer = CVAnalyzer()

# @app.route('/api/analyze', methods=['POST'])
# def analyze_cv():
#     """Analyze CV against assignment requirements"""
#     try:
#         cv_file = request.files.get('cv_file')
#         assignment_file = request.files.get('assignment_file')
#         assignment_data = json.loads(request.form.get('assignment_data', '{}'))
#         consultant_data = json.loads(request.form.get('consultant_data', '{}'))
        
#         if not cv_file:
#             return jsonify({'error': 'CV file is required'}), 400
        
#         cv_content = cv_file.read()
#         cv_text = analyzer.extract_text_from_file(cv_content, cv_file.filename)
        
#         assignment_text = assignment_data.get('description', '')
#         if assignment_file:
#             assignment_content = assignment_file.read()
#             assignment_file_text = analyzer.extract_text_from_file(assignment_content, assignment_file.filename)
#             assignment_text = f"{assignment_text}\n\n{assignment_file_text}"
        
#         analysis_result = analyzer.analyze_cv_assignment_match(cv_text, assignment_text)
        
#         return jsonify({
#             'success': True,
#             'analysis': analysis_result
#         })
    
#     except Exception as e:
#         logging.error(f"API /api/analyze error: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/generate-motivations', methods=['POST'])
# def generate_motivations():
#     """Generate motivations for requirements"""
#     try:
#         data = request.json
#         cv_text = data.get('cv_text')
#         requirements = data.get('requirements', [])
#         consultant_name = data.get('consultant_name')
        
#         motivations = analyzer.generate_motivations(cv_text, requirements, consultant_name)
        
#         return jsonify({
#             'success': True,
#             'motivations': motivations
#         })
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/generate-cover-letter', methods=['POST'])
# def generate_cover_letter():
#     """Generate cover letter"""
#     try:
#         data = request.json
#         cv_text = data.get('cv_text')
#         assignment_info = data.get('assignment_info')
#         consultant_name = data.get('consultant_name')
#         analysis_result = data.get('analysis_result')
        
#         cover_letter = analyzer.generate_cover_letter(cv_text, assignment_info, consultant_name, analysis_result)
        
#         return jsonify({
#             'success': True,
#             'cover_letter': cover_letter
#         })
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/generate-email', methods=['POST'])
# def generate_email():
#     """Generate introduction email"""
#     try:
#         data = request.json
#         consultant_info = data.get('consultant_info')
#         assignment_info = data.get('assignment_info')
#         analysis_result = data.get('analysis_result')
        
#         email = analyzer.generate_introduction_email(consultant_info, assignment_info, analysis_result)
        
#         return jsonify({
#             'success': True,
#             'email': email
#         })
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({'status': 'healthy', 'service': 'CV Analysis API'})

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)



# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from openai import OpenAI, RateLimitError
# import os
# from typing import Dict, List, Any
# import json
# import PyPDF2
# import docx
# from io import BytesIO
# import logging
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
# from dotenv import load_dotenv
# import hashlib

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)

# class CVAnalyzer:
#     def __init__(self):
#         api_key = os.getenv('OPENAI_API_KEY')
#         if not api_key:
#             raise ValueError("OPENAI_API_KEY not set in .env file")
#         self.client = OpenAI(api_key=api_key)
#         self.use_mock = os.getenv('USE_MOCK', 'False').lower() == 'true'

#     def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
#         """Extract text from uploaded file based on file type"""
#         try:
#             if filename.lower().endswith('.pdf'):
#                 return self._extract_from_pdf(file_content)
#             elif filename.lower().endswith(('.doc', '.docx')):
#                 return self._extract_from_docx(file_content)
#             elif filename.lower().endswith('.txt'):
#                 return file_content.decode('utf-8')
#             else:
#                 raise ValueError(f"Unsupported file type: {filename}")
#         except Exception as e:
#             raise Exception(f"Error extracting text from {filename}: {str(e)}")

#     def _extract_from_pdf(self, file_content: bytes) -> str:
#         """Extract text from PDF file"""
#         pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
#         text = ""
#         for page in pdf_reader.pages:
#             extracted = page.extract_text()
#             if extracted:
#                 text += extracted + "\n"
#         return text

#     def _extract_from_docx(self, file_content: bytes) -> str:
#         """Extract text from DOCX file"""
#         doc = docx.Document(BytesIO(file_content))
#         text = ""
#         for paragraph in doc.paragraphs:
#             text += paragraph.text + "\n"
#         return text

#     def _mock_analysis(self) -> Dict[str, Any]:
#         """Mock response for testing without API"""
#         return {
#             "overall_score": 85,
#             "requirements_score": 90,
#             "wishes_score": 80,
#             "requirements": [
#                 {
#                     "id": "req1",
#                     "type": "require",
#                     "title": "SQL Proficiency",
#                     "description": "Advanced SQL skills",
#                     "match": True,
#                     "percentage": 95,
#                     "explanation": "CV shows 5+ years of SQL experience in data analysis projects."
#                 }
#             ],
#             "wishes": [
#                 {
#                     "id": "wish1",
#                     "type": "wish",
#                     "title": "Power BI Experience",
#                     "description": "Familiarity with Power BI",
#                     "match": True,
#                     "percentage": 80,
#                     "explanation": "CV mentions dashboard creation with Power BI."
#                 }
#             ]
#         }

#     @retry(
#         stop=stop_after_attempt(5),
#         wait=wait_exponential(multiplier=2, min=4, max=60),
#         retry=retry_if_exception_type((RateLimitError, json.JSONDecodeError))
#     )
#     def _call_openai(self, prompt: str, system_content: str, temperature: float = 0.3) -> str:
#         """Internal API call with retry"""
#         try:
#             response = self.client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     {"role": "system", "content": system_content},
#                     {"role": "user", "content": prompt}
#                 ],
#                 temperature=temperature
#             )
#             content = response.choices[0].message.content.strip()
#             logging.debug(f"Raw OpenAI response: {content}")
#             return content
#         except RateLimitError as e:
#             logging.error(f"Rate limit exceeded: {str(e)}")
#             raise
#         except Exception as e:
#             logging.error(f"OpenAI API error: {str(e)}")
#             raise

#     def analyze_cv_assignment_match(self, cv_text: str, assignment_text: str) -> Dict[str, Any]:
#         """Analyze CV against assignment requirements using GPT-3.5-turbo"""
#         if self.use_mock:
#             logging.debug("Using mock analysis response")
#             return self._mock_analysis()

#         # Validate assignment_text
#         if not assignment_text or assignment_text.isspace():
#             logging.error("Assignment requirements are empty")
#             return {
#                 "overall_score": 0,
#                 "requirements_score": 0,
#                 "wishes_score": 0,
#                 "requirements": [],
#                 "wishes": [],
#                 "error": "Assignment requirements cannot be empty"
#             }

#         # Truncate inputs to reduce tokens
#         cv_text = cv_text[:1000]
#         assignment_text = assignment_text[:1000]

#         # Cache key based on inputs
#         cache_key = hashlib.md5((cv_text + assignment_text).encode()).hexdigest()
#         cache_file = f"cache/{cache_key}.json"
#         if os.path.exists(cache_file):
#             logging.debug(f"Returning cached result for key: {cache_key}")
#             with open(cache_file, 'r') as f:
#                 return json.load(f)

#         prompt = f"""
#         You are an expert HR consultant specializing in data professional recruitment.
#         Analyze the provided CV against the assignment requirements and return a response in **valid JSON format only**.
#         Do not include any text outside the JSON object, such as explanations or code fences.

#         ASSIGNMENT REQUIREMENTS:
#         {assignment_text}

#         CONSULTANT CV:
#         {cv_text}

#         Return a JSON object with the following structure:
#         {{
#             "overall_score": <number 0-100>,
#             "requirements_score": <number 0-100>,
#             "wishes_score": <number 0-100>,
#             "requirements": [
#                 {{
#                     "id": "<unique_id>",
#                     "type": "require",
#                     "title": "<requirement_title>",
#                     "description": "<requirement_description>",
#                     "match": <boolean>,
#                     "percentage": <number 0-100>,
#                     "explanation": "<detailed_explanation>"
#                 }}
#             ],
#             "wishes": [
#                 {{
#                     "id": "<unique_id>",
#                     "type": "wish",
#                     "title": "<wish_title>",
#                     "description": "<wish_description>",
#                     "match": <boolean>,
#                     "percentage": <number 0-100>,
#                     "explanation": "<detailed_explanation>"
#                 }}
#             ]
#         }}

#         Focus on:
#         - Technical skills matching (e.g., Azure, SQL, Power BI)
#         - Experience relevance
#         - Education requirements
#         - Soft skills and cultural fit
#         - Provide specific examples from the CV

#         If no requirements are provided, return an empty requirements and wishes list with scores of 0.
#         Ensure the response is a valid JSON object with no additional text or code fences.
#         """

#         try:
#             content = self._call_openai(
#                 prompt,
#                 "You are an expert HR consultant. Return only valid JSON with no additional text or code fences."
#             )
#             result = json.loads(content)

#             # Cache result
#             os.makedirs("cache", exist_ok=True)
#             with open(cache_file, 'w') as f:
#                 json.dump(result, f)
#             logging.debug(f"Cached result for key: {cache_key}")

#             return result
#         except json.JSONDecodeError as e:
#             logging.error(f"JSON parsing error: {e}, raw content: {content}")
#             return {
#                 "overall_score": 0,
#                 "requirements_score": 0,
#                 "wishes_score": 0,
#                 "requirements": [],
#                 "wishes": [],
#                 "error": f"Invalid JSON response from OpenAI: {str(e)}"
#             }
#         except RateLimitError as e:
#             logging.error(f"Rate limit error: {str(e)}")
#             return {
#                 "overall_score": 0,
#                 "requirements_score": 0,
#                 "wishes_score": 0,
#                 "requirements": [],
#                 "wishes": [],
#                 "error": "Rate limit exceeded. Please try again later or upgrade your OpenAI plan."
#             }
#         except Exception as e:
#             logging.error(f"API error: {str(e)}")
#             return {
#                 "overall_score": 0,
#                 "requirements_score": 0,
#                 "wishes_score": 0,
#                 "requirements": [],
#                 "wishes": [],
#                 "error": f"Error in CV analysis: {str(e)}"
#             }

#     def generate_motivations(self, cv_text: str, requirements: List[Dict], consultant_name: str) -> Dict[str, str]:
#         """Generate personalized motivations for each requirement"""
#         if self.use_mock:
#             return {req['id']: "Mock motivation for testing." for req in requirements}

#         motivations = {}
#         cv_text = cv_text[:1000]

#         for req in requirements:
#             prompt = f"""
#             Generate a personalized motivation for the following requirement based on the consultant's CV.
            
#             CONSULTANT: {consultant_name}
#             REQUIREMENT: {req['title']} - {req['description']}
#             MATCH PERCENTAGE: {req['percentage']}%
            
#             CV CONTENT:
#             {cv_text}
            
#             Write a 2-3 sentence motivation that:
#             - Specifically addresses this requirement
#             - Uses concrete examples from the CV
#             - Shows relevant experience and skills
#             - Maintains professional tone
            
#             If the match is low, acknowledge the gap but highlight transferable skills.
#             """

#             try:
#                 content = self._call_openai(
#                     prompt,
#                     "You are an expert at writing compelling, specific motivations for job requirements.",
#                     temperature=0.4
#                 )
#                 motivations[req['id']] = content
#             except RateLimitError:
#                 motivations[req['id']] = "Rate limit exceeded. Please try again later."
#             except Exception as e:
#                 motivations[req['id']] = f"Error generating motivation: {str(e)}"

#         return motivations

#     def generate_cover_letter(self, cv_text: str, assignment_info: Dict, consultant_name: str, analysis_result: Dict) -> str:
#         """Generate a personalized cover letter"""
#         if self.use_mock:
#             return "Mock cover letter for testing."

#         cv_text = cv_text[:1000]
#         prompt = f"""
#         Write a professional cover letter for the following consultant and assignment.
        
#         CONSULTANT: {consultant_name}
#         CLIENT: {assignment_info.get('client', 'the client')}
#         POSITION: {assignment_info.get('title', 'the position')}
#         OVERALL MATCH SCORE: {analysis_result.get('overall_score', 0)}%
        
#         CV CONTENT:
#         {cv_text}
        
#         ASSIGNMENT DESCRIPTION:
#         {assignment_info.get('description', '')[:1000]}
        
#         Write a compelling cover letter that:
#         - Opens with a strong, personalized introduction
#         - Highlights the most relevant experience and skills
#         - Addresses any potential concerns (like education gaps) proactively
#         - Shows enthusiasm for the specific role and company
#         - Maintains professional yet personal tone
#         - Ends with a clear call to action
#         - Is approximately 300-400 words
        
#         Use specific examples from the CV and make it feel authentic to the consultant's background.
#         """

#         try:
#             content = self._call_openai(
#                 prompt,
#                 "You are an expert at writing compelling, personalized cover letters for data professionals.",
#                 temperature=0.5
#             )
#             return content
#         except RateLimitError:
#             return "Rate limit exceeded. Please try again later."
#         except Exception as e:
#             return f"Error generating cover letter: {str(e)}"

#     def generate_introduction_email(self, consultant_info: Dict, assignment_info: Dict, analysis_result: Dict) -> str:
#         """Generate a professional introduction email"""
#         if self.use_mock:
#             return "Mock email for testing."

#         consultant_name = consultant_info.get('name', 'the consultant')
#         client_name = assignment_info.get('client', 'the client')
#         position_title = assignment_info.get('title', 'the position')
#         contact_person = consultant_info.get('contactPerson', 'Sir/Madam')
#         overall_score = analysis_result.get('overall_score', 0)

#         prompt = f"""
#         Write a professional introduction email from a staffing agency to a client.
        
#         CONSULTANT: {consultant_name}
#         CLIENT: {client_name}
#         POSITION: {position_title}
#         CONTACT PERSON: {contact_person}
#         MATCH SCORE: {overall_score}%
        
#         Write an email that:
#         - Has a clear, professional subject line
#         - Addresses the contact person by name
#         - Introduces the consultant with key strengths
#         - Mentions the high match score and relevant experience
#         - Includes standard terms of offer section (with placeholders)
#         - Lists attachments (motivation, cover letter)
#         - Ends with professional closing and contact information
#         - Maintains business-appropriate tone
#         - Is concise but informative (200-300 words)
        
#         Use "Wanita Bajnath" as the sender name.
#         """

#         try:
#             content = self._call_openai(
#                 prompt,
#                 "You are an expert at writing professional business emails for staffing agencies."
#             )
#             return content
#         except RateLimitError:
#             return "Rate limit exceeded. Please try again later."
#         except Exception as e:
#             return f"Error generating email: {str(e)}"

#     def customize_content(self, content_type: str, original_content: str, user_prompt: str, context: Dict = None) -> str:
#         """Customize content based on user prompt"""
#         if self.use_mock:
#             return f"Mock customized {content_type} content based on: {user_prompt}"

#         system_prompts = {
#             'motivation': "You are an expert at customizing motivations for job requirements. Take the original content and modify it based on the user's specific instructions while maintaining professionalism and relevance.",
#             'coverletter': "You are an expert at customizing cover letters. Take the original cover letter and modify it based on the user's specific instructions while maintaining professional tone and structure.",
#             'email': "You are an expert at customizing professional business emails. Take the original email and modify it based on the user's specific instructions while maintaining business etiquette and clarity."
#         }

#         context_info = ""
#         if context:
#             consultant_name = context.get('consultant', {}).get('name', 'the consultant')
#             assignment_info = context.get('assignment', {})
#             client_name = assignment_info.get('client', 'the client')
#             position_title = assignment_info.get('title', 'the position')
            
#             context_info = f"""
#             CONTEXT:
#             - Consultant: {consultant_name}
#             - Client: {client_name}
#             - Position: {position_title}
#             """

#         prompt = f"""
#         {context_info}
        
#         ORIGINAL CONTENT:
#         {original_content}
        
#         USER INSTRUCTIONS:
#         {user_prompt}
        
#         Please modify the original content according to the user's instructions. Maintain the same format and professional tone, but incorporate the requested changes. Return only the modified content without any explanations or additional text.
#         """

#         try:
#             content = self._call_openai(
#                 prompt,
#                 system_prompts.get(content_type, "You are an expert content editor."),
#                 temperature=0.4
#             )
#             return content
#         except RateLimitError:
#             return f"Rate limit exceeded. Please try again later."
#         except Exception as e:
#             return f"Error customizing content: {str(e)}"
        
# # Initialize analyzer
# analyzer = CVAnalyzer()

# @app.route('/api/analyze', methods=['POST'])
# def analyze_cv():
#     """Analyze CV against assignment requirements"""
#     try:
#         cv_file = request.files.get('cv_file')
#         assignment_file = request.files.get('assignment_file')
#         assignment_data = json.loads(request.form.get('assignment_data', '{}'))
#         consultant_data = json.loads(request.form.get('consultant_data', '{}'))
        
#         if not cv_file:
#             return jsonify({'error': 'CV file is required'}), 400
        
#         cv_content = cv_file.read()
#         cv_text = analyzer.extract_text_from_file(cv_content, cv_file.filename)
        
#         assignment_text = assignment_data.get('description', '')
#         if assignment_file:
#             assignment_content = assignment_file.read()
#             assignment_file_text = analyzer.extract_text_from_file(assignment_content, assignment_file.filename)
#             assignment_text = f"{assignment_text}\n\n{assignment_file_text}"
        
#         analysis_result = analyzer.analyze_cv_assignment_match(cv_text, assignment_text)
        
#         return jsonify({
#             'success': True,
#             'analysis': analysis_result,
#             'cv_text': cv_text  # Return CV text for later use
#         })
    
#     except Exception as e:
#         logging.error(f"API /api/analyze error: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/generate-motivations', methods=['POST'])
# def generate_motivations():
#     """Generate motivations for requirements"""
#     try:
#         data = request.json
#         cv_text = data.get('cv_text')
#         requirements = data.get('requirements', [])
#         consultant_name = data.get('consultant_name')
        
#         motivations = analyzer.generate_motivations(cv_text, requirements, consultant_name)
        
#         return jsonify({
#             'success': True,
#             'motivations': motivations
#         })
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/generate-cover-letter', methods=['POST'])
# def generate_cover_letter():
#     """Generate cover letter"""
#     try:
#         data = request.json
#         cv_text = data.get('cv_text')
#         assignment_info = data.get('assignment_info')
#         consultant_name = data.get('consultant_name')
#         analysis_result = data.get('analysis_result')
        
#         cover_letter = analyzer.generate_cover_letter(cv_text, assignment_info, consultant_name, analysis_result)
        
#         return jsonify({
#             'success': True,
#             'cover_letter': cover_letter
#         })
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/generate-email', methods=['POST'])
# def generate_email():
#     """Generate introduction email"""
#     try:
#         data = request.json
#         consultant_info = data.get('consultant_info')
#         assignment_info = data.get('assignment_info')
#         analysis_result = data.get('analysis_result')
        
#         email = analyzer.generate_introduction_email(consultant_info, assignment_info, analysis_result)
        
#         return jsonify({
#             'success': True,
#             'email': email
#         })
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/customize-content', methods=['POST'])
# def customize_content():
#     """Customize content with AI based on user prompt"""
#     try:
#         data = request.json
#         content_type = data.get('type')
#         original_content = data.get('content')
#         user_prompt = data.get('prompt')
#         context = data.get('context', {})
        
#         if not all([content_type, original_content, user_prompt]):
#             return jsonify({'error': 'Missing required fields'}), 400
        
#         customized_content = analyzer.customize_content(content_type, original_content, user_prompt, context)
        
#         return jsonify({
#             'success': True,
#             'customized_content': customized_content
#         })
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({'status': 'healthy', 'service': 'CV Analysis API'})

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)













# # app.py
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from openai import OpenAI, RateLimitError
# import os
# from typing import Dict, List, Any
# import json
# import pdfplumber
# # REMOVED the problematic import to prevent ModuleNotFoundError
# import docx
# from io import BytesIO
# import logging
# from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
# from dotenv import load_dotenv
# import hashlib
# from requests.exceptions import RequestException

# # Load environment variables from a .env file
# load_dotenv()

# # --- Configuration ---
# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo')
# USE_MOCK = os.getenv('USE_MOCK', 'False').lower() == 'true'
# CACHE_DIR = os.getenv('CACHE_DIR', 'cache')
# MAX_INPUT_CHARS = int(os.getenv('MAX_INPUT_CHARS', '50000'))

# # --- Flask App Initialization ---
# app = Flask(__name__)
# CORS(app)

# # --- Logging Configuration ---
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# # --- Core CV Analysis Logic ---
# class CVAnalyzer:
#     def __init__(self):
#         if not OPENAI_API_KEY and not USE_MOCK:
#             raise ValueError("OPENAI_API_KEY not set in .env file and mock mode is disabled.")
#         self.client = OpenAI(api_key=OPENAI_API_KEY)
#         self.use_mock = USE_MOCK
#         logger.info(f"CVAnalyzer initialized with model: {OPENAI_MODEL}, Mock Mode: {self.use_mock}")

#     def _truncate_text(self, text: str) -> str:
#         """Truncates text if it exceeds the maximum character limit."""
#         if len(text) > MAX_INPUT_CHARS:
#             logger.warning(f"Input text truncated to {MAX_INPUT_CHARS} characters.")
#             return text[:MAX_INPUT_CHARS]
#         return text

#     def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
#         """Extracts text from PDF, DOCX, or TXT files."""
#         logger.debug(f"Extracting text from {filename}")
#         file_extension = os.path.splitext(filename)[1].lower()
#         try:
#             if file_extension == '.pdf':
#                 text = self._extract_from_pdf(file_content)
#             elif file_extension in ['.doc', '.docx']:
#                 text = self._extract_from_docx(file_content)
#             elif file_extension == '.txt':
#                 text = file_content.decode('utf-8')
#             else:
#                 raise ValueError(f"Unsupported file type: {file_extension}. Please use PDF, DOCX, or TXT.")
            
#             if not text or text.isspace():
#                 raise ValueError(f"No text could be extracted from '{filename}'. The file may be empty or image-based.")
#             return text
#         except Exception as e:
#             logger.error(f"Error extracting text from {filename}: {e}", exc_info=True)
#             raise Exception(f"Could not read file '{filename}'. It may be corrupted, password-protected, or in an unsupported format.") from e

#     def _extract_from_pdf(self, file_content: bytes) -> str:
#         """
#         Extracts text from a PDF file using pdfplumber.
#         Handles encrypted PDFs by checking the exception message for "Password".
#         """
#         text = ""
#         try:
#             with pdfplumber.open(BytesIO(file_content)) as pdf:
#                 # This will raise an exception for encrypted files when we access pages.
#                 for page in pdf.pages:
#                     extracted = page.extract_text()
#                     if extracted:
#                         text += extracted + "\n"
#             return text
#         except Exception as e:
#             # CORRECTED & MORE ROBUST: Check the exception string for the keyword "Password".
#             if "Password" in str(e):
#                 logger.error("Failed to process PDF: The file is password-protected.")
#                 raise ValueError("The provided PDF is password-protected and cannot be read.")
#             else:
#                 logger.error(f"An unexpected error occurred during PDF processing: {e}", exc_info=True)
#                 raise Exception("Failed to process PDF file due to an unexpected error.") from e

#     def _extract_from_docx(self, file_content: bytes) -> str:
#         """Extracts text from a DOCX file."""
#         doc = docx.Document(BytesIO(file_content))
#         return "\n".join(para.text for para in doc.paragraphs)

#     @retry(
#         stop=stop_after_attempt(3),
#         wait=wait_exponential(multiplier=2, min=4, max=30),
#         retry=retry_if_exception_type((RateLimitError, json.JSONDecodeError, RequestException)),
#         reraise=True
#     )
#     def _call_openai(self, prompt: str, system_content: str, temperature: float = 0.2, use_json_mode: bool = False) -> str:
#         """Internal method to call the OpenAI API with a robust retry mechanism."""
#         logger.debug(f"Calling OpenAI API with model {OPENAI_MODEL}. Temperature: {temperature}.")
#         params = {
#             "model": OPENAI_MODEL,
#             "messages": [
#                 {"role": "system", "content": system_content},
#                 {"role": "user", "content": prompt}
#             ],
#             "temperature": temperature,
#         }
#         if use_json_mode:
#             params["response_format"] = {"type": "json_object"}
#         response = self.client.chat.completions.create(**params)
#         return response.choices[0].message.content.strip()

#     def analyze_cv_assignment_match(self, cv_text: str, assignment_text: str) -> Dict[str, Any]:
#         """Analyzes a CV against assignment requirements."""
#         if self.use_mock: return self._mock_analysis()

#         cv_text = self._truncate_text(cv_text)
#         assignment_text = self._truncate_text(assignment_text)

#         cache_key = hashlib.md5((cv_text + assignment_text).encode()).hexdigest()
#         os.makedirs(CACHE_DIR, exist_ok=True)
#         cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
#         if os.path.exists(cache_file):
#             logger.info(f"Returning cached result for {cache_key}")
#             with open(cache_file, 'r') as f: return json.load(f)

#         prompt = f"""
#         Analyze the provided CV against the assignment requirements.

#         ASSIGNMENT REQUIREMENTS:
#         {assignment_text}

#         CONSULTANT CV:
#         {cv_text}

#         Your task is to act as an expert HR analyst. Follow these steps:
#         1. Identify all mandatory 'requirements' and optional 'wishes' from the assignment.
#         2. For each one, meticulously check the CV for evidence of a match.
#         3. Score the match quality from 0-100. Direct experience = 90-100. Related skills = 50-70. No evidence = 0.
#         4. Provide a concise, evidence-based explanation for each score.
#         5. Calculate `requirements_score`, `wishes_score`, and a weighted `overall_score` (70% requirements, 30% wishes).
#         6. Return a single, valid JSON object as your final output.

#         JSON Structure:
#         {{
#             "overall_score": <number>, "requirements_score": <number>, "wishes_score": <number>,
#             "requirements": [{{ "id": "req_1", "type": "require", "title": "<title>", "description": "<desc>", "match": <boolean>, "percentage": <number>, "explanation": "<evidence>" }}],
#             "wishes": [{{ "id": "wish_1", "type": "wish", "title": "<title>", "description": "<desc>", "match": <boolean>, "percentage": <number>, "explanation": "<evidence>" }}]
#         }}
#         """
#         system_content = "You are a world-class HR analyst. You must return your analysis ONLY in the specified JSON format."
#         content = self._call_openai(prompt, system_content, use_json_mode=True)
#         result = json.loads(content)
#         with open(cache_file, 'w') as f: json.dump(result, f)
#         logger.info(f"Cached new result for key: {cache_key}")
#         return result

#     def generate_motivations(self, cv_text: str, requirements: List[Dict], consultant_name: str) -> Dict[str, str]:
#         """Generates personalized motivations for each requirement."""
#         if self.use_mock: return {req['id']: "Mock motivation for testing." for req in requirements}
#         motivations = {}
#         cv_text = self._truncate_text(cv_text)
#         system_content = "You are an expert at writing compelling, specific motivations for job requirements. Your tone is professional and confident."
#         for req in requirements:
#             prompt = f"""
#             Generate a personalized, 2-3 sentence motivation for the following requirement based on the consultant's CV.
#             CONSULTANT: {consultant_name}
#             REQUIREMENT: {req['title']} - {req['description']}
#             CV SNIPPETS:
#             {cv_text}
#             Instructions:
#             - Write a motivation that directly addresses the requirement.
#             - Weave in specific examples, projects, or skills from the CV.
#             - If the match is low, focus on transferable skills and a strong desire to learn.
#             - Return only the motivation text, without any titles or extra formatting.
#             """
#             try:
#                 content = self._call_openai(prompt, system_content, temperature=0.4)
#                 motivations[req['id']] = content
#             except Exception as e:
#                 logger.error(f"Error generating motivation for requirement {req['id']}: {e}")
#                 motivations[req['id']] = f"Error generating motivation: {str(e)}"
#         return motivations

#     def generate_cover_letter(self, cv_text: str, assignment_info: Dict, consultant_name: str, analysis_result: Dict) -> str:
#         """Generates a personalized cover letter."""
#         if self.use_mock: return "Mock cover letter for testing."
#         cv_text = self._truncate_text(cv_text)
#         assignment_description = self._truncate_text(assignment_info.get('description', ''))
#         prompt = f"""
#         Write a professional and compelling cover letter (300-400 words).
#         CONSULTANT: {consultant_name}
#         CLIENT: {assignment_info.get('client', 'the client')}
#         POSITION: {assignment_info.get('title', 'the position')}
#         CONSULTANT CV (SUMMARY):
#         {cv_text}
#         ASSIGNMENT DESCRIPTION:
#         {assignment_description}
#         Instructions:
#         1. Create a strong, personalized opening.
#         2. Highlight the top 2-3 most relevant skills and experiences from the CV that match the assignment. Use specific examples.
#         3. Show genuine enthusiasm for the role and the client's company.
#         4. Maintain a professional, confident, yet personable tone.
#         5. Conclude with a clear call to action.
#         """
#         system_content = "You are an expert career coach specializing in writing persuasive cover letters for tech professionals."
#         return self._call_openai(prompt, system_content, temperature=0.5)

#     def generate_introduction_email(self, consultant_info: Dict, assignment_info: Dict, analysis_result: Dict) -> str:
#         """Generates a professional introduction email from an agency to a client."""
#         if self.use_mock: return "Mock email for testing."
#         prompt = f"""
#         Write a professional introduction email from a staffing agency to a client.
#         CONSULTANT: {consultant_info.get('name', 'the consultant')}
#         CLIENT: {assignment_info.get('client', 'the client')}
#         POSITION: {assignment_info.get('title', 'the position')}
#         CONTACT PERSON AT CLIENT: {consultant_info.get('contactPerson', 'Hiring Manager')}
#         MATCH SCORE: {analysis_result.get('overall_score', 0)}%
#         KEY REQUIREMENTS MET: {', '.join([r['title'] for r in analysis_result.get('requirements', []) if r.get('match')])}
#         Instructions:
#         - Write a concise and professional email (200-300 words).
#         - Use a clear subject line like: "Introduction: [Consultant Name] for the [Position Title] Role".
#         - Briefly introduce the consultant, highlighting their key strengths and the high match score.
#         - Mention attached documents (CV, motivation).
#         - Use "Wanita Bajnath" as the sender's name.
#         """
#         system_content = "You are an expert business communicator for a recruitment agency. Your tone is professional, efficient, and client-focused."
#         return self._call_openai(prompt, system_content, temperature=0.3)
    
#     def customize_content(self, content_type: str, original_content: str, user_prompt: str, context: Dict = None) -> str:
#         """Customizes generated content based on user feedback."""
#         if self.use_mock: return f"Mock customized content for {content_type}."
#         system_prompts = {
#             'motivation': "You are an expert editor specializing in job application motivations. Refine the provided text based on the user's instructions, keeping it professional and concise.",
#             'coverletter': "You are an expert editor for professional cover letters. Rewrite the original letter to incorporate the user's feedback, enhancing its persuasive impact.",
#             'email': "You are an expert business communication editor. Modify the email according to the user's request, ensuring it remains professional and clear."
#         }
#         prompt = f"""
#         You are tasked with editing the following text based on user instructions.
#         ORIGINAL CONTENT:
#         ---
#         {original_content}
#         ---
#         USER INSTRUCTIONS:
#         ---
#         {user_prompt}
#         ---
#         Please return only the fully rewritten, modified content. Do not add any commentary.
#         """
#         system_content = system_prompts.get(content_type, "You are a helpful editing assistant.")
#         return self._call_openai(prompt, system_content, temperature=0.4)

# # --- Initialization ---
# try:
#     analyzer = CVAnalyzer()
# except ValueError as e:
#     logger.critical(f"CRITICAL: CVAnalyzer failed to initialize: {e}", exc_info=True)
#     analyzer = None

# # --- API Endpoints ---
# def get_request_data():
#     """Helper to parse multipart form data."""
#     if 'cv_file' not in request.files:
#         raise ValueError('CV file is required.')
#     return {
#         "cv_file": request.files['cv_file'],
#         "assignment_file": request.files.get('assignment_file'),
#         "assignment_data": json.loads(request.form.get('assignment_data', '{}')),
#         "consultant_data": json.loads(request.form.get('consultant_data', '{}'))
#     }

# @app.route('/api/analyze', methods=['POST'])
# def analyze_cv_endpoint():
#     form_data = get_request_data()
#     cv_text = analyzer.extract_text_from_file(form_data['cv_file'].read(), form_data['cv_file'].filename)
#     assignment_text = form_data['assignment_data'].get('description', '')
#     if form_data['assignment_file']:
#         assignment_file_text = analyzer.extract_text_from_file(form_data['assignment_file'].read(), form_data['assignment_file'].filename)
#         assignment_text += f"\n\n{assignment_file_text}"
#     analysis_result = analyzer.analyze_cv_assignment_match(cv_text, assignment_text)
#     return jsonify({'success': True, 'analysis': analysis_result, 'cv_text': cv_text})

# @app.route('/api/generate-motivations', methods=['POST'])
# def generate_motivations_endpoint():
#     data = request.json
#     motivations = analyzer.generate_motivations(data['cv_text'], data['requirements'], data['consultant_name'])
#     return jsonify({'success': True, 'motivations': motivations})

# @app.route('/api/generate-cover-letter', methods=['POST'])
# def generate_cover_letter_endpoint():
#     data = request.json
#     cover_letter = analyzer.generate_cover_letter(data['cv_text'], data['assignment_info'], data['consultant_name'], data['analysis_result'])
#     return jsonify({'success': True, 'cover_letter': cover_letter})

# @app.route('/api/generate-email', methods=['POST'])
# def generate_email_endpoint():
#     data = request.json
#     email = analyzer.generate_introduction_email(data['consultant_info'], data['assignment_info'], data['analysis_result'])
#     return jsonify({'success': True, 'email': email})

# @app.route('/api/customize-content', methods=['POST'])
# def customize_content_endpoint():
#     data = request.json
#     if not all(k in data for k in ['type', 'content', 'prompt']):
#         raise ValueError('Missing required fields: type, content, prompt.')
#     customized_content = analyzer.customize_content(data['type'], data['content'], data['prompt'], data.get('context', {}))
#     return jsonify({'success': True, 'customized_content': customized_content})

# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({'status': 'healthy', 'service': 'CV Analysis API'})

# # --- Centralized Error Handler ---
# @app.errorhandler(Exception)
# def handle_exception(e: Exception):
#     logger.error(f"An unhandled exception occurred: {e}", exc_info=True)
#     if isinstance(e, ValueError): status_code = 400
#     elif isinstance(e, RateLimitError): status_code = 429
#     else: status_code = 500
#     return jsonify({"success": False, "error": "An internal server error occurred.", "message": str(e)}), status_code

# # --- App Runner ---
# if __name__ == '__main__':
#     if not analyzer:
#         print("FATAL: Application cannot start because CVAnalyzer failed to initialize. Check .env file and logs.")
#     else:
#         app.run(debug=True, host='0.0.0.0', port=5000)








import os
import re
import json
import hashlib
import logging
import time
import PyPDF2
from io import BytesIO
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI, RateLimitError
from typing import Dict, List, Any
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential, wait_random, retry_if_exception_type
from dotenv import load_dotenv
import pdfplumber
import docx

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4-turbo')
USE_MOCK = os.getenv('USE_MOCK', 'False').lower() == 'true'
CACHE_DIR = os.getenv('CACHE_DIR', 'cache')
MAX_INPUT_CHARS = int(os.getenv('MAX_INPUT_CHARS', '50000'))

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- Enhanced File Validation ---
def validate_file_upload(file, valid_extensions=('.pdf', '.docx', '.doc', '.txt'), max_size_mb=10):
    """Enhanced file validation with content checking."""
    file.seek(0, 2)  # End
    size = file.tell()
    file.seek(0)
    
    if size > max_size_mb * 1024 * 1024:
        raise ValueError(f"File too large. Maximum size is {max_size_mb}MB.")
    
    if size == 0:
        raise ValueError("File is empty.")
    
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in valid_extensions:
        raise ValueError(f"Unsupported file extension: {ext}. Supported: {', '.join(valid_extensions)}")
    
    # Read file header for validation
    header = file.read(min(512, size))  # Read first 512 bytes or entire file if smaller
    file.seek(0)
    
    if ext == '.pdf':
        if not header.startswith(b'%PDF-'):
            raise ValueError("Invalid PDF file format - missing PDF header.")
    elif ext == '.docx':
        if not header.startswith(b'PK\x03\x04'):
            raise ValueError("Invalid DOCX file format.")
    elif ext == '.doc':
        if not header.startswith(b'\xd0\xcf\x11\xe0'):
            raise ValueError("Invalid DOC file format.")

# --- CV Analyzer Class ---
class CVAnalyzer:
    def __init__(self):
        if not OPENAI_API_KEY and not USE_MOCK:
            raise ValueError("OPENAI_API_KEY not set and mock mode disabled.")
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        self.use_mock = USE_MOCK
        logger.info(f"CVAnalyzer initialized with model {OPENAI_MODEL}, Mock: {self.use_mock}")

    def _mock_analysis(self):
        """Mock analysis for testing purposes."""
        return {
            "overall_score": 85,
            "requirements_score": 80,
            "wishes_score": 90,
            "requirements": [
                {
                    "id": "req_1",
                    "type": "require",
                    "title": "Python Development",
                    "description": "Experience with Python programming",
                    "match": True,
                    "percentage": 85,
                    "explanation": "Strong Python experience evident in CV"
                }
            ],
            "wishes": [
                {
                    "id": "wish_1",
                    "type": "wish",
                    "title": "Machine Learning",
                    "description": "Knowledge of ML frameworks",
                    "match": True,
                    "percentage": 75,
                    "explanation": "Some ML experience mentioned"
                }
            ]
        }

    def _sanitize_and_truncate_text(self, text: str) -> str:
        """Sanitize and truncate text input."""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Keep only safe characters
        text = re.sub(r'[^\w\s\-.,!?@#&()"\':;/\\]', '', text)
        
        if len(text) > MAX_INPUT_CHARS:
            logger.warning(f"Input text truncated to {MAX_INPUT_CHARS} characters.")
            return text[:MAX_INPUT_CHARS]
        return text

    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """Extract text from various file formats."""
        logger.debug(f"Extracting text from {filename}")
        ext = os.path.splitext(filename)[1].lower()
        
        try:
            if ext == '.pdf':
                return self._extract_from_pdf(file_content)
            elif ext in ['.doc', '.docx']:
                return self._extract_from_docx(file_content)
            elif ext == '.txt':
                return file_content.decode('utf-8', errors='ignore')
            else:
                raise ValueError(f"Unsupported file type: {ext}")
        except Exception as e:
            logger.error(f"Error extracting text from {filename}: {e}", exc_info=True)
            raise Exception(f"Could not read '{filename}'. {str(e)}") from e

    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Enhanced PDF extraction with multiple fallback methods."""
        text = ""
        
        # Method 1: Try pdfplumber first (with corrected encryption check)
        try:
            with pdfplumber.open(BytesIO(file_content)) as pdf:
                # Corrected encryption check for newer pdfplumber versions
                try:
                    # Try to access first page to check if encrypted
                    if pdf.pages and len(pdf.pages) > 0:
                        # Test access to first page
                        test_page = pdf.pages[0]
                        test_page.extract_text()  # This will fail if encrypted
                    else:
                        raise ValueError("PDF has no readable pages.")
                except Exception as encrypt_check:
                    if any(x in str(encrypt_check).lower() for x in ['password', 'encrypted', 'secured', 'decrypt']):
                        raise ValueError("The PDF is password-protected and cannot be read.")
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf.pages):
                    try:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
                    except Exception as page_error:
                        logger.warning(f"Failed to extract text from page {page_num + 1}: {page_error}")
                        continue
                
                if text.strip():
                    return text
                        
        except Exception as e:
            logger.debug(f"pdfplumber failed: {e}")  # Changed to debug to reduce log noise
            if any(x in str(e).lower() for x in ['password', 'encrypted', 'secured', 'decrypt']):
                raise ValueError("The PDF is password-protected and cannot be read.")
        
        # Method 2: Try PyPDF2 as fallback
        try:
            file_content_copy = BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(file_content_copy)
            
            # Check encryption with PyPDF2
            if pdf_reader.is_encrypted:
                raise ValueError("The PDF is password-protected and cannot be read.")
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
                except Exception as page_error:
                    logger.warning(f"PyPDF2 page {page_num + 1} extraction failed: {page_error}")
                    continue
            
            if text.strip():
                logger.info("PDF extracted using PyPDF2 fallback")
                return text
                
        except Exception as e:
            logger.warning(f"PyPDF2 fallback failed: {e}")
            if any(x in str(e).lower() for x in ['password', 'encrypted', 'secured', 'decrypt']):
                raise ValueError("The PDF is password-protected and cannot be read.")
        
        # If all methods failed but no text was extracted
        if not text.strip():
            raise ValueError("Could not extract any text from the PDF. The file may be image-based, corrupted, or in an unsupported format.")
        
        return text

    def _extract_from_docx(self, file_content: bytes) -> str:
        """Enhanced DOCX extraction with better error handling."""
        try:
            doc = docx.Document(BytesIO(file_content))
            
            # Extract text from paragraphs
            paragraphs = []
            for para in doc.paragraphs:
                if para.text.strip():
                    paragraphs.append(para.text)
            
            # Extract text from tables
            table_text = []
            for table in doc.tables:
                for row in table.rows:
                    row_text = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_text.append(cell.text.strip())
                    if row_text:
                        table_text.append(" | ".join(row_text))
            
            # Combine all text
            all_text = paragraphs + table_text
            
            if not all_text:
                raise ValueError("DOCX file appears empty or contains no readable text.")
            
            return "\n".join(all_text)
            
        except Exception as e:
            if "corrupted" in str(e).lower() or "invalid" in str(e).lower():
                raise ValueError("The DOCX file appears to be corrupted and cannot be processed.")
            raise Exception("Failed to process DOCX file.") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=30) + wait_random(0, 3),
        retry=retry_if_exception_type((RateLimitError, json.JSONDecodeError, RequestException)),
        reraise=True
    )
    def _call_openai(self, prompt: str, system_content: str, temperature: float = 0.2, use_json_mode: bool = False) -> str:
        """Call OpenAI API with retry logic."""
        if self.use_mock:
            return '{"mock": "response for testing"}'
            
        logger.debug(f"Calling OpenAI {OPENAI_MODEL}")
        params = {
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
        }
        if use_json_mode:
            params["response_format"] = {"type": "json_object"}
        
        response = self.client.chat.completions.create(**params)
        return response.choices[0].message.content.strip()

    def _validate_analysis_result(self, result: Dict) -> Dict:
        """Validate the structure and content of analysis results."""
        required_fields = ['overall_score', 'requirements_score', 'wishes_score', 'requirements', 'wishes']
        
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field: {field} in analysis result.")
        
        # Validate score ranges
        for key in ['overall_score', 'requirements_score', 'wishes_score']:
            val = result[key]
            if not isinstance(val, (float, int)) or not 0 <= val <= 100:
                raise ValueError(f"Invalid score value for {key}: {val}")
        
        return result

    def _get_cache_key(self, cv_text: str, assignment_text: str) -> str:
        """Generate cache key for CV-assignment pair."""
        return hashlib.sha256((cv_text + assignment_text).encode()).hexdigest()

    def _is_cache_valid(self, cache_file, ttl_hours=24) -> bool:
        """Check if cache file is valid and not expired."""
        if not os.path.exists(cache_file):
            return False
        
        file_age = time.time() - os.path.getmtime(cache_file)
        return file_age < (ttl_hours * 3600)

    def analyze_cv_assignment_match(self, cv_text: str, assignment_text: str) -> Dict[str, Any]:
        """Analyze CV against assignment requirements."""
        if self.use_mock:
            return self._mock_analysis()
        
        cv_text = self._sanitize_and_truncate_text(cv_text)
        assignment_text = self._sanitize_and_truncate_text(assignment_text)
        
        # Check cache
        cache_key = self._get_cache_key(cv_text, assignment_text)
        os.makedirs(CACHE_DIR, exist_ok=True)
        cache_file = os.path.join(CACHE_DIR, f"{cache_key}.json")
        
        if self._is_cache_valid(cache_file):
            logger.info(f"Returning cached result {cache_key}")
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        prompt = f"""
        Analyze the provided CV against assignment requirements.

        ASSIGNMENT REQUIREMENTS:
        {assignment_text}

        CONSULTANT CV:
        {cv_text}

        Act as an expert HR analyst. Follow these steps:
        1. Identify all mandatory 'requirements' and optional 'wishes' from the assignment.
        2. For each requirement/wish, meticulously check the CV for evidence of a match.
        3. Score the match quality from 0-100. Direct experience = 90-100; related skills = 50-70; no evidence = 0.
        4. Provide concise, evidence-based explanation for each score.
        5. Calculate requirements_score, wishes_score, and weighted overall_score (70% requirements, 30% wishes).
        6. Return a single, valid JSON object as your final output.

        JSON format:
        {{
            "overall_score": <number>, 
            "requirements_score": <number>, 
            "wishes_score": <number>,
            "requirements": [{{
                "id": "req_1", 
                "type": "require", 
                "title": "<title>", 
                "description": "<desc>", 
                "match": <boolean>, 
                "percentage": <number>, 
                "explanation": "<evidence>"
            }}],
            "wishes": [{{
                "id": "wish_1", 
                "type": "wish", 
                "title": "<title>", 
                "description": "<desc>", 
                "match": <boolean>, 
                "percentage": <number>, 
                "explanation": "<evidence>"
            }}]
        }}
        """
        
        system_content = "You are a world-class HR analyst. You must return your analysis ONLY in the specified JSON format."
        content = self._call_openai(prompt, system_content, use_json_mode=True)
        
        try:
            result = json.loads(content)
            result = self._validate_analysis_result(result)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed: {e}")
            raise ValueError("Failed to parse AI response as valid JSON.")
        
        # Cache the result
        with open(cache_file, 'w') as f:
            json.dump(result, f)
        logger.info(f"Cached new result with key: {cache_key}")
        
        return result

    def generate_motivations(self, cv_text: str, requirements: List[Dict], consultant_name: str) -> Dict[str, str]:
        """Generate personalized motivations for each requirement."""
        if self.use_mock:
            return {req['id']: "Mock motivation for testing." for req in requirements}
        
        motivations = {}
        cv_text = self._sanitize_and_truncate_text(cv_text)
        system_content = "You are an expert at writing compelling, specific motivations for job requirements."
        
        for req in requirements:
            prompt = f"""
            Generate a personalized, 2-3 sentence motivation for the following requirement based on the consultant's CV.
            
            CONSULTANT: {consultant_name}
            REQUIREMENT: {req['title']} - {req['description']}
            
            CV CONTENT:
            {cv_text}
            
            Instructions:
            - Write a motivation that directly addresses the requirement.
            - Use specific examples, projects, or skills from the CV.
            - If the match is low, focus on transferable skills and strong desire to learn.
            - Return only the motivation text, without any titles or extra formatting.
            """
            
            try:
                content = self._call_openai(prompt, system_content, temperature=0.4)
                motivations[req['id']] = content
            except Exception as e:
                logger.error(f"Error generating motivation for requirement {req['id']}: {e}")
                motivations[req['id']] = f"Error generating motivation: {str(e)}"
        
        return motivations

    def generate_cover_letter(self, cv_text: str, assignment_info: Dict, consultant_name: str, analysis_result: Dict) -> str:
        """Generate a personalized cover letter."""
        if self.use_mock:
            return "Mock cover letter for testing."
        
        cv_text = self._sanitize_and_truncate_text(cv_text)
        assignment_description = self._sanitize_and_truncate_text(assignment_info.get('description', ''))
        
        prompt = f"""
        Write a professional and compelling cover letter (300-400 words).
        
        CONSULTANT: {consultant_name}
        CLIENT: {assignment_info.get('client', 'the client')}
        POSITION: {assignment_info.get('title', 'the position')}
        
        CONSULTANT CV SUMMARY:
        {cv_text}
        
        ASSIGNMENT DESCRIPTION:
        {assignment_description}
        
        Instructions:
        1. Create a strong, personalized opening.
        2. Highlight the top 2-3 most relevant skills and experiences from the CV that match the assignment. Use specific examples.
        3. Show genuine enthusiasm for the role and the client's company.
        4. Maintain a professional, confident, yet personable tone.
        5. Conclude with a clear call to action.
        """
        
        system_content = "You are an expert career coach specializing in writing persuasive cover letters for tech professionals."
        return self._call_openai(prompt, system_content, temperature=0.5)

    def generate_introduction_email(self, consultant_info: Dict, assignment_info: Dict, analysis_result: Dict) -> str:
        """Generate a professional introduction email."""
        if self.use_mock:
            return "Mock email for testing."
        
        prompt = f"""
        Write a professional introduction email from a staffing agency to a client.
        
        CONSULTANT: {consultant_info.get('name', 'the consultant')}
        CLIENT: {assignment_info.get('client', 'the client')}
        POSITION: {assignment_info.get('title', 'the position')}
        CONTACT PERSON AT CLIENT: {consultant_info.get('contactPerson', 'Hiring Manager')}
        MATCH SCORE: {analysis_result.get('overall_score', 0)}%
        KEY REQUIREMENTS MET: {', '.join([r['title'] for r in analysis_result.get('requirements', []) if r.get('match')])}
        
        Instructions:
        - Write a concise and professional email (200-300 words).
        - Use a clear subject line like: "Introduction: [Consultant Name] for the [Position Title] Role".
        - Briefly introduce the consultant, highlighting their key strengths and the high match score.
        - Mention attached documents (CV, motivation).
        - Use "Wanita Bajnath" as the sender's name.
        """
        
        system_content = "You are an expert business communicator for a recruitment agency. Your tone is professional, efficient, and client-focused."
        return self._call_openai(prompt, system_content, temperature=0.3)

    def customize_content(self, content_type: str, original_content: str, user_prompt: str, context: Dict = None) -> str:
        """Customize generated content based on user feedback."""
        if self.use_mock:
            return f"Mock customized content for {content_type}."
        
        system_prompts = {
            'motivation': "You are an expert editor specializing in job application motivations. Refine the provided text based on the user's instructions, keeping it professional and concise.",
            'coverletter': "You are an expert editor for professional cover letters. Rewrite the original letter to incorporate the user's feedback, enhancing its persuasive impact.",
            'email': "You are an expert business communication editor. Modify the email according to the user's request, ensuring it remains professional and clear."
        }
        
        prompt = f"""
        You are tasked with editing the following text based on user instructions.
        
        ORIGINAL CONTENT:
        ---
        {original_content}
        ---
        
        USER INSTRUCTIONS:
        ---
        {user_prompt}
        ---
        
        Please return only the fully rewritten, modified content. Do not add any commentary.
        """
        
        system_content = system_prompts.get(content_type, "You are a helpful editing assistant.")
        return self._call_openai(prompt, system_content, temperature=0.4)

# --- Initialize Analyzer ---
try:
    analyzer = CVAnalyzer()
except ValueError as e:
    logger.critical(f"CRITICAL: CVAnalyzer failed to initialize: {e}", exc_info=True)
    analyzer = None

# --- Helper Functions ---
def get_request_data():
    """Parse multipart form data from request."""
    if 'cv_file' not in request.files:
        raise ValueError('CV file is required.')
    
    cv_file = request.files['cv_file']
    validate_file_upload(cv_file)
    
    assignment_file = request.files.get('assignment_file')
    if assignment_file:
        validate_file_upload(assignment_file)
    
    return {
        "cv_file": cv_file,
        "assignment_file": assignment_file,
        "assignment_data": json.loads(request.form.get('assignment_data', '{}')),
        "consultant_data": json.loads(request.form.get('consultant_data', '{}'))
    }

# --- API Endpoints ---
@app.route('/api/analyze', methods=['POST'])
def analyze_cv_endpoint():
    """Analyze CV against assignment requirements."""
    if not analyzer:
        raise Exception("CV Analyzer not initialized properly.")
    
    form_data = get_request_data()
    
    # Extract CV text
    cv_text = analyzer.extract_text_from_file(
        form_data['cv_file'].read(), 
        form_data['cv_file'].filename
    )
    
    # Get assignment text
    assignment_text = form_data['assignment_data'].get('description', '')
    
    # Extract assignment file text if provided
    if form_data['assignment_file']:
        assignment_file_text = analyzer.extract_text_from_file(
            form_data['assignment_file'].read(), 
            form_data['assignment_file'].filename
        )
        assignment_text += f"\n\n{assignment_file_text}"
    
    # Perform analysis
    analysis_result = analyzer.analyze_cv_assignment_match(cv_text, assignment_text)
    
    return jsonify({
        'success': True, 
        'analysis': analysis_result, 
        'cv_text': cv_text
    })

@app.route('/api/generate-motivations', methods=['POST'])
def generate_motivations_endpoint():
    """Generate motivations for requirements."""
    if not analyzer:
        raise Exception("CV Analyzer not initialized properly.")
    
    data = request.json
    if not all(k in data for k in ['cv_text', 'requirements', 'consultant_name']):
        raise ValueError('Missing required fields: cv_text, requirements, consultant_name.')
    
    motivations = analyzer.generate_motivations(
        data['cv_text'], 
        data['requirements'], 
        data['consultant_name']
    )
    
    return jsonify({'success': True, 'motivations': motivations})

@app.route('/api/generate-cover-letter', methods=['POST'])
def generate_cover_letter_endpoint():
    """Generate cover letter."""
    if not analyzer:
        raise Exception("CV Analyzer not initialized properly.")
    
    data = request.json
    if not all(k in data for k in ['cv_text', 'assignment_info', 'consultant_name', 'analysis_result']):
        raise ValueError('Missing required fields: cv_text, assignment_info, consultant_name, analysis_result.')
    
    cover_letter = analyzer.generate_cover_letter(
        data['cv_text'], 
        data['assignment_info'], 
        data['consultant_name'], 
        data['analysis_result']
    )
    
    return jsonify({'success': True, 'cover_letter': cover_letter})

@app.route('/api/generate-email', methods=['POST'])
def generate_email_endpoint():
    """Generate introduction email."""
    if not analyzer:
        raise Exception("CV Analyzer not initialized properly.")
    
    data = request.json
    if not all(k in data for k in ['consultant_info', 'assignment_info', 'analysis_result']):
        raise ValueError('Missing required fields: consultant_info, assignment_info, analysis_result.')
    
    email = analyzer.generate_introduction_email(
        data['consultant_info'], 
        data['assignment_info'], 
        data['analysis_result']
    )
    
    return jsonify({'success': True, 'email': email})

@app.route('/api/customize-content', methods=['POST'])
def customize_content_endpoint():
    """Customize generated content."""
    if not analyzer:
        raise Exception("CV Analyzer not initialized properly.")
    
    data = request.json
    if not all(k in data for k in ['type', 'content', 'prompt']):
        raise ValueError('Missing required fields: type, content, prompt.')
    
    customized_content = analyzer.customize_content(
        data['type'], 
        data['content'], 
        data['prompt'], 
        data.get('context', {})
    )
    
    return jsonify({'success': True, 'customized_content': customized_content})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy', 
        'service': 'CV Analysis API',
        'analyzer_initialized': analyzer is not None
    })

# --- Error Handlers ---
@app.errorhandler(ValueError)
def handle_validation_error(e):
    logger.error(f"Validation error: {e}", exc_info=True)
    return jsonify({
        "success": False, 
        "error": "validation_error", 
        "message": str(e), 
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 400

@app.errorhandler(RateLimitError)
def handle_rate_limit_error(e):
    logger.error(f"Rate limit exceeded: {e}", exc_info=True)
    return jsonify({
        "success": False, 
        "error": "rate_limit_exceeded", 
        "message": "API rate limit exceeded. Please try again later.", 
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 429

@app.errorhandler(Exception)
def handle_generic_error(e):
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    return jsonify({
        "success": False, 
        "error": "internal_error", 
        "message": str(e), 
        "timestamp": datetime.now(timezone.utc).isoformat()
    }), 500

# --- App Runner ---
if __name__ == '__main__':
    if not analyzer:
        print("FATAL: Application cannot start because CVAnalyzer failed to initialize. Check .env file and logs.")
    else:
        app.run(debug=True, host='0.0.0.0', port=5000)
