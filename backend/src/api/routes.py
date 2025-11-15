# # import json
# # import logging
# # from typing import Optional, Dict, Any
# # from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
# # from fastapi.responses import JSONResponse
# # from typing import List
# # from src.serivces.translation_service import get_translation_service
# # from src.serivces.comparison_service import ResumeComparisonService

# # # Import from src package
# # from src.serivces.file_handler import FileHandler, get_file_handler  
# # from src.serivces.analyzer import CVAnalyzer  
# # from src.config import config

# # logger = logging.getLogger(__name__)

# # # Create the API router (equivalent to Flask Blueprint)
# # api_router = APIRouter(prefix='/api', tags=["cv-analysis"])

# # # Instantiate service classes (for backward compatibility)
# # file_handler = FileHandler()
# # analyzer = CVAnalyzer()

# # # Initialize translation service
# # translation_service = get_translation_service()

# # async def get_request_data(
# #     cv_file: UploadFile = File(..., description="CV file to analyze"),
# #     assignment_file: Optional[UploadFile] = File(None, description="Optional assignment file"),
# #     model: str = Form(default=config.DEFAULT_OPENAI_MODEL, description="OpenAI model to use"),
# #     assignment_data: str = Form(default='{}', description="Assignment data as JSON string"),
# #     consultant_data: str = Form(default='{}', description="Consultant data as JSON string"),
# #     handler: FileHandler = Depends(get_file_handler)
# # ) -> Dict[str, Any]:
# #     """Parses and validates multipart form data from the incoming request."""
    
# #     # Validate CV file
# #     if not cv_file.filename:
# #         raise HTTPException(status_code=400, detail="CV file is required.")
    
# #     await handler.validate_file(cv_file)  # Make sure this is awaited
    
# #     # Validate assignment file if provided
# #     if assignment_file and assignment_file.filename:
# #         await handler.validate_file(assignment_file)  # Make sure this is awaited
    
# #     # Parse JSON data
# #     try:
# #         assignment_data_parsed = json.loads(assignment_data)
# #         consultant_data_parsed = json.loads(consultant_data)
# #     except json.JSONDecodeError:
# #         raise HTTPException(
# #             status_code=400, 
# #             detail="Invalid JSON format in 'assignment_data' or 'consultant_data'."
# #         )

# #     return {
# #         "cv_file": cv_file,
# #         "assignment_file": assignment_file,
# #         "assignment_data": assignment_data_parsed,
# #         "consultant_data": consultant_data_parsed,
# #         "model_name": model
# #     }
    
# # @api_router.post('/analyze-multiple', summary="Analyze multiple resumes")
# # async def analyze_multiple_resumes(
# #     cv_files: List[UploadFile] = File(..., description="Multiple CV files (max 10)"),
# #     assignment_file: Optional[UploadFile] = File(None),
# #     assignment_data: str = Form(default='{}'),
# #     model: str = Form(default=config.DEFAULT_OPENAI_MODEL),
# #     handler: FileHandler = Depends(get_file_handler)
# # ):
# #     """Analyze multiple resumes with ranking."""
# #     logger.info(f"Received {len(cv_files)} resumes for batch analysis")
    
# #     if len(cv_files) > 10:
# #         raise HTTPException(
# #             status_code=400,
# #             detail="Maximum 10 resumes allowed per batch"
# #         )
    
# #     try:
# #         assignment_parsed = json.loads(assignment_data)
# #     except json.JSONDecodeError:
# #         raise HTTPException(status_code=400, detail="Invalid assignment_data JSON")
    
# #     job_description = assignment_parsed.get('description', '')
    
# #     if assignment_file and assignment_file.filename:
# #         assignment_content = await assignment_file.read()
# #         assignment_text = await handler.extract_text_from_file(
# #             assignment_content,
# #             assignment_file.filename
# #         )
# #         job_description += f"\n\n{assignment_text}"
    
# #     if not job_description.strip():
# #         raise HTTPException(
# #             status_code=400,
# #             detail="Job description is required"
# #         )
    
# #     processed_resumes = []
# #     for cv_file in cv_files:
# #         try:
# #             await handler.validate_file(cv_file)
# #             content = await cv_file.read()
# #             text = await handler.extract_text_from_file(content, cv_file.filename)
            
# #             translation_result = await translation_service.process_resume_with_translation(
# #                 text, target_lang='en'
# #             )
            
# #             processed_resumes.append({
# #                 "filename": cv_file.filename,
# #                 "original_text": text,
# #                 "processed_text": translation_result['processed_text'],
# #                 "detected_language": translation_result['detected_language'],
# #                 "language_name": translation_result['language_name'],
# #                 "was_translated": translation_result['was_translated']
# #             })
            
# #         except Exception as e:
# #             logger.error(f"Error processing {cv_file.filename}: {e}")
# #             processed_resumes.append({
# #                 "filename": cv_file.filename,
# #                 "error": str(e),
# #                 "status": "failed"
# #             })
    
# #     comparison_service = ResumeComparisonService(analyzer)
# #     comparison_result = await comparison_service.compare_resumes(
# #         resumes=processed_resumes,
# #         job_description=job_description,
# #         job_data=assignment_parsed
# #     )
    
# #     return {
# #         'success': True,
# #         'comparison': comparison_result,
# #         'summary': comparison_service.generate_comparison_summary(comparison_result)
# #     }


# # @api_router.post('/generate-motivation-letter', summary="Generate motivation letter")
# # async def generate_motivation_letter_endpoint(
# #     request_data: Dict[str, Any]
# # ):
# #     """Generate personalized motivation letter."""
# #     logger.info("Generating motivation letter")
    
# #     required_keys = ['cv_text', 'job_info', 'candidate_name', 'analysis_result']
# #     if not all(k in request_data for k in required_keys):
# #         raise HTTPException(
# #             status_code=400,
# #             detail=f'Missing required fields'
# #         )
    
# #     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
# #     motivation_letter = await analyzer.generate_motivation_letter(
# #         cv_text=request_data['cv_text'],
# #         job_info=request_data['job_info'],
# #         candidate_name=request_data['candidate_name'],
# #         analysis_result=request_data['analysis_result'],
# #         model_name=model_name
# #     )
    
# #     return {
# #         'success': True,
# #         'motivation_letter': motivation_letter
# #     }


# # @api_router.post('/translate-resume', summary="Translate resume")
# # async def translate_resume_endpoint(
# #     cv_file: UploadFile = File(...),
# #     target_language: str = Form(default='en'),
# #     handler: FileHandler = Depends(get_file_handler)
# # ):
# #     """Detect and translate resume."""
# #     logger.info(f"Translating resume: {cv_file.filename}")
    
# #     await handler.validate_file(cv_file)
# #     content = await cv_file.read()
# #     text = await handler.extract_text_from_file(content, cv_file.filename)
    
# #     result = await translation_service.process_resume_with_translation(
# #         text, target_lang=target_language
# #     )
    
# #     return {
# #         'success': True,
# #         'translation_result': result
# #     }

# # @api_router.post('/analyze', summary="Analyze CV against assignment requirements")
# # async def analyze_cv_endpoint(form_data: Dict[str, Any] = Depends(get_request_data)):
# #     """Endpoint to analyze a CV against assignment requirements."""
# #     logger.info("Received request at /api/analyze")
    
# #     # Read CV file content
# #     cv_content = await form_data['cv_file'].read()
# #     cv_text = await file_handler.extract_text_from_file(cv_content, form_data['cv_file'].filename)
    
# #     assignment_text = form_data['assignment_data'].get('description', '')
# #     model_name = form_data['model_name']
    
# #     # Handle assignment file if provided
# #     if form_data['assignment_file'] and form_data['assignment_file'].filename:
# #         assignment_file_content = await form_data['assignment_file'].read()
# #         assignment_file_text = await file_handler.extract_text_from_file(
# #             assignment_file_content, 
# #             form_data['assignment_file'].filename
# #         )
# #         assignment_text += f"\n\n--- From Uploaded Document ---\n{assignment_file_text}"
    
# #     if not assignment_text.strip():
# #         raise HTTPException(
# #             status_code=400, 
# #             detail="Assignment description cannot be empty. Please provide text or a file."
# #         )
    
# #     # Make analyzer methods async as well
# #     analysis_result = await analyzer.analyze_cv_assignment_match(cv_text, assignment_text, model_name=model_name)
    
# #     return {
# #         'success': True, 
# #         'analysis': analysis_result, 
# #         'cv_text': cv_text
# #     }

# # @api_router.post('/generate-motivations', summary="Generate personalized motivations")
# # async def generate_motivations_endpoint(request_data: Dict[str, Any]):
# #     """Endpoint to generate personalized motivations."""
# #     logger.info("Received request at /api/generate-motivations")
    
# #     required_keys = ['cv_text', 'requirements', 'consultant_name']
# #     if not all(k in request_data for k in required_keys):
# #         raise HTTPException(
# #             status_code=400, 
# #             detail=f'Missing required fields: {", ".join(required_keys)}'
# #         )
    
# #     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
# #     motivations = await analyzer.generate_motivations(
# #         request_data['cv_text'], 
# #         request_data['requirements'], 
# #         request_data['consultant_name'],
# #         model_name=model_name
# #     )
    
# #     return {'success': True, 'motivations': motivations}

# # @api_router.post('/generate-cover-letter', summary="Generate a cover letter")
# # async def generate_cover_letter_endpoint(request_data: Dict[str, Any]):
# #     """Endpoint to generate a cover letter."""
# #     logger.info("Received request at /api/generate-cover-letter")
    
# #     required_keys = ['cv_text', 'assignment_info', 'consultant_name', 'analysis_result']
# #     if not all(k in request_data for k in required_keys):
# #         raise HTTPException(
# #             status_code=400, 
# #             detail=f'Missing required fields: {", ".join(required_keys)}'
# #         )
    
# #     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
        
# #     cover_letter = await analyzer.generate_cover_letter(
# #         request_data['cv_text'], 
# #         request_data['assignment_info'], 
# #         request_data['consultant_name'], 
# #         request_data['analysis_result'],
# #         model_name=model_name
# #     )
    
# #     return {'success': True, 'cover_letter': cover_letter}

# # @api_router.post('/generate-email', summary="Generate an introduction email")
# # async def generate_email_endpoint(request_data: Dict[str, Any]):
# #     """Endpoint to generate an introduction email."""
# #     logger.info("Received request at /api/generate-email")
    
# #     required_keys = ['consultant_info', 'assignment_info', 'analysis_result']
# #     if not all(k in request_data for k in required_keys):
# #         raise HTTPException(
# #             status_code=400, 
# #             detail=f'Missing required fields: {", ".join(required_keys)}'
# #         )
    
# #     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
# #     email = await analyzer.generate_introduction_email(
# #         request_data['consultant_info'], 
# #         request_data['assignment_info'], 
# #         request_data['analysis_result'],
# #         model_name=model_name
# #     )
    
# #     return {'success': True, 'email': email}

# # @api_router.post('/customize-content', summary="Customize generated content based on user feedback")
# # async def customize_content_endpoint(request_data: Dict[str, Any]):
# #     """Endpoint to customize generated content based on user feedback."""
# #     logger.info("Received request at /api/customize-content")
    
# #     required_keys = ['type', 'content', 'prompt']
# #     if not all(k in request_data for k in required_keys):
# #         raise HTTPException(
# #             status_code=400, 
# #             detail=f'Missing required fields: {", ".join(required_keys)}'
# #         )
    
# #     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
# #     customized_content = await analyzer.customize_content(
# #         request_data['type'], 
# #         request_data['content'], 
# #         request_data['prompt'], 
# #         request_data.get('context', {}),
# #         model_name=model_name
# #     )
    
# #     return {'success': True, 'customized_content': customized_content}









# import json
# import logging

# from fastapi.responses import JSONResponse
# from src.serivces.translation_service import get_translation_service
# from src.serivces.comparison_service import ResumeComparisonService

# # Import from src package
# from src.serivces.file_handler import FileHandler, get_file_handler  
# from src.serivces.analyzer import CVAnalyzer  
# from src.config import config

# from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
# from typing import List, Optional, Dict, Any
# import zipfile
# import io
# import logging

# logger = logging.getLogger(__name__)

# api_router = APIRouter(prefix='/api', tags=["cv-analysis"])

# # # Instantiate service classes (for backward compatibility)
# file_handler = FileHandler()
# analyzer = CVAnalyzer()

# # # Initialize translation service
# translation_service = get_translation_service()

# @api_router.post('/analyze-multiple', summary="Analyze multiple resumes")
# async def analyze_multiple_resumes(
#     cv_files: List[UploadFile] = File(..., description="Multiple CV files (max 10)"),
#     assignment_file: Optional[UploadFile] = File(None),
#     assignment_data: str = Form(default='{}'),
#     model: str = Form(default=config.DEFAULT_OPENAI_MODEL),
#     handler: FileHandler = Depends(get_file_handler)
# ):
#     """Analyze multiple resumes with ranking and score tracking."""
#     logger.info(f"Received {len(cv_files)} files for batch analysis using model: {model}")
    
#     all_cv_files = []
#     for cv_file in cv_files:
#         if cv_file.filename.endswith('.zip'):
#             # Extract ZIP file
#             content = await cv_file.read()
#             with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
#                 for file_info in zip_ref.namelist():
#                     if file_info.endswith(('.pdf', '.docx', '.doc', '.txt')):
#                         file_content = zip_ref.read(file_info)
#                         # Create UploadFile-like object
#                         extracted_file = UploadFile(
#                             filename=file_info,
#                             file=io.BytesIO(file_content)
#                         )
#                         all_cv_files.append(extracted_file)
#         else:
#             all_cv_files.append(cv_file)
    
#     if len(all_cv_files) > 10:
#         raise HTTPException(
#             status_code=400,
#             detail="Maximum 10 resumes allowed per batch"
#         )
    
#     try:
#         assignment_parsed = json.loads(assignment_data)
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=400, detail="Invalid assignment_data JSON")
    
#     job_description = assignment_parsed.get('description', '')
    
#     if assignment_file and assignment_file.filename:
#         assignment_content = await assignment_file.read()
#         assignment_text = await handler.extract_text_from_file(
#             assignment_content,
#             assignment_file.filename
#         )
#         job_description += f"\n\n{assignment_text}"
    
#     if not job_description.strip():
#         raise HTTPException(
#             status_code=400,
#             detail="Job description is required"
#         )
    
#     processed_resumes = []
#     for cv_file in all_cv_files:
#         try:
#             await handler.validate_file(cv_file)
#             content = await cv_file.read()
#             text = await handler.extract_text_from_file(content, cv_file.filename)
            
#             translation_result = await translation_service.process_resume_with_translation(
#                 text, target_lang='en'
#             )
            
#             processed_resumes.append({
#                 "filename": cv_file.filename,
#                 "original_text": text,
#                 "processed_text": translation_result['processed_text'],
#                 "detected_language": translation_result['detected_language'],
#                 "language_name": translation_result['language_name'],
#                 "was_translated": translation_result['was_translated']
#             })
            
#         except Exception as e:
#             logger.error(f"Error processing {cv_file.filename}: {e}")
#             processed_resumes.append({
#                 "filename": cv_file.filename,
#                 "error": str(e),
#                 "status": "failed"
#             })
    
#     comparison_service = ResumeComparisonService(analyzer)
    
#     comparison_result = await comparison_service.compare_resumes(
#         resumes=processed_resumes,
#         job_description=job_description,
#         job_data=assignment_parsed,
#         model_name=model
#     )
    
#     return {
#         'success': True,
#         'comparison': comparison_result,
#         'summary': comparison_service.generate_comparison_summary(comparison_result),
#         'model_used': model
#     }

# @api_router.post('/customize-content', summary="Customize generated content based on user feedback")
# async def customize_content_endpoint(request_data: Dict[str, Any]):
#     """Endpoint to customize generated content with score recalculation."""
#     logger.info("Received request at /api/customize-content")
    
#     required_keys = ['type', 'content', 'prompt']
#     if not all(k in request_data for k in required_keys):
#         raise HTTPException(
#             status_code=400, 
#             detail=f'Missing required fields: {", ".join(required_keys)}'
#         )
    
#     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
#     customized_content = await analyzer.customize_content(
#         request_data['type'], 
#         request_data['content'], 
#         request_data['prompt'], 
#         request_data.get('context', {}),
#         model_name=model_name
#     )
    
#     new_score = None
#     if 'context' in request_data and 'analysisData' in request_data['context']:
#         analysis_data = request_data['context']['analysisData']
#         # Calculate new score based on updated analysis
#         matched_reqs = sum(1 for r in analysis_data.get('requirements', []) if r.get('match'))
#         total_reqs = len(analysis_data.get('requirements', [])) or 1
#         matched_wishes = sum(1 for w in analysis_data.get('wishes', []) if w.get('match'))
#         total_wishes = len(analysis_data.get('wishes', [])) or 1
        
#         req_score = (matched_reqs / total_reqs) * 100
#         wish_score = (matched_wishes / total_wishes) * 100
#         new_score = req_score * 0.7 + wish_score * 0.3
    
#     return {
#         'success': True,
#         'customized_content': customized_content,
#         'new_score': new_score
#     }

# import json
# import logging
# import zipfile
# import io
# from typing import Optional, Dict, Any, List
# from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
# from fastapi.responses import JSONResponse

# from src.serivces.translation_service import get_translation_service
# from src.serivces.comparison_service import ResumeComparisonService
# from src.serivces.file_handler import FileHandler, get_file_handler  
# from src.serivces.analyzer import CVAnalyzer  
# from src.config import config

# logger = logging.getLogger(__name__)

# # Create the API router
# api_router = APIRouter(prefix='/api', tags=["cv-analysis"])

# # Instantiate service classes
# file_handler = FileHandler()
# analyzer = CVAnalyzer()
# translation_service = get_translation_service()

# async def get_request_data(
#     cv_file: UploadFile = File(..., description="CV file to analyze"),
#     assignment_file: Optional[UploadFile] = File(None, description="Optional assignment file"),
#     model: str = Form(default=config.DEFAULT_OPENAI_MODEL, description="LLM model to use"),
#     assignment_data: str = Form(default='{}', description="Assignment data as JSON string"),
#     consultant_data: str = Form(default='{}', description="Consultant data as JSON string"),
#     handler: FileHandler = Depends(get_file_handler)
# ) -> Dict[str, Any]:
#     """Parses and validates multipart form data from the incoming request."""
    
#     if not cv_file.filename:
#         raise HTTPException(status_code=400, detail="CV file is required.")
    
#     await handler.validate_file(cv_file)
    
#     if assignment_file and assignment_file.filename:
#         await handler.validate_file(assignment_file)
    
#     try:
#         assignment_data_parsed = json.loads(assignment_data)
#         consultant_data_parsed = json.loads(consultant_data)
#     except json.JSONDecodeError:
#         raise HTTPException(
#             status_code=400, 
#             detail="Invalid JSON format in 'assignment_data' or 'consultant_data'."
#         )

#     return {
#         "cv_file": cv_file,
#         "assignment_file": assignment_file,
#         "assignment_data": assignment_data_parsed,
#         "consultant_data": consultant_data_parsed,
#         "model_name": model
#     }

# @api_router.post('/analyze-multiple', summary="Analyze multiple resumes with ranking")
# async def analyze_multiple_resumes(
#     cv_files: List[UploadFile] = File(..., description="Multiple CV files or ZIP (max 10 resumes)"),
#     assignment_file: Optional[UploadFile] = File(None),
#     assignment_data: str = Form(default='{}'),
#     model: str = Form(default=config.DEFAULT_OPENAI_MODEL),
#     handler: FileHandler = Depends(get_file_handler)
# ):
#     """Analyze multiple resumes with ranking and score tracking. Supports ZIP files."""
#     logger.info(f"Received {len(cv_files)} files for batch analysis using model: {model}")
    
#     all_cv_files = []
#     for cv_file in cv_files:
#         if cv_file.filename.endswith('.zip'):
#             content = await cv_file.read()
#             try:
#                 with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
#                     for file_info in zip_ref.namelist():
#                         if file_info.endswith(('.pdf', '.docx', '.doc', '.txt')) and not file_info.startswith('__MACOSX'):
#                             file_content = zip_ref.read(file_info)
#                             extracted_file = UploadFile(
#                                 filename=file_info.split('/')[-1],
#                                 file=io.BytesIO(file_content)
#                             )
#                             all_cv_files.append(extracted_file)
#                             logger.info(f"Extracted {file_info} from ZIP")
#             except zipfile.BadZipFile:
#                 raise HTTPException(status_code=400, detail=f"Invalid ZIP file: {cv_file.filename}")
#         else:
#             all_cv_files.append(cv_file)
    
#     if len(all_cv_files) > 10:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Maximum 10 resumes allowed per batch. Found {len(all_cv_files)} resumes."
#         )
    
#     try:
#         assignment_parsed = json.loads(assignment_data)
#     except json.JSONDecodeError:
#         raise HTTPException(status_code=400, detail="Invalid assignment_data JSON")
    
#     job_description = assignment_parsed.get('description', '')
    
#     if assignment_file and assignment_file.filename:
#         assignment_content = await assignment_file.read()
#         assignment_text = await handler.extract_text_from_file(
#             assignment_content,
#             assignment_file.filename
#         )
#         job_description += f"\n\n{assignment_text}"
    
#     if not job_description.strip():
#         raise HTTPException(
#             status_code=400,
#             detail="Job description is required"
#         )
    
#     processed_resumes = []
#     for cv_file in all_cv_files:
#         try:
#             await handler.validate_file(cv_file)
#             content = await cv_file.read()
#             text = await handler.extract_text_from_file(content, cv_file.filename)
            
#             translation_result = await translation_service.process_resume_with_translation(
#                 text, target_lang='en'
#             )
            
#             processed_resumes.append({
#                 "filename": cv_file.filename,
#                 "original_text": text,
#                 "processed_text": translation_result['processed_text'],
#                 "detected_language": translation_result['detected_language'],
#                 "language_name": translation_result['language_name'],
#                 "was_translated": translation_result['was_translated']
#             })
            
#         except Exception as e:
#             logger.error(f"Error processing {cv_file.filename}: {e}")
#             processed_resumes.append({
#                 "filename": cv_file.filename,
#                 "error": str(e),
#                 "status": "failed"
#             })
    
#     comparison_service = ResumeComparisonService(analyzer)
#     comparison_result = await comparison_service.compare_resumes(
#         resumes=processed_resumes,
#         job_description=job_description,
#         job_data=assignment_parsed,
#         model_name=model
#     )
    
#     return {
#         'success': True,
#         'comparison': comparison_result,
#         'summary': comparison_service.generate_comparison_summary(comparison_result),
#         'model_used': model
#     }

# @api_router.post('/analyze', summary="Analyze CV against assignment requirements")
# async def analyze_cv_endpoint(form_data: Dict[str, Any] = Depends(get_request_data)):
#     """Endpoint to analyze a single CV against assignment requirements."""
#     logger.info(f"Received request at /api/analyze using model: {form_data['model_name']}")
    
#     cv_content = await form_data['cv_file'].read()
#     cv_text = await file_handler.extract_text_from_file(cv_content, form_data['cv_file'].filename)
    
#     assignment_text = form_data['assignment_data'].get('description', '')
#     model_name = form_data['model_name']
    
#     if form_data['assignment_file'] and form_data['assignment_file'].filename:
#         assignment_file_content = await form_data['assignment_file'].read()
#         assignment_file_text = await file_handler.extract_text_from_file(
#             assignment_file_content, 
#             form_data['assignment_file'].filename
#         )
#         assignment_text += f"\n\n--- From Uploaded Document ---\n{assignment_file_text}"
    
#     if not assignment_text.strip():
#         raise HTTPException(
#             status_code=400, 
#             detail="Assignment description cannot be empty. Please provide text or a file."
#         )
    
#     analysis_result = await analyzer.analyze_cv_assignment_match(
#         cv_text, 
#         assignment_text, 
#         model_name=model_name
#     )
    
#     analysis_result['initial_score'] = analysis_result['overall_score']
#     analysis_result['customization_count'] = 0
    
#     return {
#         'success': True, 
#         'analysis': analysis_result, 
#         'cv_text': cv_text,
#         'model_used': model_name
#     }

# @api_router.post('/generate-motivations', summary="Generate personalized motivations")
# async def generate_motivations_endpoint(request_data: Dict[str, Any]):
#     """Endpoint to generate personalized motivations."""
#     logger.info("Received request at /api/generate-motivations")
    
#     required_keys = ['cv_text', 'requirements', 'consultant_name']
#     if not all(k in request_data for k in required_keys):
#         raise HTTPException(
#             status_code=400, 
#             detail=f'Missing required fields: {", ".join(required_keys)}'
#         )
    
#     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
#     motivations = await analyzer.generate_motivations(
#         request_data['cv_text'], 
#         request_data['requirements'], 
#         request_data['consultant_name'],
#         model_name=model_name
#     )
    
#     return {'success': True, 'motivations': motivations}

# @api_router.post('/generate-cover-letter', summary="Generate a cover letter")
# async def generate_cover_letter_endpoint(request_data: Dict[str, Any]):
#     """Endpoint to generate a cover letter."""
#     logger.info("Received request at /api/generate-cover-letter")
    
#     required_keys = ['cv_text', 'assignment_info', 'consultant_name', 'analysis_result']
#     if not all(k in request_data for k in required_keys):
#         raise HTTPException(
#             status_code=400, 
#             detail=f'Missing required fields: {", ".join(required_keys)}'
#         )
    
#     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
        
#     cover_letter = await analyzer.generate_cover_letter(
#         request_data['cv_text'], 
#         request_data['assignment_info'], 
#         request_data['consultant_name'], 
#         request_data['analysis_result'],
#         model_name=model_name
#     )
    
#     return {'success': True, 'cover_letter': cover_letter}

# @api_router.post('/generate-email', summary="Generate an introduction email")
# async def generate_email_endpoint(request_data: Dict[str, Any]):
#     """Endpoint to generate an introduction email."""
#     logger.info("Received request at /api/generate-email")
    
#     required_keys = ['consultant_info', 'assignment_info', 'analysis_result']
#     if not all(k in request_data for k in required_keys):
#         raise HTTPException(
#             status_code=400, 
#             detail=f'Missing required fields: {", ".join(required_keys)}'
#         )
    
#     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
#     email = await analyzer.generate_introduction_email(
#         request_data['consultant_info'], 
#         request_data['assignment_info'], 
#         request_data['analysis_result'],
#         model_name=model_name
#     )
    
#     return {'success': True, 'email': email}

# @api_router.post('/generate-motivation-letter', summary="Generate motivation letter")
# async def generate_motivation_letter_endpoint(request_data: Dict[str, Any]):
#     """Generate personalized motivation letter."""
#     logger.info("Generating motivation letter")
    
#     required_keys = ['cv_text', 'job_info', 'candidate_name', 'analysis_result']
#     if not all(k in request_data for k in required_keys):
#         raise HTTPException(
#             status_code=400,
#             detail=f'Missing required fields'
#         )
    
#     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
#     motivation_letter = await analyzer.generate_motivation_letter(
#         cv_text=request_data['cv_text'],
#         job_info=request_data['job_info'],
#         candidate_name=request_data['candidate_name'],
#         analysis_result=request_data['analysis_result'],
#         model_name=model_name
#     )
    
#     return {
#         'success': True,
#         'motivation_letter': motivation_letter
#     }

# @api_router.post('/customize-content', summary="Customize generated content with score tracking")
# async def customize_content_endpoint(request_data: Dict[str, Any]):
#     """Endpoint to customize generated content and track score improvements."""
#     logger.info("Received request at /api/customize-content")
    
#     required_keys = ['type', 'content', 'prompt']
#     if not all(k in request_data for k in required_keys):
#         raise HTTPException(
#             status_code=400, 
#             detail=f'Missing required fields: {", ".join(required_keys)}'
#         )
    
#     model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
#     customized_content = await analyzer.customize_content(
#         request_data['type'], 
#         request_data['content'], 
#         request_data['prompt'], 
#         request_data.get('context', {}),
#         model_name=model_name
#     )
    
#     new_score = None
#     score_improvement = None
    
#     if 'context' in request_data:
#         context = request_data['context']
#         if 'cv_text' in context and 'assignment_text' in context:
#             # Re-analyze with customized content to get new score
#             try:
#                 new_analysis = await analyzer.analyze_cv_assignment_match(
#                     cv_text=context['cv_text'],
#                     assignment_text=context['assignment_text'],
#                     model_name=model_name
#                 )
#                 new_score = new_analysis.get('overall_score', 0)
                
#                 # Calculate improvement if initial score exists
#                 if 'initial_score' in context:
#                     initial_score = context['initial_score']
#                     score_improvement = new_score - initial_score
#                     improvement_percentage = (score_improvement / initial_score * 100) if initial_score > 0 else 0
                    
#                     logger.info(f"Score improved from {initial_score}% to {new_score}% (+{improvement_percentage:.1f}%)")
                    
#             except Exception as e:
#                 logger.error(f"Error recalculating score: {e}")
    
#     return {
#         'success': True,
#         'customized_content': customized_content,
#         'new_score': new_score,
#         'score_improvement': score_improvement
#     }

# @api_router.post('/translate-resume', summary="Translate resume")
# async def translate_resume_endpoint(
#     cv_file: UploadFile = File(...),
#     target_language: str = Form(default='en'),
#     handler: FileHandler = Depends(get_file_handler)
# ):
#     """Detect and translate resume."""
#     logger.info(f"Translating resume: {cv_file.filename}")
    
#     await handler.validate_file(cv_file)
#     content = await cv_file.read()
#     text = await handler.extract_text_from_file(content, cv_file.filename)
    
#     result = await translation_service.process_resume_with_translation(
#         text, target_lang=target_language
#     )
    
#     return {
#         'success': True,
#         'translation_result': result
#     }










import json
import logging
import zipfile
import io
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse

from src.serivces.translation_service import get_translation_service
from src.serivces.comparison_service import ResumeComparisonService
from src.serivces.file_handler import FileHandler, get_file_handler  
from src.serivces.analyzer import CVAnalyzer  
from src.config import config
from src.serivces.MatchCalculator import MatchCalculator

logger = logging.getLogger(__name__)

# Create the API router
api_router = APIRouter(prefix='/api', tags=["cv-analysis"])

# Instantiate service classes
file_handler = FileHandler()
analyzer = CVAnalyzer()
translation_service = get_translation_service()
match_calculator = MatchCalculator()

async def get_request_data(
    cv_file: UploadFile = File(..., description="CV file to analyze"),
    assignment_file: Optional[UploadFile] = File(None, description="Optional assignment file"),
    model: str = Form(default=config.DEFAULT_OPENAI_MODEL, description="LLM model to use"),
    assignment_data: str = Form(default='{}', description="Assignment data as JSON string"),
    consultant_data: str = Form(default='{}', description="Consultant data as JSON string"),
    handler: FileHandler = Depends(get_file_handler)
) -> Dict[str, Any]:
    """Parses and validates multipart form data from the incoming request."""
    
    if not cv_file.filename:
        raise HTTPException(status_code=400, detail="CV file is required.")
    
    await handler.validate_file(cv_file)
    
    if assignment_file and assignment_file.filename:
        await handler.validate_file(assignment_file)
    
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

@api_router.post('/analyze-multiple', summary="Analyze multiple resumes with ranking")
async def analyze_multiple_resumes(
    cv_files: List[UploadFile] = File(..., description="Multiple CV files or ZIP (max 10 resumes)"),
    assignment_file: Optional[UploadFile] = File(None),
    assignment_data: str = Form(default='{}'),
    model: str = Form(default=config.DEFAULT_OPENAI_MODEL),
    handler: FileHandler = Depends(get_file_handler)
):
    """Analyze multiple resumes with ranking and score tracking. Supports ZIP files."""
    logger.info(f"Received {len(cv_files)} files for batch analysis using model: {model}")
    
    all_cv_files = []
    for cv_file in cv_files:
        if cv_file.filename.endswith('.zip'):
            content = await cv_file.read()
            try:
                with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
                    for file_info in zip_ref.namelist():
                        if file_info.endswith(('.pdf', '.docx', '.doc', '.txt')) and not file_info.startswith('__MACOSX'):
                            file_content = zip_ref.read(file_info)
                            extracted_file = UploadFile(
                                filename=file_info.split('/')[-1],
                                file=io.BytesIO(file_content)
                            )
                            all_cv_files.append(extracted_file)
                            logger.info(f"Extracted {file_info} from ZIP")
            except zipfile.BadZipFile:
                raise HTTPException(status_code=400, detail=f"Invalid ZIP file: {cv_file.filename}")
        else:
            all_cv_files.append(cv_file)
    
    if len(all_cv_files) > 10:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum 10 resumes allowed per batch. Found {len(all_cv_files)} resumes."
        )
    
    try:
        assignment_parsed = json.loads(assignment_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid assignment_data JSON")
    
    job_description = assignment_parsed.get('description', '')
    
    if assignment_file and assignment_file.filename:
        assignment_content = await assignment_file.read()
        assignment_text = await handler.extract_text_from_file(
            assignment_content,
            assignment_file.filename
        )
        job_description += f"\n\n{assignment_text}"
    
    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description is required"
        )
    
    processed_resumes = []
    for cv_file in all_cv_files:
        try:
            await handler.validate_file(cv_file)
            content = await cv_file.read()
            text = await handler.extract_text_from_file(content, cv_file.filename)
            
            translation_result = await translation_service.process_resume_with_translation(
                text, target_lang='en'
            )
            
            processed_resumes.append({
                "filename": cv_file.filename,
                "original_text": text,
                "processed_text": translation_result['processed_text'],
                "detected_language": translation_result['detected_language'],
                "language_name": translation_result['language_name'],
                "was_translated": translation_result['was_translated']
            })
            
        except Exception as e:
            logger.error(f"Error processing {cv_file.filename}: {e}")
            processed_resumes.append({
                "filename": cv_file.filename,
                "error": str(e),
                "status": "failed"
            })
    
    comparison_service = ResumeComparisonService(analyzer)
    comparison_result = await comparison_service.compare_resumes(
        resumes=processed_resumes,
        job_description=job_description,
        job_data=assignment_parsed,
        model_name=model
    )
    
    return {
        'success': True,
        'comparison': comparison_result,
        'summary': comparison_service.generate_comparison_summary(comparison_result),
        'model_used': model
    }

@api_router.post('/analyze', summary="Analyze CV against assignment requirements")
async def analyze_cv_endpoint(form_data: Dict[str, Any] = Depends(get_request_data)):
    """Endpoint to analyze a single CV against assignment requirements."""
    logger.info(f"Received request at /api/analyze using model: {form_data['model_name']}")
    
    cv_content = await form_data['cv_file'].read()
    cv_text = await file_handler.extract_text_from_file(cv_content, form_data['cv_file'].filename)
    
    assignment_text = form_data['assignment_data'].get('description', '')
    model_name = form_data['model_name']
    
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
    
    analysis_result = await analyzer.analyze_cv_assignment_match(
        cv_text, 
        assignment_text, 
        model_name=model_name
    )
    
    analysis_result['initial_score'] = analysis_result['overall_score']
    analysis_result['customization_count'] = 0
    
    return {
        'success': True, 
        'analysis': analysis_result, 
        'cv_text': cv_text,
        'model_used': model_name
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

@api_router.post('/generate-motivation-letter', summary="Generate motivation letter")
async def generate_motivation_letter_endpoint(request_data: Dict[str, Any]):
    """Generate personalized motivation letter."""
    logger.info("Generating motivation letter")
    
    required_keys = ['cv_text', 'job_info', 'candidate_name', 'analysis_result']
    if not all(k in request_data for k in required_keys):
        raise HTTPException(
            status_code=400,
            detail=f'Missing required fields'
        )
    
    model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    
    motivation_letter = await analyzer.generate_motivation_letter(
        cv_text=request_data['cv_text'],
        job_info=request_data['job_info'],
        candidate_name=request_data['candidate_name'],
        analysis_result=request_data['analysis_result'],
        model_name=model_name
    )
    
    return {
        'success': True,
        'motivation_letter': motivation_letter
    }

@api_router.post('/customize-content', summary="Customize generated content with dynamic score tracking")
async def customize_content_endpoint(request_data: Dict[str, Any]):
    """Endpoint to customize generated content and dynamically recalculate match scores."""
    logger.info(f"Received request at /api/customize-content for type: {request_data.get('type')}")
    
    required_keys = ['type', 'content', 'prompt']
    if not all(k in request_data for k in required_keys):
        raise HTTPException(
            status_code=400, 
            detail=f'Missing required fields: {", ".join(required_keys)}'
        )
    
    model_name = request_data.get('model', config.DEFAULT_OPENAI_MODEL)
    content_type = request_data['type']
    
    customized_content = await analyzer.customize_content(
        content_type, 
        request_data['content'], 
        request_data['prompt'], 
        request_data.get('context', {}),
        model_name=model_name
    )
    
    new_match_percentage = None
    context = request_data.get('context', {})
    
    if content_type == 'motivation':
        # Recalculate motivation match percentage
        if 'requirement' in context and 'cv_text' in context:
            new_match_percentage = await match_calculator.recalculate_motivation_match(
                motivation_text=customized_content,
                requirement=context['requirement'],
                cv_text=context.get('cv_text', '')
            )
            logger.info(f"Motivation match recalculated: {new_match_percentage:.1f}%")
    
    elif content_type == 'cover_letter':
        # Recalculate cover letter match percentage
        if 'requirements' in context:
            new_match_percentage = await match_calculator.recalculate_cover_letter_match(
                cover_letter_text=customized_content,
                requirements=context['requirements'],
                assignment_description=context.get('assignment_description', '')
            )
            logger.info(f"Cover letter match recalculated: {new_match_percentage:.1f}%")
    
    elif content_type == 'email':
        # Recalculate email match percentage
        if 'requirements' in context:
            new_match_percentage = await match_calculator.recalculate_email_match(
                email_text=customized_content,
                requirements=context['requirements'],
                consultant_name=context.get('consultant_name', '')
            )
            logger.info(f"Email match recalculated: {new_match_percentage:.1f}%")
    
    elif content_type == 'cv' or content_type == 'analysis':
        # Recalculate full CV analysis score
        if 'cv_text' in context and 'assignment_text' in context:
            try:
                new_analysis = await analyzer.analyze_cv_assignment_match(
                    cv_text=customized_content,
                    assignment_text=context['assignment_text'],
                    model_name=model_name
                )
                new_match_percentage = new_analysis.get('overall_score', 0)
                logger.info(f"CV analysis score recalculated: {new_match_percentage:.1f}%")
            except Exception as e:
                logger.error(f"Error recalculating CV score: {e}")
    
    # Calculate score improvement
    score_improvement = None
    improvement_percentage = None
    if new_match_percentage is not None and 'initial_match_percentage' in context:
        initial_score = context['initial_match_percentage']
        score_improvement = new_match_percentage - initial_score
        improvement_percentage = (score_improvement / initial_score * 100) if initial_score > 0 else 0
        
        logger.info(
            f"Score improved from {initial_score:.1f}% to {new_match_percentage:.1f}% "
            f"({'+' if score_improvement >= 0 else ''}{score_improvement:.1f}%, "
            f"{'+' if improvement_percentage >= 0 else ''}{improvement_percentage:.1f}%)"
        )
    
    return {
        'success': True,
        'customized_content': customized_content,
        'new_match_percentage': new_match_percentage,
        'score_improvement': score_improvement,
        'improvement_percentage': improvement_percentage,
        'content_type': content_type
    }

@api_router.post('/recalculate-motivations', summary="Recalculate match percentages for all motivations")
async def recalculate_motivations_endpoint(request_data: Dict[str, Any]):
    """Recalculate match percentages for all motivations after customization."""
    logger.info("Recalculating all motivation match percentages")
    
    required_keys = ['motivations', 'requirements', 'cv_text']
    if not all(k in request_data for k in required_keys):
        raise HTTPException(
            status_code=400,
            detail=f'Missing required fields: {", ".join(required_keys)}'
        )
    
    updated_percentages = await match_calculator.batch_recalculate_motivations(
        motivations=request_data['motivations'],
        requirements=request_data['requirements'],
        cv_text=request_data['cv_text']
    )
    
    return {
        'success': True,
        'updated_percentages': updated_percentages
    }

@api_router.post('/translate-resume', summary="Translate resume")
async def translate_resume_endpoint(
    cv_file: UploadFile = File(...),
    target_language: str = Form(default='en'),
    handler: FileHandler = Depends(get_file_handler)
):
    """Detect and translate resume."""
    logger.info(f"Translating resume: {cv_file.filename}")
    
    await handler.validate_file(cv_file)
    content = await cv_file.read()
    text = await handler.extract_text_from_file(content, cv_file.filename)
    
    result = await translation_service.process_resume_with_translation(
        text, target_lang=target_language
    )
    
    return {
        'success': True,
        'translation_result': result
    }
