import json
import logging
from flask import Blueprint, request, jsonify

# Import from src package
from src.serivces.file_handler import FileHandler  # Note: Directory is actually misspelled in the filesystem
from src.serivces.analyzer import CVAnalyzer  # Note: Directory is actually misspelled in the filesystem
from src.config import config

logger = logging.getLogger(__name__)

api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# Instantiate service classes
file_handler = FileHandler()
analyzer = CVAnalyzer()

def get_request_data():
    """Parses and validates multipart form data from the incoming request."""
    if 'cv_file' not in request.files:
        raise ValueError('CV file (`cv_file`) is required.')
        
    # Get the selected model from the request
    model_name = request.form.get('model', config.DEFAULT_OPENAI_MODEL)
    
    # Get the selected model from the request
    model_name = request.form.get('model', 'gpt-3.5-turbo')  
    
    cv_file = request.files['cv_file']
    file_handler.validate_file(cv_file)
    
    assignment_file = request.files.get('assignment_file')
    if assignment_file and assignment_file.filename:
        file_handler.validate_file(assignment_file)
    
    try:
        assignment_data = json.loads(request.form.get('assignment_data', '{}'))
        consultant_data = json.loads(request.form.get('consultant_data', '{}'))
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON format in 'assignment_data' or 'consultant_data'.")

    return {
        "cv_file": cv_file,
        "assignment_file": assignment_file,
        "assignment_data": assignment_data,
        "consultant_data": consultant_data,
        "model_name": model_name
    }

@api_blueprint.route('/analyze', methods=['POST'])
def analyze_cv_endpoint():
    """Endpoint to analyze a CV against assignment requirements."""
    logger.info("Received request at /api/analyze")
    form_data = get_request_data()
    
    cv_text = file_handler.extract_text_from_file(form_data['cv_file'].read(), form_data['cv_file'].filename)
    
    assignment_text = form_data['assignment_data'].get('description', '')
    model_name = form_data['model_name']  # Get the model name from the form data
    
    if form_data['assignment_file'] and form_data['assignment_file'].filename:
        assignment_file_text = file_handler.extract_text_from_file(
            form_data['assignment_file'].read(), 
            form_data['assignment_file'].filename
        )
        assignment_text += f"\n\n--- From Uploaded Document ---\n{assignment_file_text}"
    
    if not assignment_text.strip():
        raise ValueError("Assignment description cannot be empty. Please provide text or a file.")
        
    analysis_result = analyzer.analyze_cv_assignment_match(cv_text, assignment_text, model_name=model_name)
    
    return jsonify({
        'success': True, 
        'analysis': analysis_result, 
        'cv_text': cv_text
    })

@api_blueprint.route('/generate-motivations', methods=['POST'])
def generate_motivations_endpoint():
    """Endpoint to generate personalized motivations."""
    logger.info("Received request at /api/generate-motivations")
    data = request.json
    required_keys = ['cv_text', 'requirements', 'consultant_name']
    if not all(k in data for k in required_keys):
        raise ValueError(f'Missing required fields: {", ".join(required_keys)}')
    
    model_name = data.get('model', config.DEFAULT_OPENAI_MODEL)
    
    motivations = analyzer.generate_motivations(
        data['cv_text'], 
        data['requirements'], 
        data['consultant_name'],
        model_name=model_name
    )
    
    return jsonify({'success': True, 'motivations': motivations})

@api_blueprint.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter_endpoint():
    """Endpoint to generate a cover letter."""
    logger.info("Received request at /api/generate-cover-letter")
    data = request.json
    required_keys = ['cv_text', 'assignment_info', 'consultant_name', 'analysis_result']
    if not all(k in data for k in required_keys):
        raise ValueError(f'Missing required fields: {", ".join(required_keys)}')
    
    model_name = data.get('model', config.DEFAULT_OPENAI_MODEL)
        
    cover_letter = analyzer.generate_cover_letter(
        data['cv_text'], 
        data['assignment_info'], 
        data['consultant_name'], 
        data['analysis_result'],
        model_name=model_name
    )
    
    return jsonify({'success': True, 'cover_letter': cover_letter})

@api_blueprint.route('/generate-email', methods=['POST'])
def generate_email_endpoint():
    """Endpoint to generate an introduction email."""
    logger.info("Received request at /api/generate-email")
    data = request.json
    required_keys = ['consultant_info', 'assignment_info', 'analysis_result']
    if not all(k in data for k in required_keys):
        raise ValueError(f'Missing required fields: {", ".join(required_keys)}')
    
    model_name = data.get('model', config.DEFAULT_OPENAI_MODEL)
    
    email = analyzer.generate_introduction_email(
        data['consultant_info'], 
        data['assignment_info'], 
        data['analysis_result'],
        model_name=model_name
    )
    
    return jsonify({'success': True, 'email': email})

@api_blueprint.route('/customize-content', methods=['POST'])
def customize_content_endpoint():
    """Endpoint to customize generated content based on user feedback."""
    logger.info("Received request at /api/customize-content")
    data = request.json
    required_keys = ['type', 'content', 'prompt']
    if not all(k in data for k in required_keys):
        raise ValueError(f'Missing required fields: {", ".join(required_keys)}')
    
    model_name = data.get('model', config.DEFAULT_OPENAI_MODEL)
    
    customized_content = analyzer.customize_content(
        data['type'], 
        data['content'], 
        data['prompt'], 
        data.get('context', {}),
        model_name=model_name
    )
    
    return jsonify({'success': True, 'customized_content': customized_content})
