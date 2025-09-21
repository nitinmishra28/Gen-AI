# # # run_evaluation.py

# # # It seems there's a typo in your directory name. Ensure this matches your actual folder.
# # # If your folder is named 'services', change the import line accordingly.
# # from src.serivces.analyzer import CVAnalyzer
# # from src.serivces.evaluation_service import EvaluationService

# # # --- SETUP ---
# # # This initializes your classes that will call the LLMs and calculate scores.
# # analyzer = CVAnalyzer()
# # evaluator = EvaluationService()

# # # 1. DEFINE YOUR TEST CASE
# # # USE A REAL CV HERE: The text should be the content of a resume, not a cover letter.
# # # Using triple quotes """ allows for clean, multi-line strings.
# # cv_text = """
# # Jane Doe
# # Full-Stack Developer
# # (123) 456-7890 | jane.doe@email.com | linkedin.com/in/janedoe

# # PROFESSIONAL SUMMARY
# # A results-driven Full-Stack Developer with 1.5 years of experience at BITTWOBYTE TECHNOLOGY, specializing in building and maintaining business intelligence applications. Proficient in React, Python/Flask, and SQL, with a proven ability to integrate complex APIs and implement robust back-end solutions. Passionate about writing clean code and creating data-driven applications.

# # WORK EXPERIENCE
# # BITTWOBYTE TECHNOLOGY PRIVATE LIMITED | Full-Stack Developer | Jan 2024 - Present
# # - Designed and developed front-end components for a business intelligence dashboard using React and Material-UI, improving data visualization capabilities.
# # - Built and maintained back-end services with Python and Flask, handling API requests and business logic for data processing.
# # - Integrated the HubSpot API to extract and process workflow data, enabling new filtering and reporting features.
# # - Implemented a Role-Based Access Control (RBAC) system from scratch, enhancing application security and user management.
# # - Optimized SQL queries for a PostgreSQL database, reducing report generation time by 25%.

# # TECHNICAL SKILLS
# # - Languages: Python, JavaScript, SQL, HTML/CSS
# # - Frameworks: React, Flask, Node.js
# # - Databases: PostgreSQL, MongoDB
# # - Tools: Git, Docker, Postman, HubSpot API, Jira
# # """

# # # The job description for the role.
# # assignment_info = {
# #     "description": """
# # Summary
# # We are seeking a skilled and enthusiastic Software Developer to join our team. You will be responsible for building and maintaining software applications, writing clean and efficient code, and collaborating with cross-functional teams throughout the software development lifecycle. The ideal candidate has strong problem-solving skills, a passion for technology, and the ability to adapt to new languages and frameworks.

# # Responsibilities
# # - Design and develop high-quality, scalable software applications.
# # - Write clean, functional, and well-documented code in appropriate programming languages.
# # - Test and debug software to ensure optimal performance.
# # - Collaborate with product managers and other developers.
# # - Participate in code reviews and improve coding standards.
# # - Integrate third-party APIs and services.

# # Required skills and qualifications
# # - Bachelor's degree in a related field.
# # - Proficiency in a language like Python or Java.
# # - Understanding of the software development lifecycle (SDLC) and Agile.
# # - Experience with Git, database systems, and strong problem-solving skills.
# # """
# # }

# # consultant_name = "Jane Doe"
# # # This is passed to the cover letter function but is empty for this test, which is fine.
# # analysis_result = {}

# # # 2. DEFINE YOUR "GOLDEN" REFERENCE OUTPUT
# # # This is a high-quality example you've written yourself.
# # # It should be a strong, concise cover letter for the CV and job description above.
# # reference_cover_letter = """
# # Dear Hiring Manager,

# # I am writing to express my strong interest in the Software Developer position. My 1.5 years of experience as a Full-Stack Developer at BITTWOBYTE TECHNOLOGY has equipped me with a robust skill set in Python, Flask, and React, directly aligning with your job requirements.

# # In my current role, I have designed and implemented secure back-end services, integrated complex third-party APIs like HubSpot, and optimized database queries to improve performance. These hands-on experiences make me confident that I can contribute effectively to your team from day one.

# # I am passionate about building high-quality software and am eager to bring my technical skills and problem-solving abilities to your team. Thank you for your time and consideration.

# # Sincerely,
# # Jane Doe
# # """

# # # --- RUN EVALUATION ---
# # print("Running evaluations for Cover Letter Generation...")

# # # Generate cover letters using both models.
# # cover_letter_gpt35 = analyzer.generate_cover_letter(
# #     cv_text, assignment_info, consultant_name, analysis_result, model_name='gemma2:9b-instruct-q4_K_M'
# # )

# # cover_letter_gpt4 = analyzer.generate_cover_letter(
# #     cv_text, assignment_info, consultant_name, analysis_result, model_name='gemma3:1b'
# # )

# # # --- CALCULATE SCORES ---
# # # BLEU Scores (higher is better - measures similarity to your reference)
# # bleu_gpt35 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_gpt35)
# # bleu_gpt4 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_gpt4)

# # # Perplexity Scores (lower is better - measures fluency and coherence)
# # perplexity_gpt35 = evaluator.calculate_perplexity(cover_letter_gpt35)
# # perplexity_gpt4 = evaluator.calculate_perplexity(cover_letter_gpt4)

# # # --- PRINT REPORT ---
# # # Use f-strings for clean, readable output.
# # print("\n--- Evaluation Report ---")
# # print(f"Model: gpt-3.5-turbo")
# # print(f"  - BLEU Score: {bleu_gpt35:.4f}")
# # print(f"  - Perplexity: {perplexity_gpt35:.2f}")

# # print("\nGPT-3.5 Generated Letter:")
# # print("-" * 30)
# # print(cover_letter_gpt35)
# # print("-" * 30)

# # print(f"\nModel: gpt-4")
# # print(f"  - BLEU Score: {bleu_gpt4:.4f}")
# # print(f"  - Perplexity: {perplexity_gpt4:.2f}")

# # print("\nGPT-4 Generated Letter:")
# # print("-" * 30)
# # print(cover_letter_gpt4)
# # print("-" * 30)

# # run_evaluation.py

# # Make sure this import path matches your directory structure.
# # If your folder is named 'services', change 'serivces' to 'services'.

# # from src.serivces.analyzer import CVAnalyzer
# # from src.serivces.evaluation_service import EvaluationService

# # # --- SETUP ---
# # # This initializes your classes that will call the LLMs and calculate scores.
# # analyzer = CVAnalyzer()
# # evaluator = EvaluationService()

# # # 1. DEFINE YOUR TEST CASE
# # # Using triple quotes """ allows for clean, multi-line strings.
# # cv_text = """
# # Jane Doe
# # Full-Stack Developer
# # (123) 456-7890 | jane.doe@email.com | linkedin.com/in/janedoe

# # PROFESSIONAL SUMMARY
# # A results-driven Full-Stack Developer with 1.5 years of experience at BITTWOBYTE TECHNOLOGY, specializing in building and maintaining business intelligence applications. Proficient in React, Python/Flask, and SQL, with a proven ability to integrate complex APIs and implement robust back-end solutions. Passionate about writing clean code and creating data-driven applications.

# # WORK EXPERIENCE
# # BITTWOBYTE TECHNOLOGY PRIVATE LIMITED | Full-Stack Developer | Jan 2024 - Present
# # - Designed and developed front-end components for a business intelligence dashboard using React and Material-UI, improving data visualization capabilities.
# # - Built and maintained back-end services with Python and Flask, handling API requests and business logic for data processing.
# # - Integrated the HubSpot API to extract and process workflow data, enabling new filtering and reporting features.
# # - Implemented a Role-Based Access Control (RBAC) system from scratch, enhancing application security and user management.
# # - Optimized SQL queries for a PostgreSQL database, reducing report generation time by 25%.

# # TECHNICAL SKILLS
# # - Languages: Python, JavaScript, SQL, HTML/CSS
# # - Frameworks: React, Flask, Node.js
# # - Databases: PostgreSQL, MongoDB
# # - Tools: Git, Docker, Postman, HubSpot API, Jira
# # """

# # # The job description for the role.
# # assignment_info = {
# #     "description": """
# # Summary
# # We are seeking a skilled and enthusiastic Software Developer to join our team. You will be responsible for building and maintaining software applications, writing clean and efficient code, and collaborating with cross-functional teams throughout the software development lifecycle. The ideal candidate has strong problem-solving skills, a passion for technology, and the ability to adapt to new languages and frameworks.

# # Responsibilities
# # - Design and develop high-quality, scalable software applications.
# # - Write clean, functional, and well-documented code in appropriate programming languages.
# # - Test and debug software to ensure optimal performance.
# # - Collaborate with product managers and other developers.
# # - Participate in code reviews and improve coding standards.
# # - Integrate third-party APIs and services.

# # Required skills and qualifications
# # - Bachelor's degree in a related field.
# # - Proficiency in a language like Python or Java.
# # - Understanding of the software development lifecycle (SDDC) and Agile.
# # - Experience with Git, database systems, and strong problem-solving skills.
# # """
# # }

# # consultant_name = "Jane Doe"
# # # This is passed to the cover letter function but is empty for this test, which is fine.
# # analysis_result = {}

# # # 2. DEFINE YOUR "GOLDEN" REFERENCE OUTPUT
# # reference_cover_letter = """
# # Dear Hiring Manager,

# # I am writing to express my strong interest in the Software Developer position. My 1.5 years of experience as a Full-Stack Developer at BITTWOBYTE TECHNOLOGY has equipped me with a robust skill set in Python, Flask, and React, directly aligning with your job requirements.

# # In my current role, I have designed and implemented secure back-end services, integrated complex third-party APIs like HubSpot, and optimized database queries to improve performance. These hands-on experiences make me confident that I can contribute effectively to your team from day one.

# # I am passionate about building high-quality software and am eager to bring my technical skills and problem-solving abilities to your team. Thank you for your time and consideration.

# # Sincerely,
# # Jane Doe
# # """

# # # --- RUN EVALUATION ---
# # print("Running evaluations for Cover Letter Generation using local Ollama models...")

# # # Define the models you are testing
# # model_1_name = 'gemma2:9b-instruct-q4_K_M'
# # model_2_name = 'gemma3:1b' 
# # model_3_name = 'gemini-pro-flash' 

# # # Generate cover letters using your specified models.
# # cover_letter_model_1 = analyzer.generate_cover_letter(
# #     cv_text, assignment_info, consultant_name, analysis_result, model_name=model_1_name
# # )

# # cover_letter_model_2 = analyzer.generate_cover_letter(
# #     cv_text, assignment_info, consultant_name, analysis_result, model_name=model_2_name
# # )
# # cover_letter_model_3 = analyzer.generate_cover_letter(cv_text, assignment_info, consultant_name, analysis_result, model_name=model_3_name) # NEW

# # # --- CALCULATE SCORES ---
# # # BLEU Scores (higher is better)
# # bleu_model_1 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_1)
# # bleu_model_2 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_2)
# # bleu_model_3 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_3) # NEW


# # # Perplexity Scores (lower is better)
# # perplexity_model_1 = evaluator.calculate_perplexity(cover_letter_model_1)
# # perplexity_model_2 = evaluator.calculate_perplexity(cover_letter_model_2)
# # perplexity_model_3 = evaluator.calculate_perplexity(cover_letter_model_3)

# # # --- PRINT REPORT ---
# # # Use f-strings and the model name variables for a dynamic and accurate report.
# # print("\n--- Evaluation Report ---")
# # print(f"Model: {model_1_name}")
# # print(f"  - BLEU Score: {bleu_model_1:.4f}")
# # print(f"  - Perplexity: {perplexity_model_1:.2f}")

# # print(f"\nGenerated Letter ({model_1_name}):")
# # print("-" * 30)
# # print(cover_letter_model_1)
# # print("-" * 30)

# # print(f"\nModel: {model_2_name}")
# # print(f"  - BLEU Score: {bleu_model_2:.4f}")
# # print(f"  - Perplexity: {perplexity_model_2:.2f}")

# # print(f"\nGenerated Letter ({model_2_name}):")
# # print("-" * 30)
# # print(cover_letter_model_2)
# # print("-" * 30)


# # print(f"\nModel: {model_3_name}")
# # print(f"  - BLEU Score: {bleu_model_3:.4f}")
# # print(f"  - Perplexity: {perplexity_model_3:.2f}")
# # print(f"\nGenerated Letter ({model_3_name}):")
# # print("-" * 30)
# # print(cover_letter_model_3)
# # print("-" * 30)







# from src.serivces.analyzer import CVAnalyzer
# from src.serivces.evaluation_service import EvaluationService

# # --- SETUP ---
# analyzer = CVAnalyzer()
# evaluator = EvaluationService()

# # 1. DEFINE YOUR TEST CASE
# cv_text = """
# Jane Doe
# Full-Stack Developer
# (123) 456-7890 | jane.doe@email.com | linkedin.com/in/janedoe

# PROFESSIONAL SUMMARY
# A results-driven Full-Stack Developer with 1.5 years of experience at BITTWOBYTE TECHNOLOGY, specializing in building and maintaining business intelligence applications. Proficient in React, Python/Flask, and SQL, with a proven ability to integrate complex APIs and implement robust back-end solutions. Passionate about writing clean code and creating data-driven applications.

# WORK EXPERIENCE
# BITTWOBYTE TECHNOLOGY PRIVATE LIMITED | Full-Stack Developer | Jan 2024 - Present
# - Designed and developed front-end components for a business intelligence dashboard using React and Material-UI, improving data visualization capabilities.
# - Built and maintained back-end services with Python and Flask, handling API requests and business logic for data processing.
# - Integrated the HubSpot API to extract and process workflow data, enabling new filtering and reporting features.
# - Implemented a Role-Based Access Control (RBAC) system from scratch, enhancing application security and user management.
# - Optimized SQL queries for a PostgreSQL database, reducing report generation time by 25%.

# TECHNICAL SKILLS
# - Languages: Python, JavaScript, SQL, HTML/CSS
# - Frameworks: React, Flask, Node.js
# - Databases: PostgreSQL, MongoDB
# - Tools: Git, Docker, Postman, HubSpot API, Jira
# """

# assignment_info = {
#     "description": """
# Summary
# We are seeking a skilled and enthusiastic Software Developer to join our team. You will be responsible for building and maintaining software applications, writing clean and efficient code, and collaborating with cross-functional teams throughout the software development lifecycle. The ideal candidate has strong problem-solving skills, a passion for technology, and the ability to adapt to new languages and frameworks.

# Responsibilities
# - Design and develop high-quality, scalable software applications.
# - Write clean, functional, and well-documented code in appropriate programming languages.
# - Test and debug software to ensure optimal performance.
# - Collaborate with product managers and other developers.
# - Participate in code reviews and improve coding standards.
# - Integrate third-party APIs and services.

# Required skills and qualifications
# - Bachelor's degree in a related field.
# - Proficiency in a language like Python or Java.
# - Understanding of the software development lifecycle (SDLC) and Agile.
# - Experience with Git, database systems, and strong problem-solving skills.
# """
# }

# consultant_name = "Jane Doe"
# analysis_result = {}

# # 2. DEFINE YOUR "GOLDEN" REFERENCE OUTPUT
# reference_cover_letter = """
# Dear Hiring Manager,

# I am writing to express my strong interest in the Software Developer position. My 1.5 years of experience as a Full-Stack Developer at BITTWOBYTE TECHNOLOGY has equipped me with a robust skill set in Python, Flask, and React, directly aligning with your job requirements.

# In my current role, I have designed and implemented secure back-end services, integrated complex third-party APIs like HubSpot, and optimized database queries to improve performance. These hands-on experiences make me confident that I can contribute effectively to your team from day one.

# I am passionate about building high-quality software and am eager to bring my technical skills and problem-solving abilities to your team. Thank you for your time and consideration.

# Sincerely,
# Jane Doe
# """

# # --- RUN EVALUATION ---
# print("Running evaluations for Cover Letter Generation using local Ollama models and Gemini...")

# # Define the models you are testing
# model_1_name = 'gemma2:9b-instruct-q4_K_M'
# model_2_name = 'gemma3:1b'
# model_3_name = 'gemini-1.5-flash'  # Updated to a valid Gemini model

# # Generate cover letters using your specified models
# try:
#     cover_letter_model_1 = analyzer.generate_cover_letter(
#         cv_text, assignment_info, consultant_name, analysis_result, model_name=model_1_name
#     )
# except Exception as e:
#     print(f"Error generating cover letter for {model_1_name}: {e}")
#     cover_letter_model_1 = "Error: Could not generate cover letter."

# try:
#     cover_letter_model_2 = analyzer.generate_cover_letter(
#         cv_text, assignment_info, consultant_name, analysis_result, model_name=model_2_name
#     )
# except Exception as e:
#     print(f"Error generating cover letter for {model_2_name}: {e}")
#     cover_letter_model_2 = "Error: Could not generate cover letter."

# try:
#     cover_letter_model_3 = analyzer.generate_cover_letter(
#         cv_text, assignment_info, consultant_name, analysis_result, model_name=model_3_name
#     )
# except Exception as e:
#     print(f"Error generating cover letter for {model_3_name}: {e}")
#     cover_letter_model_3 = "Error: Could not generate cover letter."

# # --- CALCULATE SCORES ---
# # BLEU Scores (higher is better)
# bleu_model_1 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_1) if cover_letter_model_1.startswith("Dear") else 0.0
# bleu_model_2 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_2) if cover_letter_model_2.startswith("Dear") else 0.0
# bleu_model_3 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_3) if cover_letter_model_3.startswith("Dear") else 0.0

# # Perplexity Scores (lower is better)
# perplexity_model_1 = evaluator.calculate_perplexity(cover_letter_model_1) if cover_letter_model_1.startswith("Dear") else float('inf')
# perplexity_model_2 = evaluator.calculate_perplexity(cover_letter_model_2) if cover_letter_model_2.startswith("Dear") else float('inf')
# perplexity_model_3 = evaluator.calculate_perplexity(cover_letter_model_3) if cover_letter_model_3.startswith("Dear") else float('inf')

# # --- PRINT REPORT ---
# print("\n--- Evaluation Report ---")
# print(f"Model: {model_1_name}")
# print(f"  - BLEU Score: {bleu_model_1:.4f}")
# print(f"  - Perplexity: {perplexity_model_1:.2f}")
# print(f"\nGenerated Letter ({model_1_name}):")
# print("-" * 30)
# print(cover_letter_model_1)
# print("-" * 30)

# print(f"\nModel: {model_2_name}")
# print(f"  - BLEU Score: {bleu_model_2:.4f}")
# print(f"  - Perplexity: {perplexity_model_2:.2f}")
# print(f"\nGenerated Letter ({model_2_name}):")
# print("-" * 30)
# print(cover_letter_model_2)
# print("-" * 30)

# print(f"\nModel: {model_3_name}")
# print(f"  - BLEU Score: {bleu_model_3:.4f}")
# print(f"  - Perplexity: {perplexity_model_3:.2f}")
# print(f"\nGenerated Letter ({model_3_name}):")
# print("-" * 30)
# print(cover_letter_model_3)
# print("-" * 30)



from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import asyncio
import logging

from src.serivces.analyzer import CVAnalyzer
from src.serivces.evaluation_service import EvaluationService, get_evaluation_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CV Analysis Evaluation API",
    description="API for evaluating CV analysis and cover letter generation using multiple models",
    version="1.0.0"
)

# Pydantic models for request/response
class EvaluationRequest(BaseModel):
    cv_text: str
    assignment_info: Dict[str, Any]
    consultant_name: str
    models: List[str]
    reference_cover_letter: Optional[str] = None

class ModelResult(BaseModel):
    model_name: str
    cover_letter: str
    bleu_score: float
    perplexity: float
    error: Optional[str] = None

class EvaluationResponse(BaseModel):
    results: List[ModelResult]
    summary: Dict[str, Any]

# Dependency to get analyzer
async def get_analyzer() -> CVAnalyzer:
    return CVAnalyzer()

# Test data endpoint
@app.get("/test-data")
async def get_test_data():
    """Get predefined test data for evaluation."""
    return {
        "cv_text": """Jane Doe
Full-Stack Developer
(123) 456-7890 | jane.doe@email.com | linkedin.com/in/janedoe

PROFESSIONAL SUMMARY
A results-driven Full-Stack Developer with 1.5 years of experience at BITTWOBYTE TECHNOLOGY, specializing in building and maintaining business intelligence applications. Proficient in React, Python/Flask, and SQL, with a proven ability to integrate complex APIs and implement robust back-end solutions. Passionate about writing clean code and creating data-driven applications.

WORK EXPERIENCE
BITTWOBYTE TECHNOLOGY PRIVATE LIMITED | Full-Stack Developer | Jan 2024 - Present
- Designed and developed front-end components for a business intelligence dashboard using React and Material-UI, improving data visualization capabilities.
- Built and maintained back-end services with Python and Flask, handling API requests and business logic for data processing.
- Integrated the HubSpot API to extract and process workflow data, enabling new filtering and reporting features.
- Implemented a Role-Based Access Control (RBAC) system from scratch, enhancing application security and user management.
- Optimized SQL queries for a PostgreSQL database, reducing report generation time by 25%.

TECHNICAL SKILLS
- Languages: Python, JavaScript, SQL, HTML/CSS
- Frameworks: React, Flask, Node.js
- Databases: PostgreSQL, MongoDB
- Tools: Git, Docker, Postman, HubSpot API, Jira""",
        
        "assignment_info": {
            "description": """Summary
We are seeking a skilled and enthusiastic Software Developer to join our team. You will be responsible for building and maintaining software applications, writing clean and efficient code, and collaborating with cross-functional teams throughout the software development lifecycle. The ideal candidate has strong problem-solving skills, a passion for technology, and the ability to adapt to new languages and frameworks.

Responsibilities
- Design and develop high-quality, scalable software applications.
- Write clean, functional, and well-documented code in appropriate programming languages.
- Test and debug software to ensure optimal performance.
- Collaborate with product managers and other developers.
- Participate in code reviews and improve coding standards.
- Integrate third-party APIs and services.

Required skills and qualifications
- Bachelor's degree in a related field.
- Proficiency in a language like Python or Java.
- Understanding of the software development lifecycle (SDLC) and Agile.
- Experience with Git, database systems, and strong problem-solving skills."""
        },
        
        "consultant_name": "Jane Doe",
        
        "reference_cover_letter": """Dear Hiring Manager,

I am writing to express my strong interest in the Software Developer position. My 1.5 years of experience as a Full-Stack Developer at BITTWOBYTE TECHNOLOGY has equipped me with a robust skill set in Python, Flask, and React, directly aligning with your job requirements.

In my current role, I have designed and implemented secure back-end services, integrated complex third-party APIs like HubSpot, and optimized database queries to improve performance. These hands-on experiences make me confident that I can contribute effectively to your team from day one.

I am passionate about building high-quality software and am eager to bring my technical skills and problem-solving abilities to your team. Thank you for your time and consideration.

Sincerely,
Jane Doe""",
        
        "models": [
            "gpt-3.5-turbo",
            "gpt-4-turbo",
            "gemma2:9b-instruct-q4_K_M",
            "gemma3:1b", 
            "gemini-1.5-flash"
        ]
    }

@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_models(
    request: EvaluationRequest,
    analyzer: CVAnalyzer = Depends(get_analyzer),
    evaluator: EvaluationService = Depends(get_evaluation_service)
):
    """
    Evaluate multiple models for cover letter generation.
    """
    logger.info(f"Starting evaluation for {len(request.models)} models")
    
    results = []
    analysis_result = {}  # Empty for now, can be populated if needed
    
    # Process each model
    async def evaluate_single_model(model_name: str) -> ModelResult:
        """Evaluate a single model."""
        try:
            logger.info(f"Generating cover letter with {model_name}")
            
            # Generate cover letter
            cover_letter = await analyzer.generate_cover_letter(
                request.cv_text, 
                request.assignment_info, 
                request.consultant_name, 
                analysis_result, 
                model_name=model_name
            )
            
            # Calculate metrics if cover letter was generated successfully
            if cover_letter and not cover_letter.startswith("Error:"):
                bleu_score = 0.0
                if request.reference_cover_letter:
                    bleu_score = await evaluator.calculate_bleu(
                        request.reference_cover_letter, 
                        cover_letter
                    )
                
                perplexity = await evaluator.calculate_perplexity(cover_letter)
                
                return ModelResult(
                    model_name=model_name,
                    cover_letter=cover_letter,
                    bleu_score=bleu_score,
                    perplexity=perplexity
                )
            else:
                return ModelResult(
                    model_name=model_name,
                    cover_letter=cover_letter or "No output generated",
                    bleu_score=0.0,
                    perplexity=float('inf'),
                    error="Failed to generate valid cover letter"
                )
                
        except Exception as e:
            logger.error(f"Error evaluating {model_name}: {e}")
            return ModelResult(
                model_name=model_name,
                cover_letter=f"Error: {str(e)}",
                bleu_score=0.0,
                perplexity=float('inf'),
                error=str(e)
            )
    
    # Run evaluations concurrently
    tasks = [evaluate_single_model(model) for model in request.models]
    results = await asyncio.gather(*tasks)
    
    # Calculate summary statistics
    valid_results = [r for r in results if r.error is None]
    summary = {
        "total_models": len(request.models),
        "successful_evaluations": len(valid_results),
        "failed_evaluations": len(results) - len(valid_results),
    }
    
    if valid_results:
        summary.update({
            "average_bleu": sum(r.bleu_score for r in valid_results) / len(valid_results),
            "average_perplexity": sum(r.perplexity for r in valid_results) / len(valid_results),
            "best_bleu_model": max(valid_results, key=lambda x: x.bleu_score).model_name,
            "best_perplexity_model": min(valid_results, key=lambda x: x.perplexity).model_name
        })
    
    logger.info(f"Evaluation completed. {len(valid_results)}/{len(request.models)} successful")
    
    return EvaluationResponse(results=results, summary=summary)

@app.post("/evaluate-quick")
async def evaluate_quick_test(
    analyzer: CVAnalyzer = Depends(get_analyzer),
    evaluator: EvaluationService = Depends(get_evaluation_service)
):
    """
    Quick evaluation using predefined test data.
    """
    test_data = await get_test_data()
    
    request = EvaluationRequest(
        cv_text=test_data["cv_text"],
        assignment_info=test_data["assignment_info"],
        consultant_name=test_data["consultant_name"],
        models=test_data["models"],
        reference_cover_letter=test_data["reference_cover_letter"]
    )
    
    return await evaluate_models(request, analyzer, evaluator)

@app.get("/available-models")
async def get_available_models():
    """Get list of available models for evaluation."""
    from src.config import config
    return {
        "available_models": config.all_available_models,
        "model_configs": {
            "openai_models": list(config.OPENAI_MODELS.keys()),
            "gemini_models": list(config.GEMINI_MODELS.keys()),
            "ollama_models": list(config.OLLAMA_MODELS.keys())
        }
    }

@app.post("/single-model-evaluation")
async def evaluate_single_model_endpoint(
    model_name: str,
    cv_text: str,
    assignment_description: str,
    consultant_name: str,
    reference_cover_letter: Optional[str] = None,
    analyzer: CVAnalyzer = Depends(get_analyzer),
    evaluator: EvaluationService = Depends(get_evaluation_service)
):
    """
    Evaluate a single model with custom inputs.
    """
    try:
        # Generate cover letter
        cover_letter = await analyzer.generate_cover_letter(
            cv_text,
            {"description": assignment_description},
            consultant_name,
            {},
            model_name=model_name
        )
        
        # Calculate metrics
        result = {
            "model_name": model_name,
            "cover_letter": cover_letter,
            "word_count": len(cover_letter.split()),
            "character_count": len(cover_letter)
        }
        
        if reference_cover_letter:
            result["bleu_score"] = await evaluator.calculate_bleu(reference_cover_letter, cover_letter)
        
        if cover_letter and not cover_letter.startswith("Error:"):
            result["perplexity"] = await evaluator.calculate_perplexity(cover_letter)
        else:
            result["perplexity"] = float('inf')
            
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "CV Analysis Evaluation API",
        "models_available": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "run_evaluation:app",  # Replace with your actual filename
        host="0.0.0.0",
        port=8001,  # Different port from main app
        reload=True,
        log_level="info"
    )
