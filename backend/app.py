from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from typing import Dict, List, Any
import json
import PyPDF2
import docx
from io import BytesIO
import logging

app = Flask(__name__)
CORS(app)



# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Configure OpenAI API key
# openai.api_key = 


class CVAnalyzer:
    def __init__(self):
        self.client = openai

    
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
            text += page.extract_text() + "\n"
        return text
    
    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def analyze_cv_assignment_match(self, cv_text: str, assignment_text: str) -> Dict[str, Any]:
        """Analyze CV against assignment requirements using GPT-4"""
        
        prompt = f"""
        You are an expert HR consultant specializing in data professional recruitment. 
        Analyze the following CV against the assignment requirements and provide a detailed matching analysis.

        ASSIGNMENT REQUIREMENTS:
        {assignment_text}

        CONSULTANT CV:
        {cv_text}

        Please provide a JSON response with the following structure:
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
        - Technical skills matching (Azure, SQL, Power BI, etc.)
        - Experience relevance
        - Education requirements
        - Soft skills and cultural fit
        - Provide specific examples from the CV
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert HR consultant. Provide detailed, accurate analysis in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            raise Exception(f"Error in CV analysis: {str(e)}")
    
    def generate_motivations(self, cv_text: str, requirements: List[Dict], consultant_name: str) -> Dict[str, str]:
        """Generate personalized motivations for each requirement"""
        
        motivations = {}
        
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
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert at writing compelling, specific motivations for job requirements."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4
                )
                
                motivations[req['id']] = response.choices[0].message.content.strip()
                
            except Exception as e:
                motivations[req['id']] = f"Error generating motivation: {str(e)}"
        
        return motivations
    
    def generate_cover_letter(self, cv_text: str, assignment_info: Dict, consultant_name: str, analysis_result: Dict) -> str:
        """Generate a personalized cover letter"""
        
        prompt = f"""
        Write a professional cover letter for the following consultant and assignment.
        
        CONSULTANT: {consultant_name}
        CLIENT: {assignment_info.get('client', 'the client')}
        POSITION: {assignment_info.get('title', 'the position')}
        OVERALL MATCH SCORE: {analysis_result.get('overall_score', 0)}%
        
        CV CONTENT:
        {cv_text}
        
        ASSIGNMENT DESCRIPTION:
        {assignment_info.get('description', '')}
        
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
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at writing compelling, personalized cover letters for data professionals."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating cover letter: {str(e)}"
    
    def generate_introduction_email(self, consultant_info: Dict, assignment_info: Dict, analysis_result: Dict) -> str:
        """Generate a professional introduction email"""
        
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
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at writing professional business emails for staffing agencies."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating email: {str(e)}"

# Initialize analyzer
analyzer = CVAnalyzer()

# @app.route('/api/analyze', methods=['POST'])
# def analyze_cv():
#     """Analyze CV against assignment requirements"""
#     try:
#         # Get form data
#         cv_file = request.files.get('cv_file')
#         assignment_file = request.files.get('assignment_file')
#         assignment_data = json.loads(request.form.get('assignment_data', '{}'))
#         consultant_data = json.loads(request.form.get('consultant_data', '{}'))
        
#         if not cv_file:
#             return jsonify({'error': 'CV file is required'}), 400
        
#         # Extract CV text
#         cv_content = cv_file.read()
#         cv_text = analyzer.extract_text_from_file(cv_content, cv_file.filename)
        
#         # Get assignment text
#         assignment_text = assignment_data.get('description', '')
#         if assignment_file:
#             assignment_content = assignment_file.read()
#             assignment_file_text = analyzer.extract_text_from_file(assignment_content, assignment_file.filename)
#             assignment_text = f"{assignment_text}\n\n{assignment_file_text}"
        
#         # Perform analysis
#         analysis_result = analyzer.analyze_cv_assignment_match(cv_text, assignment_text)
        
#         return jsonify({
#             'success': True,
#             'analysis': analysis_result
#         })
        
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_cv():
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
            'analysis': analysis_result
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

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'CV Analysis API'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)