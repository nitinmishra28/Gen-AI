# # Working code ----------------------------------
# import json
# import logging
# from flask import Blueprint, request, jsonify

# # Import from src package
# from src.serivces.file_handler import FileHandler  # Note: Directory is actually misspelled in the filesystem
# from src.serivces.analyzer import CVAnalyzer  # Note: Directory is actually misspelled in the filesystem
# from src.config import config

# logger = logging.getLogger(__name__)

# api_blueprint = Blueprint('api', __name__, url_prefix='/api')

# # Instantiate service classes
# file_handler = FileHandler()
# analyzer = CVAnalyzer()

# def get_request_data():
#     """Parses and validates multipart form data from the incoming request."""
#     if 'cv_file' not in request.files:
#         raise ValueError('CV file (`cv_file`) is required.')
        
#     # Get the selected model from the request
#     model_name = request.form.get('model', config.DEFAULT_OPENAI_MODEL)
    
#     # Get the selected model from the request
#     model_name = request.form.get('model', 'gpt-3.5-turbo')  
    
#     cv_file = request.files['cv_file']
#     file_handler.validate_file(cv_file)
    
#     assignment_file = request.files.get('assignment_file')
#     if assignment_file and assignment_file.filename:
#         file_handler.validate_file(assignment_file)
    
#     try:
#         assignment_data = json.loads(request.form.get('assignment_data', '{}'))
#         consultant_data = json.loads(request.form.get('consultant_data', '{}'))
#     except json.JSONDecodeError:
#         raise ValueError("Invalid JSON format in 'assignment_data' or 'consultant_data'.")

#     return {
#         "cv_file": cv_file,
#         "assignment_file": assignment_file,
#         "assignment_data": assignment_data,
#         "consultant_data": consultant_data,
#         "model_name": model_name
#     }

# @api_blueprint.route('/analyze', methods=['POST'])
# def analyze_cv_endpoint():
#     """Endpoint to analyze a CV against assignment requirements."""
#     logger.info("Received request at /api/analyze")
#     form_data = get_request_data()
    
#     cv_text = file_handler.extract_text_from_file(form_data['cv_file'].read(), form_data['cv_file'].filename)
    
#     assignment_text = form_data['assignment_data'].get('description', '')
#     model_name = form_data['model_name']  # Get the model name from the form data
    
#     if form_data['assignment_file'] and form_data['assignment_file'].filename:
#         assignment_file_text = file_handler.extract_text_from_file(
#             form_data['assignment_file'].read(), 
#             form_data['assignment_file'].filename
#         )
#         assignment_text += f"\n\n--- From Uploaded Document ---\n{assignment_file_text}"
    
#     if not assignment_text.strip():
#         raise ValueError("Assignment description cannot be empty. Please provide text or a file.")
        
#     analysis_result = analyzer.analyze_cv_assignment_match(cv_text, assignment_text, model_name=model_name)
    
#     return jsonify({
#         'success': True, 
#         'analysis': analysis_result, 
#         'cv_text': cv_text
#     })

# @api_blueprint.route('/generate-motivations', methods=['POST'])
# def generate_motivations_endpoint():
#     """Endpoint to generate personalized motivations."""
#     logger.info("Received request at /api/generate-motivations")
#     data = request.json
#     required_keys = ['cv_text', 'requirements', 'consultant_name']
#     if not all(k in data for k in required_keys):
#         raise ValueError(f'Missing required fields: {", ".join(required_keys)}')
    
#     model_name = data.get('model', config.DEFAULT_OPENAI_MODEL)
    
#     motivations = analyzer.generate_motivations(
#         data['cv_text'], 
#         data['requirements'], 
#         data['consultant_name'],
#         model_name=model_name
#     )
    
#     return jsonify({'success': True, 'motivations': motivations})

# @api_blueprint.route('/generate-cover-letter', methods=['POST'])
# def generate_cover_letter_endpoint():
#     """Endpoint to generate a cover letter."""
#     logger.info("Received request at /api/generate-cover-letter")
#     data = request.json
#     required_keys = ['cv_text', 'assignment_info', 'consultant_name', 'analysis_result']
#     if not all(k in data for k in required_keys):
#         raise ValueError(f'Missing required fields: {", ".join(required_keys)}')
    
#     model_name = data.get('model', config.DEFAULT_OPENAI_MODEL)
        
#     cover_letter = analyzer.generate_cover_letter(
#         data['cv_text'], 
#         data['assignment_info'], 
#         data['consultant_name'], 
#         data['analysis_result'],
#         model_name=model_name
#     )
    
#     return jsonify({'success': True, 'cover_letter': cover_letter})

# @api_blueprint.route('/generate-email', methods=['POST'])
# def generate_email_endpoint():
#     """Endpoint to generate an introduction email."""
#     logger.info("Received request at /api/generate-email")
#     data = request.json
#     required_keys = ['consultant_info', 'assignment_info', 'analysis_result']
#     if not all(k in data for k in required_keys):
#         raise ValueError(f'Missing required fields: {", ".join(required_keys)}')
    
#     model_name = data.get('model', config.DEFAULT_OPENAI_MODEL)
    
#     email = analyzer.generate_introduction_email(
#         data['consultant_info'], 
#         data['assignment_info'], 
#         data['analysis_result'],
#         model_name=model_name
#     )
    
#     return jsonify({'success': True, 'email': email})

# @api_blueprint.route('/customize-content', methods=['POST'])
# def customize_content_endpoint():
#     """Endpoint to customize generated content based on user feedback."""
#     logger.info("Received request at /api/customize-content")
#     data = request.json
#     required_keys = ['type', 'content', 'prompt']
#     if not all(k in data for k in required_keys):
#         raise ValueError(f'Missing required fields: {", ".join(required_keys)}')
    
#     model_name = data.get('model', config.DEFAULT_OPENAI_MODEL)
    
#     customized_content = analyzer.customize_content(
#         data['type'], 
#         data['content'], 
#         data['prompt'], 
#         data.get('context', {}),
#         model_name=model_name
#     )
    
#     return jsonify({'success': True, 'customized_content': customized_content})



import json
import logging
from typing import Optional, Dict, Any
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse

# Import from src package
from src.serivces.file_handler import FileHandler, get_file_handler  # Note: Directory is actually misspelled in the filesystem
from src.serivces.analyzer import CVAnalyzer  # Note: Directory is actually misspelled in the filesystem
from src.config import config

logger = logging.getLogger(__name__)

# Create the API router (equivalent to Flask Blueprint)
api_router = APIRouter(prefix='/api', tags=["cv-analysis"])

# Instantiate service classes (for backward compatibility)
file_handler = FileHandler()
analyzer = CVAnalyzer()

async def get_request_data(
    cv_file: UploadFile = File(..., description="CV file to analyze"),
    assignment_file: Optional[UploadFile] = File(None, description="Optional assignment file"),
    model: str = Form(default=config.DEFAULT_OPENAI_MODEL, description="OpenAI model to use"),
    assignment_data: str = Form(default='{}', description="Assignment data as JSON string"),
    consultant_data: str = Form(default='{}', description="Consultant data as JSON string"),
    handler: FileHandler = Depends(get_file_handler)
) -> Dict[str, Any]:
    """Parses and validates multipart form data from the incoming request."""
    
    # Validate CV file
    if not cv_file.filename:
        raise HTTPException(status_code=400, detail="CV file is required.")
    
    await handler.validate_file(cv_file)  # Make sure this is awaited
    
    # Validate assignment file if provided
    if assignment_file and assignment_file.filename:
        await handler.validate_file(assignment_file)  # Make sure this is awaited
    
    # Parse JSON data
    try:
        assignment_data_parsed = json.loads(assignment_data)
        consultant_data_parsed = json.loads(consultant_data)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid JSON format in 'assignment_data' or 'consultant_data'."
        )

    return {
        "cv_file": cv_file,
        "assignment_file": assignment_file,
        "assignment_data": assignment_data_parsed,
        "consultant_data": consultant_data_parsed,
        "model_name": model
    }

@api_router.post('/analyze', summary="Analyze CV against assignment requirements")
async def analyze_cv_endpoint(form_data: Dict[str, Any] = Depends(get_request_data)):
    """Endpoint to analyze a CV against assignment requirements."""
    logger.info("Received request at /api/analyze")
    
    # Read CV file content
    cv_content = await form_data['cv_file'].read()
    cv_text = await file_handler.extract_text_from_file(cv_content, form_data['cv_file'].filename)
    
    assignment_text = form_data['assignment_data'].get('description', '')
    model_name = form_data['model_name']
    
    # Handle assignment file if provided
    if form_data['assignment_file'] and form_data['assignment_file'].filename:
        assignment_file_content = await form_data['assignment_file'].read()
        assignment_file_text = await file_handler.extract_text_from_file(
            assignment_file_content, 
            form_data['assignment_file'].filename
        )
        assignment_text += f"\n\n--- From Uploaded Document ---\n{assignment_file_text}"
    
    if not assignment_text.strip():
        raise HTTPException(
            status_code=400, 
            detail="Assignment description cannot be empty. Please provide text or a file."
        )
    
    # Make analyzer methods async as well
    analysis_result = await analyzer.analyze_cv_assignment_match(cv_text, assignment_text, model_name=model_name)
    
    return {
        'success': True, 
        'analysis': analysis_result, 
        'cv_text': cv_text
    }

@api_router.post('/generate-motivations', summary="Generate personalized motivations")
async def generate_motivations_endpoint(request_data: Dict[str, Any]):
    """Endpoint to generate personalized motivations."""
    logger.info("Received request at /api/generate-motivations")
    
    required_keys = ['cv_text', 'requirements', 'consultant_name']
    if not all(k in request_data for k in required_keys):
        raise HTTPException(
            status_code=400, 
            detail=f'Missing required fields: {", ".join(required_keys)}'
        )
    
    model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
    motivations = await analyzer.generate_motivations(
        request_data['cv_text'], 
        request_data['requirements'], 
        request_data['consultant_name'],
        model_name=model_name
    )
    
    return {'success': True, 'motivations': motivations}

@api_router.post('/generate-cover-letter', summary="Generate a cover letter")
async def generate_cover_letter_endpoint(request_data: Dict[str, Any]):
    """Endpoint to generate a cover letter."""
    logger.info("Received request at /api/generate-cover-letter")
    
    required_keys = ['cv_text', 'assignment_info', 'consultant_name', 'analysis_result']
    if not all(k in request_data for k in required_keys):
        raise HTTPException(
            status_code=400, 
            detail=f'Missing required fields: {", ".join(required_keys)}'
        )
    
    model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
        
    cover_letter = await analyzer.generate_cover_letter(
        request_data['cv_text'], 
        request_data['assignment_info'], 
        request_data['consultant_name'], 
        request_data['analysis_result'],
        model_name=model_name
    )
    
    return {'success': True, 'cover_letter': cover_letter}

@api_router.post('/generate-email', summary="Generate an introduction email")
async def generate_email_endpoint(request_data: Dict[str, Any]):
    """Endpoint to generate an introduction email."""
    logger.info("Received request at /api/generate-email")
    
    required_keys = ['consultant_info', 'assignment_info', 'analysis_result']
    if not all(k in request_data for k in required_keys):
        raise HTTPException(
            status_code=400, 
            detail=f'Missing required fields: {", ".join(required_keys)}'
        )
    
    model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
    email = await analyzer.generate_introduction_email(
        request_data['consultant_info'], 
        request_data['assignment_info'], 
        request_data['analysis_result'],
        model_name=model_name
    )
    
    return {'success': True, 'email': email}

@api_router.post('/customize-content', summary="Customize generated content based on user feedback")
async def customize_content_endpoint(request_data: Dict[str, Any]):
    """Endpoint to customize generated content based on user feedback."""
    logger.info("Received request at /api/customize-content")
    
    required_keys = ['type', 'content', 'prompt']
    if not all(k in request_data for k in required_keys):
        raise HTTPException(
            status_code=400, 
            detail=f'Missing required fields: {", ".join(required_keys)}'
        )
    
    model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
    customized_content = await analyzer.customize_content(
        request_data['type'], 
        request_data['content'], 
        request_data['prompt'], 
        request_data.get('context', {}),
        model_name=model_name
    )
    
    return {'success': True, 'customized_content': customized_content}
