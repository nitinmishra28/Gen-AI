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



from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI, RateLimitError
import os
from typing import Dict, List, Any
import json
import PyPDF2
import docx
from io import BytesIO
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from dotenv import load_dotenv
import hashlib

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class CVAnalyzer:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set in .env file")
        self.client = OpenAI(api_key=api_key)
        self.use_mock = os.getenv('USE_MOCK', 'False').lower() == 'true'

    def extract_text_from_file(self, file_content: bytes, filename: str) -> str:
        """Extract text from uploaded file based on file type"""
        try:
            if filename.lower().endswith('.pdf'):
                return self._extract_from_pdf(file_content)
            elif filename.lower().endswith(('.doc', '.docx')):
                return self._extract_from_docx(file_content)
            elif filename.lower().endswith('.txt'):
                return file_content.decode('utf-8')
            else:
                raise ValueError(f"Unsupported file type: {filename}")
        except Exception as e:
            raise Exception(f"Error extracting text from {filename}: {str(e)}")

    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file"""
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        return text

    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def _mock_analysis(self) -> Dict[str, Any]:
        """Mock response for testing without API"""
        return {
            "overall_score": 85,
            "requirements_score": 90,
            "wishes_score": 80,
            "requirements": [
                {
                    "id": "req1",
                    "type": "require",
                    "title": "SQL Proficiency",
                    "description": "Advanced SQL skills",
                    "match": True,
                    "percentage": 95,
                    "explanation": "CV shows 5+ years of SQL experience in data analysis projects."
                }
            ],
            "wishes": [
                {
                    "id": "wish1",
                    "type": "wish",
                    "title": "Power BI Experience",
                    "description": "Familiarity with Power BI",
                    "match": True,
                    "percentage": 80,
                    "explanation": "CV mentions dashboard creation with Power BI."
                }
            ]
        }

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=2, min=4, max=60),
        retry=retry_if_exception_type((RateLimitError, json.JSONDecodeError))
    )
    def _call_openai(self, prompt: str, system_content: str, temperature: float = 0.3) -> str:
        """Internal API call with retry"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            content = response.choices[0].message.content.strip()
            logging.debug(f"Raw OpenAI response: {content}")
            return content
        except RateLimitError as e:
            logging.error(f"Rate limit exceeded: {str(e)}")
            raise
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            raise

    def analyze_cv_assignment_match(self, cv_text: str, assignment_text: str) -> Dict[str, Any]:
        """Analyze CV against assignment requirements using GPT-3.5-turbo"""
        if self.use_mock:
            logging.debug("Using mock analysis response")
            return self._mock_analysis()

        # Validate assignment_text
        if not assignment_text or assignment_text.isspace():
            logging.error("Assignment requirements are empty")
            return {
                "overall_score": 0,
                "requirements_score": 0,
                "wishes_score": 0,
                "requirements": [],
                "wishes": [],
                "error": "Assignment requirements cannot be empty"
            }

        # Truncate inputs to reduce tokens
        cv_text = cv_text[:1000]
        assignment_text = assignment_text[:1000]

        # Cache key based on inputs
        cache_key = hashlib.md5((cv_text + assignment_text).encode()).hexdigest()
        cache_file = f"cache/{cache_key}.json"
        if os.path.exists(cache_file):
            logging.debug(f"Returning cached result for key: {cache_key}")
            with open(cache_file, 'r') as f:
                return json.load(f)

        prompt = f"""
        You are an expert HR consultant specializing in data professional recruitment.
        Analyze the provided CV against the assignment requirements and return a response in **valid JSON format only**.
        Do not include any text outside the JSON object, such as explanations or code fences.

        ASSIGNMENT REQUIREMENTS:
        {assignment_text}

        CONSULTANT CV:
        {cv_text}

        Return a JSON object with the following structure:
        {{
            "overall_score": <number 0-100>,
            "requirements_score": <number 0-100>,
            "wishes_score": <number 0-100>,
            "requirements": [
                {{
                    "id": "<unique_id>",
                    "type": "require",
                    "title": "<requirement_title>",
                    "description": "<requirement_description>",
                    "match": <boolean>,
                    "percentage": <number 0-100>,
                    "explanation": "<detailed_explanation>"
                }}
            ],
            "wishes": [
                {{
                    "id": "<unique_id>",
                    "type": "wish",
                    "title": "<wish_title>",
                    "description": "<wish_description>",
                    "match": <boolean>,
                    "percentage": <number 0-100>,
                    "explanation": "<detailed_explanation>"
                }}
            ]
        }}

        Focus on:
        - Technical skills matching (e.g., Azure, SQL, Power BI)
        - Experience relevance
        - Education requirements
        - Soft skills and cultural fit
        - Provide specific examples from the CV

        If no requirements are provided, return an empty requirements and wishes list with scores of 0.
        Ensure the response is a valid JSON object with no additional text or code fences.
        """

        try:
            content = self._call_openai(
                prompt,
                "You are an expert HR consultant. Return only valid JSON with no additional text or code fences."
            )
            result = json.loads(content)

            # Cache result
            os.makedirs("cache", exist_ok=True)
            with open(cache_file, 'w') as f:
                json.dump(result, f)
            logging.debug(f"Cached result for key: {cache_key}")

            return result
        except json.JSONDecodeError as e:
            logging.error(f"JSON parsing error: {e}, raw content: {content}")
            return {
                "overall_score": 0,
                "requirements_score": 0,
                "wishes_score": 0,
                "requirements": [],
                "wishes": [],
                "error": f"Invalid JSON response from OpenAI: {str(e)}"
            }
        except RateLimitError as e:
            logging.error(f"Rate limit error: {str(e)}")
            return {
                "overall_score": 0,
                "requirements_score": 0,
                "wishes_score": 0,
                "requirements": [],
                "wishes": [],
                "error": "Rate limit exceeded. Please try again later or upgrade your OpenAI plan."
            }
        except Exception as e:
            logging.error(f"API error: {str(e)}")
            return {
                "overall_score": 0,
                "requirements_score": 0,
                "wishes_score": 0,
                "requirements": [],
                "wishes": [],
                "error": f"Error in CV analysis: {str(e)}"
            }

    def generate_motivations(self, cv_text: str, requirements: List[Dict], consultant_name: str) -> Dict[str, str]:
        """Generate personalized motivations for each requirement"""
        if self.use_mock:
            return {req['id']: "Mock motivation for testing." for req in requirements}

        motivations = {}
        cv_text = cv_text[:1000]

        for req in requirements:
            prompt = f"""
            Generate a personalized motivation for the following requirement based on the consultant's CV.
            
            CONSULTANT: {consultant_name}
            REQUIREMENT: {req['title']} - {req['description']}
            MATCH PERCENTAGE: {req['percentage']}%
            
            CV CONTENT:
            {cv_text}
            
            Write a 2-3 sentence motivation that:
            - Specifically addresses this requirement
            - Uses concrete examples from the CV
            - Shows relevant experience and skills
            - Maintains professional tone
            
            If the match is low, acknowledge the gap but highlight transferable skills.
            """

            try:
                content = self._call_openai(
                    prompt,
                    "You are an expert at writing compelling, specific motivations for job requirements.",
                    temperature=0.4
                )
                motivations[req['id']] = content
            except RateLimitError:
                motivations[req['id']] = "Rate limit exceeded. Please try again later."
            except Exception as e:
                motivations[req['id']] = f"Error generating motivation: {str(e)}"

        return motivations

    def generate_cover_letter(self, cv_text: str, assignment_info: Dict, consultant_name: str, analysis_result: Dict) -> str:
        """Generate a personalized cover letter"""
        if self.use_mock:
            return "Mock cover letter for testing."

        cv_text = cv_text[:1000]
        prompt = f"""
        Write a professional cover letter for the following consultant and assignment.
        
        CONSULTANT: {consultant_name}
        CLIENT: {assignment_info.get('client', 'the client')}
        POSITION: {assignment_info.get('title', 'the position')}
        OVERALL MATCH SCORE: {analysis_result.get('overall_score', 0)}%
        
        CV CONTENT:
        {cv_text}
        
        ASSIGNMENT DESCRIPTION:
        {assignment_info.get('description', '')[:1000]}
        
        Write a compelling cover letter that:
        - Opens with a strong, personalized introduction
        - Highlights the most relevant experience and skills
        - Addresses any potential concerns (like education gaps) proactively
        - Shows enthusiasm for the specific role and company
        - Maintains professional yet personal tone
        - Ends with a clear call to action
        - Is approximately 300-400 words
        
        Use specific examples from the CV and make it feel authentic to the consultant's background.
        """

        try:
            content = self._call_openai(
                prompt,
                "You are an expert at writing compelling, personalized cover letters for data professionals.",
                temperature=0.5
            )
            return content
        except RateLimitError:
            return "Rate limit exceeded. Please try again later."
        except Exception as e:
            return f"Error generating cover letter: {str(e)}"

    def generate_introduction_email(self, consultant_info: Dict, assignment_info: Dict, analysis_result: Dict) -> str:
        """Generate a professional introduction email"""
        if self.use_mock:
            return "Mock email for testing."

        consultant_name = consultant_info.get('name', 'the consultant')
        client_name = assignment_info.get('client', 'the client')
        position_title = assignment_info.get('title', 'the position')
        contact_person = consultant_info.get('contactPerson', 'Sir/Madam')
        overall_score = analysis_result.get('overall_score', 0)

        prompt = f"""
        Write a professional introduction email from a staffing agency to a client.
        
        CONSULTANT: {consultant_name}
        CLIENT: {client_name}
        POSITION: {position_title}
        CONTACT PERSON: {contact_person}
        MATCH SCORE: {overall_score}%
        
        Write an email that:
        - Has a clear, professional subject line
        - Addresses the contact person by name
        - Introduces the consultant with key strengths
        - Mentions the high match score and relevant experience
        - Includes standard terms of offer section (with placeholders)
        - Lists attachments (motivation, cover letter)
        - Ends with professional closing and contact information
        - Maintains business-appropriate tone
        - Is concise but informative (200-300 words)
        
        Use "Wanita Bajnath" as the sender name.
        """

        try:
            content = self._call_openai(
                prompt,
                "You are an expert at writing professional business emails for staffing agencies."
            )
            return content
        except RateLimitError:
            return "Rate limit exceeded. Please try again later."
        except Exception as e:
            return f"Error generating email: {str(e)}"

    def customize_content(self, content_type: str, original_content: str, user_prompt: str, context: Dict = None) -> str:
        """Customize content based on user prompt"""
        if self.use_mock:
            return f"Mock customized {content_type} content based on: {user_prompt}"

        system_prompts = {
            'motivation': "You are an expert at customizing motivations for job requirements. Take the original content and modify it based on the user's specific instructions while maintaining professionalism and relevance.",
            'coverletter': "You are an expert at customizing cover letters. Take the original cover letter and modify it based on the user's specific instructions while maintaining professional tone and structure.",
            'email': "You are an expert at customizing professional business emails. Take the original email and modify it based on the user's specific instructions while maintaining business etiquette and clarity."
        }

        context_info = ""
        if context:
            consultant_name = context.get('consultant', {}).get('name', 'the consultant')
            assignment_info = context.get('assignment', {})
            client_name = assignment_info.get('client', 'the client')
            position_title = assignment_info.get('title', 'the position')
            
            context_info = f"""
            CONTEXT:
            - Consultant: {consultant_name}
            - Client: {client_name}
            - Position: {position_title}
            """

        prompt = f"""
        {context_info}
        
        ORIGINAL CONTENT:
        {original_content}
        
        USER INSTRUCTIONS:
        {user_prompt}
        
        Please modify the original content according to the user's instructions. Maintain the same format and professional tone, but incorporate the requested changes. Return only the modified content without any explanations or additional text.
        """

        try:
            content = self._call_openai(
                prompt,
                system_prompts.get(content_type, "You are an expert content editor."),
                temperature=0.4
            )
            return content
        except RateLimitError:
            return f"Rate limit exceeded. Please try again later."
        except Exception as e:
            return f"Error customizing content: {str(e)}"
        
# Initialize analyzer
analyzer = CVAnalyzer()

@app.route('/api/analyze', methods=['POST'])
def analyze_cv():
    """Analyze CV against assignment requirements"""
    try:
        cv_file = request.files.get('cv_file')
        assignment_file = request.files.get('assignment_file')
        assignment_data = json.loads(request.form.get('assignment_data', '{}'))
        consultant_data = json.loads(request.form.get('consultant_data', '{}'))
        
        if not cv_file:
            return jsonify({'error': 'CV file is required'}), 400
        
        cv_content = cv_file.read()
        cv_text = analyzer.extract_text_from_file(cv_content, cv_file.filename)
        
        assignment_text = assignment_data.get('description', '')
        if assignment_file:
            assignment_content = assignment_file.read()
            assignment_file_text = analyzer.extract_text_from_file(assignment_content, assignment_file.filename)
            assignment_text = f"{assignment_text}\n\n{assignment_file_text}"
        
        analysis_result = analyzer.analyze_cv_assignment_match(cv_text, assignment_text)
        
        return jsonify({
            'success': True,
            'analysis': analysis_result,
            'cv_text': cv_text  # Return CV text for later use
        })
    
    except Exception as e:
        logging.error(f"API /api/analyze error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-motivations', methods=['POST'])
def generate_motivations():
    """Generate motivations for requirements"""
    try:
        data = request.json
        cv_text = data.get('cv_text')
        requirements = data.get('requirements', [])
        consultant_name = data.get('consultant_name')
        
        motivations = analyzer.generate_motivations(cv_text, requirements, consultant_name)
        
        return jsonify({
            'success': True,
            'motivations': motivations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    """Generate cover letter"""
    try:
        data = request.json
        cv_text = data.get('cv_text')
        assignment_info = data.get('assignment_info')
        consultant_name = data.get('consultant_name')
        analysis_result = data.get('analysis_result')
        
        cover_letter = analyzer.generate_cover_letter(cv_text, assignment_info, consultant_name, analysis_result)
        
        return jsonify({
            'success': True,
            'cover_letter': cover_letter
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-email', methods=['POST'])
def generate_email():
    """Generate introduction email"""
    try:
        data = request.json
        consultant_info = data.get('consultant_info')
        assignment_info = data.get('assignment_info')
        analysis_result = data.get('analysis_result')
        
        email = analyzer.generate_introduction_email(consultant_info, assignment_info, analysis_result)
        
        return jsonify({
            'success': True,
            'email': email
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customize-content', methods=['POST'])
def customize_content():
    """Customize content with AI based on user prompt"""
    try:
        data = request.json
        content_type = data.get('type')
        original_content = data.get('content')
        user_prompt = data.get('prompt')
        context = data.get('context', {})
        
        if not all([content_type, original_content, user_prompt]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        customized_content = analyzer.customize_content(content_type, original_content, user_prompt, context)
        
        return jsonify({
            'success': True,
            'customized_content': customized_content
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'CV Analysis API'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)