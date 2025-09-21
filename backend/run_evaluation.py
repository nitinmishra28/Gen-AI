# # run_evaluation.py

# # It seems there's a typo in your directory name. Ensure this matches your actual folder.
# # If your folder is named 'services', change the import line accordingly.
# from src.serivces.analyzer import CVAnalyzer
# from src.serivces.evaluation_service import EvaluationService

# # --- SETUP ---
# # This initializes your classes that will call the LLMs and calculate scores.
# analyzer = CVAnalyzer()
# evaluator = EvaluationService()

# # 1. DEFINE YOUR TEST CASE
# # USE A REAL CV HERE: The text should be the content of a resume, not a cover letter.
# # Using triple quotes """ allows for clean, multi-line strings.
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

# # The job description for the role.
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
# # This is passed to the cover letter function but is empty for this test, which is fine.
# analysis_result = {}

# # 2. DEFINE YOUR "GOLDEN" REFERENCE OUTPUT
# # This is a high-quality example you've written yourself.
# # It should be a strong, concise cover letter for the CV and job description above.
# reference_cover_letter = """
# Dear Hiring Manager,

# I am writing to express my strong interest in the Software Developer position. My 1.5 years of experience as a Full-Stack Developer at BITTWOBYTE TECHNOLOGY has equipped me with a robust skill set in Python, Flask, and React, directly aligning with your job requirements.

# In my current role, I have designed and implemented secure back-end services, integrated complex third-party APIs like HubSpot, and optimized database queries to improve performance. These hands-on experiences make me confident that I can contribute effectively to your team from day one.

# I am passionate about building high-quality software and am eager to bring my technical skills and problem-solving abilities to your team. Thank you for your time and consideration.

# Sincerely,
# Jane Doe
# """

# # --- RUN EVALUATION ---
# print("Running evaluations for Cover Letter Generation...")

# # Generate cover letters using both models.
# cover_letter_gpt35 = analyzer.generate_cover_letter(
#     cv_text, assignment_info, consultant_name, analysis_result, model_name='gemma2:9b-instruct-q4_K_M'
# )

# cover_letter_gpt4 = analyzer.generate_cover_letter(
#     cv_text, assignment_info, consultant_name, analysis_result, model_name='gemma3:1b'
# )

# # --- CALCULATE SCORES ---
# # BLEU Scores (higher is better - measures similarity to your reference)
# bleu_gpt35 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_gpt35)
# bleu_gpt4 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_gpt4)

# # Perplexity Scores (lower is better - measures fluency and coherence)
# perplexity_gpt35 = evaluator.calculate_perplexity(cover_letter_gpt35)
# perplexity_gpt4 = evaluator.calculate_perplexity(cover_letter_gpt4)

# # --- PRINT REPORT ---
# # Use f-strings for clean, readable output.
# print("\n--- Evaluation Report ---")
# print(f"Model: gpt-3.5-turbo")
# print(f"  - BLEU Score: {bleu_gpt35:.4f}")
# print(f"  - Perplexity: {perplexity_gpt35:.2f}")

# print("\nGPT-3.5 Generated Letter:")
# print("-" * 30)
# print(cover_letter_gpt35)
# print("-" * 30)

# print(f"\nModel: gpt-4")
# print(f"  - BLEU Score: {bleu_gpt4:.4f}")
# print(f"  - Perplexity: {perplexity_gpt4:.2f}")

# print("\nGPT-4 Generated Letter:")
# print("-" * 30)
# print(cover_letter_gpt4)
# print("-" * 30)

# run_evaluation.py

# Make sure this import path matches your directory structure.
# If your folder is named 'services', change 'serivces' to 'services'.

# from src.serivces.analyzer import CVAnalyzer
# from src.serivces.evaluation_service import EvaluationService

# # --- SETUP ---
# # This initializes your classes that will call the LLMs and calculate scores.
# analyzer = CVAnalyzer()
# evaluator = EvaluationService()

# # 1. DEFINE YOUR TEST CASE
# # Using triple quotes """ allows for clean, multi-line strings.
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

# # The job description for the role.
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
# - Understanding of the software development lifecycle (SDDC) and Agile.
# - Experience with Git, database systems, and strong problem-solving skills.
# """
# }

# consultant_name = "Jane Doe"
# # This is passed to the cover letter function but is empty for this test, which is fine.
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
# print("Running evaluations for Cover Letter Generation using local Ollama models...")

# # Define the models you are testing
# model_1_name = 'gemma2:9b-instruct-q4_K_M'
# model_2_name = 'gemma3:1b' 
# model_3_name = 'gemini-pro-flash' 

# # Generate cover letters using your specified models.
# cover_letter_model_1 = analyzer.generate_cover_letter(
#     cv_text, assignment_info, consultant_name, analysis_result, model_name=model_1_name
# )

# cover_letter_model_2 = analyzer.generate_cover_letter(
#     cv_text, assignment_info, consultant_name, analysis_result, model_name=model_2_name
# )
# cover_letter_model_3 = analyzer.generate_cover_letter(cv_text, assignment_info, consultant_name, analysis_result, model_name=model_3_name) # NEW

# # --- CALCULATE SCORES ---
# # BLEU Scores (higher is better)
# bleu_model_1 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_1)
# bleu_model_2 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_2)
# bleu_model_3 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_3) # NEW


# # Perplexity Scores (lower is better)
# perplexity_model_1 = evaluator.calculate_perplexity(cover_letter_model_1)
# perplexity_model_2 = evaluator.calculate_perplexity(cover_letter_model_2)
# perplexity_model_3 = evaluator.calculate_perplexity(cover_letter_model_3)

# # --- PRINT REPORT ---
# # Use f-strings and the model name variables for a dynamic and accurate report.
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







from src.serivces.analyzer import CVAnalyzer
from src.serivces.evaluation_service import EvaluationService

# --- SETUP ---
analyzer = CVAnalyzer()
evaluator = EvaluationService()

# 1. DEFINE YOUR TEST CASE
cv_text = """
Jane Doe
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
- Tools: Git, Docker, Postman, HubSpot API, Jira
"""

assignment_info = {
    "description": """
Summary
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
- Experience with Git, database systems, and strong problem-solving skills.
"""
}

consultant_name = "Jane Doe"
analysis_result = {}

# 2. DEFINE YOUR "GOLDEN" REFERENCE OUTPUT
reference_cover_letter = """
Dear Hiring Manager,

I am writing to express my strong interest in the Software Developer position. My 1.5 years of experience as a Full-Stack Developer at BITTWOBYTE TECHNOLOGY has equipped me with a robust skill set in Python, Flask, and React, directly aligning with your job requirements.

In my current role, I have designed and implemented secure back-end services, integrated complex third-party APIs like HubSpot, and optimized database queries to improve performance. These hands-on experiences make me confident that I can contribute effectively to your team from day one.

I am passionate about building high-quality software and am eager to bring my technical skills and problem-solving abilities to your team. Thank you for your time and consideration.

Sincerely,
Jane Doe
"""

# --- RUN EVALUATION ---
print("Running evaluations for Cover Letter Generation using local Ollama models and Gemini...")

# Define the models you are testing
model_1_name = 'gemma2:9b-instruct-q4_K_M'
model_2_name = 'gemma3:1b'
model_3_name = 'gemini-1.5-flash'  # Updated to a valid Gemini model

# Generate cover letters using your specified models
try:
    cover_letter_model_1 = analyzer.generate_cover_letter(
        cv_text, assignment_info, consultant_name, analysis_result, model_name=model_1_name
    )
except Exception as e:
    print(f"Error generating cover letter for {model_1_name}: {e}")
    cover_letter_model_1 = "Error: Could not generate cover letter."

try:
    cover_letter_model_2 = analyzer.generate_cover_letter(
        cv_text, assignment_info, consultant_name, analysis_result, model_name=model_2_name
    )
except Exception as e:
    print(f"Error generating cover letter for {model_2_name}: {e}")
    cover_letter_model_2 = "Error: Could not generate cover letter."

try:
    cover_letter_model_3 = analyzer.generate_cover_letter(
        cv_text, assignment_info, consultant_name, analysis_result, model_name=model_3_name
    )
except Exception as e:
    print(f"Error generating cover letter for {model_3_name}: {e}")
    cover_letter_model_3 = "Error: Could not generate cover letter."

# --- CALCULATE SCORES ---
# BLEU Scores (higher is better)
bleu_model_1 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_1) if cover_letter_model_1.startswith("Dear") else 0.0
bleu_model_2 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_2) if cover_letter_model_2.startswith("Dear") else 0.0
bleu_model_3 = evaluator.calculate_bleu(reference_cover_letter, cover_letter_model_3) if cover_letter_model_3.startswith("Dear") else 0.0

# Perplexity Scores (lower is better)
perplexity_model_1 = evaluator.calculate_perplexity(cover_letter_model_1) if cover_letter_model_1.startswith("Dear") else float('inf')
perplexity_model_2 = evaluator.calculate_perplexity(cover_letter_model_2) if cover_letter_model_2.startswith("Dear") else float('inf')
perplexity_model_3 = evaluator.calculate_perplexity(cover_letter_model_3) if cover_letter_model_3.startswith("Dear") else float('inf')

# --- PRINT REPORT ---
print("\n--- Evaluation Report ---")
print(f"Model: {model_1_name}")
print(f"  - BLEU Score: {bleu_model_1:.4f}")
print(f"  - Perplexity: {perplexity_model_1:.2f}")
print(f"\nGenerated Letter ({model_1_name}):")
print("-" * 30)
print(cover_letter_model_1)
print("-" * 30)

print(f"\nModel: {model_2_name}")
print(f"  - BLEU Score: {bleu_model_2:.4f}")
print(f"  - Perplexity: {perplexity_model_2:.2f}")
print(f"\nGenerated Letter ({model_2_name}):")
print("-" * 30)
print(cover_letter_model_2)
print("-" * 30)

print(f"\nModel: {model_3_name}")
print(f"  - BLEU Score: {bleu_model_3:.4f}")
print(f"  - Perplexity: {perplexity_model_3:.2f}")
print(f"\nGenerated Letter ({model_3_name}):")
print("-" * 30)
print(cover_letter_model_3)
print("-" * 30)