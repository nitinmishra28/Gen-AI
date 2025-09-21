# # A centralized place for all prompts used in the application
# import json
# # --- Model-specific System Prompts ---
# SYSTEM_PROMPTS = {
#     'gpt-3.5-turbo': {
#         'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
#         Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
#         'skills': """You are a technical skills assessment expert.
#         Evaluate skills against job requirements and provide detailed matching analysis.""",
        
#         'experience': """You are an expert in evaluating professional experience.
#         Assess work history relevance and impact, focusing on concrete achievements.""",
        
#         'motivation': """You are skilled at writing compelling motivations for job applications.
#         Create engaging content that highlights candidate strengths.""",
        
#         'cover_letter': """You are a professional cover letter writer.
#         Create persuasive letters that effectively showcase candidate qualifications.""",
        
#         'summary': """You are an expert at creating professional summaries.
#         Craft concise, impactful overviews of candidate profiles."""
#     },
    
#     'gpt-4-turbo': {
#         'analyze': """You are a world-class HR analyst with deep expertise in technical recruitment and talent assessment.
#         Provide comprehensive CV analysis with detailed insights in the specified JSON format only.""",
        
#         'skills': """You are a senior technical skills evaluator with extensive industry knowledge.
#         Provide in-depth analysis of technical capabilities with specific examples.""",
        
#         'experience': """You are an expert in evaluating career trajectories and professional achievements.
#         Assess experience depth, progression, and impact with detailed context.""",
        
#         'motivation': """You are an expert at crafting compelling professional narratives.
#         Create highly personalized motivations that resonate with specific job requirements.""",
        
#         'cover_letter': """You are an expert career coach specializing in high-impact cover letters.
#         Create sophisticated, tailored letters that demonstrate deep understanding of the role.""",
        
#         'summary': """You are an expert in professional branding and career narratives.
#         Create compelling professional summaries that highlight unique value propositions."""
#     },
    
#     'gemini-1.5-flash': {
#         'analyze': """As an advanced HR analyst, provide thorough CV evaluation.
#         Return detailed analysis in the specified JSON format with clear insights.""",
        
#         'skills': """As a technical skills analyst, evaluate competencies comprehensively.
#         Focus on both technical depth and practical application.""",
        
#         'experience': """As an experience evaluation specialist, analyze career progression.
#         Focus on achievements, growth, and skill development.""",
        
#         'motivation': """As a professional content creator, craft engaging motivations.
#         Focus on alignment between candidate strengths and role requirements.""",
        
#         'cover_letter': """As a cover letter specialist, create impactful application letters.
#         Focus on clear value proposition and role alignment.""",
        
#         'summary': """As a professional profile expert, create effective summaries.
#         Focus on key achievements and unique qualifications."""
#     },
#     'gemma2:9b-instruct-q4_K_M': {
#         'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
#         Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
#         'skills': """You are a technical skills assessment expert.
#         Evaluate skills against job requirements and provide detailed matching analysis.""",
        
#         'experience': """You are an expert in evaluating professional experience.
#         Assess work history relevance and impact, focusing on concrete achievements.""",
        
#         'motivation': """You are skilled at writing compelling motivations for job applications.
#         Create engaging content that highlights candidate strengths.""",
        
#         'cover_letter': """You are a professional cover letter writer.
#         Create persuasive letters that effectively showcase candidate qualifications.""",
        
#         'summary': """You are an expert at creating professional summaries.
#         Craft concise, impactful overviews of candidate profiles."""
#     },
#     'gemma3:1b': {
#         'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
#         Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
#         'skills': """You are a technical skills assessment expert.
#         Evaluate skills against job requirements and provide detailed matching analysis.""",
        
#         'experience': """You are an expert in evaluating professional experience.
#         Assess work history relevance and impact, focusing on concrete achievements.""",
        
#         'motivation': """You are skilled at writing compelling motivations for job applications.
#         Create engaging content that highlights candidate strengths.""",
        
#         'cover_letter': """You are a professional cover letter writer.
#         Create persuasive letters that effectively showcase candidate qualifications.""",
        
#         'summary': """You are an expert at creating professional summaries.
#         Craft concise, impactful overviews of candidate profiles."""
#     },
# }

# def get_analyze_cv_prompt(cv_text: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for CV analysis."""
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['analyze'],
#         'user': f"""Analyze this CV against the requirements.

# REQUIREMENTS:
# {requirements}

# CV CONTENT:
# {cv_text}

# Return a single, valid JSON object using this exact format:
# {{
#     "overall_score": number,           # 0-100 overall match score
#     "requirements_score": number,      # 0-100 score for mandatory requirements
#     "wishes_score": number,           # 0-100 score for optional requirements
#     "requirements": [                  # Array of requirement matches
#         {{
#             "id": string,             # Unique identifier
#             "type": "require",        # Type is always "require" for requirements
#             "title": string,          # Short requirement description
#             "description": string,    # Full requirement text
#             "match": boolean,        # Whether requirement is met
#             "percentage": number,    # 0-100 match percentage
#             "explanation": string    # Evidence-based explanation
#         }}
#     ],
#     "wishes": [                      # Array of optional requirement matches
#         {{
#             "id": string,           # Unique identifier
#             "type": "wish",         # Type is always "wish" for optional items
#             "title": string,        # Short requirement description
#             "description": string,  # Full requirement text
#             "match": boolean,      # Whether requirement is met
#             "percentage": number,  # 0-100 match percentage
#             "explanation": string  # Evidence-based explanation
#         }}
#     ]
# }}"""
#     }

# def get_skills_analysis_prompt(skills_text: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for detailed skills analysis."""
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['skills'],
#         'user': f"""Analyze these technical skills against the requirements.

# REQUIRED SKILLS:
# {requirements}

# CANDIDATE SKILLS:
# {skills_text}

# Provide analysis in this JSON format:
# {{
#     "technical_skills": {{
#         "match_score": float,        # 0-1 score
#         "matching_skills": [str],    # Skills that match
#         "missing_skills": [str],     # Required skills not found
#         "additional_skills": [str]    # Extra relevant skills
#     }},
#     "recommendations": [str]         # Specific improvement suggestions
# }}"""
#     }

# def get_experience_analysis_prompt(experience: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for experience analysis."""
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['experience'],
#         'user': f"""Analyze this work experience against the job requirements.

# ROLE REQUIREMENTS:
# {requirements}

# WORK EXPERIENCE:
# {experience}

# Provide analysis in this JSON format:
# {{
#     "experience_match": {{
#         "score": float,              # 0-1 score
#         "years_relevant": float,     # Years of relevant experience
#         "key_achievements": [str],   # Relevant achievements
#         "missing_areas": [str]       # Required experience not found
#     }},
#     "recommendations": [str]         # Specific suggestions
# }}"""
#     }

# def get_motivation_prompt(cv_text: str, job_desc: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for motivation letter."""
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['motivation'],
#         'user': f"""Write a compelling motivation letter based on the CV and job description.

# JOB DESCRIPTION:
# {job_desc}

# CV CONTENT:
# {cv_text}

# Focus on:
# 1. Strong matches between requirements and experience
# 2. Relevant achievements and expertise
# 3. Specific examples from the CV
# 4. Growth potential and enthusiasm
# 5. Cultural fit and soft skills"""
#     }

# def get_cover_letter_prompt(cv_text: str, job_desc: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for cover letter."""
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['cover_letter'],
#         'user': f"""Create a professional cover letter based on the CV and job description.

# JOB DESCRIPTION:
# {job_desc}

# CV CONTENT:
# {cv_text}

# Include:
# 1. Strong opening that grabs attention
# 2. Specific examples of relevant experience
# 3. Clear connection to job requirements
# 4. Demonstration of company knowledge
# 5. Professional closing with call to action"""
#     }

# def get_customize_content_prompt(content_type: str, original_content: str, user_prompt: str, context: dict = None, model_name: str = None) -> dict:
#     """
#     Generates system and user prompts for customizing previously generated content.
#     """
#     system_prompt = (
#         "You are an expert editor and writer. Your task is to revise the provided text based on the user's instructions. "
#         "Pay close attention to the user's feedback and modify the text accordingly, maintaining a professional tone."
#     )

#     user_prompt_text = (
#         f"Please revise the following {content_type} based on my instructions.\n\n"
#         f"ORIGINAL {content_type.upper()}:\n"
#         f"'''\n{original_content}\n'''\n\n"
#         f"USER INSTRUCTIONS:\n"
#         f"'''\n{user_prompt}\n'''\n\n"
#         "Generate the revised text directly, without adding any extra commentary or conversational text."
#     )
    
#     if context:
#         user_prompt_text += f"\n\nADDITIONAL CONTEXT:\n{json.dumps(context, indent=2)}"

#     return {"system": system_prompt, "user": user_prompt_text}

# def get_summary_prompt(cv_text: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for professional summary."""
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['summary'],
#         'user': f"""Create a professional summary based on this CV.

# CV CONTENT:
# {cv_text}

# Create a concise summary that:
# 1. Highlights years of relevant experience
# 2. Emphasizes key technical skills
# 3. Mentions significant achievements
# 4. Shows career progression
# 5. Includes relevant certifications/education

# Keep it under 200 words and focus on unique value proposition."""
#     }

















# # A centralized place for all prompts used in the application
# import json

# # --- Model-specific System Prompts ---
# SYSTEM_PROMPTS = {
#     'gpt-3.5-turbo': {
#         'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
#         Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
#         'skills': """You are a technical skills assessment expert.
#         Evaluate skills against job requirements and provide detailed matching analysis.""",
        
#         'experience': """You are an expert in evaluating professional experience.
#         Assess work history relevance and impact, focusing on concrete achievements.""",
        
#         'motivation': """You are skilled at writing compelling motivations for job applications.
#         Create engaging content that highlights candidate strengths. Do not ask for more information.""",
        
#         'cover_letter': """You are a professional cover letter writer.
#         Create persuasive letters that effectively showcase candidate qualifications.""",
        
#         'summary': """You are an expert at creating professional summaries.
#         Craft concise, impactful overviews of candidate profiles."""
#     },
    
#     'gpt-4': {
#         'analyze': """You are a world-class HR analyst with deep expertise in technical recruitment and talent assessment.
#         Provide comprehensive CV analysis with detailed insights in the specified JSON format only.""",
        
#         'skills': """You are a senior technical skills evaluator with extensive industry knowledge.
#         Provide in-depth analysis of technical capabilities with specific examples.""",
        
#         'experience': """You are an expert in evaluating career trajectories and professional achievements.
#         Assess experience depth, progression, and impact with detailed context.""",
        
#         'motivation': """You are an expert at crafting compelling professional narratives.
#         Create highly personalized motivations that resonate with specific job requirements. Do not ask for more information.""",
        
#         'cover_letter': """You are an expert career coach specializing in high-impact cover letters.
#         Create sophisticated, tailored letters that demonstrate deep understanding of the role.""",
        
#         'summary': """You are an expert in professional branding and career narratives.
#         Create compelling professional summaries that highlight unique value propositions."""
#     },
    
#     'gpt-4-turbo': {
#         'analyze': """You are a world-class HR analyst with deep expertise in technical recruitment and talent assessment.
#         Provide comprehensive CV analysis with detailed insights in the specified JSON format only.""",
        
#         'skills': """You are a senior technical skills evaluator with extensive industry knowledge.
#         Provide in-depth analysis of technical capabilities with specific examples.""",
        
#         'experience': """You are an expert in evaluating career trajectories and professional achievements.
#         Assess experience depth, progression, and impact with detailed context.""",
        
#         'motivation': """You are an expert at crafting compelling professional narratives.
#         Create highly personalized motivations that resonate with specific job requirements. Do not ask for more information.""",
        
#         'cover_letter': """You are an expert career coach specializing in high-impact cover letters.
#         Create sophisticated, tailored letters that demonstrate deep understanding of the role.""",
        
#         'summary': """You are an expert in professional branding and career narratives.
#         Create compelling professional summaries that highlight unique value propositions."""
#     },
    
#     'gemini-1.5-flash': {
#         'analyze': """As an advanced HR analyst, provide thorough CV evaluation.
#         Return detailed analysis in the specified JSON format with clear insights.""",
        
#         'skills': """As a technical skills analyst, evaluate competencies comprehensively.
#         Focus on both technical depth and practical application.""",
        
#         'experience': """As an experience evaluation specialist, analyze career progression.
#         Focus on achievements, growth, and skill development.""",
        
#         'motivation': """As a professional content creator, craft engaging motivations.
#         Focus on alignment between candidate strengths and role requirements. Do not ask for more information.""",
        
#         'cover_letter': """As a cover letter specialist, create impactful application letters.
#         Focus on clear value proposition and role alignment.""",
        
#         'summary': """As a professional profile expert, create effective summaries.
#         Focus on key achievements and unique qualifications."""
#     },
    
#     'gemini-1.5-pro': {
#         'analyze': """As an advanced HR analyst, provide thorough CV evaluation.
#         Return detailed analysis in the specified JSON format with clear insights.""",
        
#         'skills': """As a technical skills analyst, evaluate competencies comprehensively.
#         Focus on both technical depth and practical application.""",
        
#         'experience': """As an experience evaluation specialist, analyze career progression.
#         Focus on achievements, growth, and skill development.""",
        
#         'motivation': """As a professional content creator, craft engaging motivations.
#         Focus on alignment between candidate strengths and role requirements. Do not ask for more information.""",
        
#         'cover_letter': """As a cover letter specialist, create impactful application letters.
#         Focus on clear value proposition and role alignment.""",
        
#         'summary': """As a professional profile expert, create effective summaries.
#         Focus on key achievements and unique qualifications."""
#     },
    
#     'gemma2:9b-instruct-q4_K_M': {
#         'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
#         Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
#         'skills': """You are a technical skills assessment expert.
#         Evaluate skills against job requirements and provide detailed matching analysis.""",
        
#         'experience': """You are an expert in evaluating professional experience.
#         Assess work history relevance and impact, focusing on concrete achievements.""",
        
#         'motivation': """You are skilled at writing compelling motivations for job applications.
#         Create engaging content that highlights candidate strengths. Do not ask for more information.""",
        
#         'cover_letter': """You are a professional cover letter writer.
#         Create persuasive letters that effectively showcase candidate qualifications.""",
        
#         'summary': """You are an expert at creating professional summaries.
#         Craft concise, impactful overviews of candidate profiles."""
#     },
    
#     'gemma3:1b': {
#         'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
#         Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
#         'skills': """You are a technical skills assessment expert.
#         Evaluate skills against job requirements and provide detailed matching analysis.""",
        
#         'experience': """You are an expert in evaluating professional experience.
#         Assess work history relevance and impact, focusing on concrete achievements.""",
        
#         'motivation': """You are skilled at writing compelling motivations for job applications.
#         Create engaging content that highlights candidate strengths. Do not ask for more information.""",
        
#         'cover_letter': """You are a professional cover letter writer.
#         Create persuasive letters that effectively showcase candidate qualifications.""",
        
#         'summary': """You are an expert at creating professional summaries.
#         Craft concise, impactful overviews of candidate profiles."""
#     },
    
#     'llama3': {
#         'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
#         Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
#         'skills': """You are a technical skills assessment expert.
#         Evaluate skills against job requirements and provide detailed matching analysis.""",
        
#         'experience': """You are an expert in evaluating professional experience.
#         Assess work history relevance and impact, focusing on concrete achievements.""",
        
#         'motivation': """You are skilled at writing compelling motivations for job applications.
#         Create engaging content that highlights candidate strengths. Do not ask for more information.""",
        
#         'cover_letter': """You are a professional cover letter writer.
#         Create persuasive letters that effectively showcase candidate qualifications.""",
        
#         'summary': """You are an expert at creating professional summaries.
#         Craft concise, impactful overviews of candidate profiles."""
#     },
# }

# def get_analyze_cv_prompt(cv_text: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for CV analysis."""
    
#     # Add fallback for unknown models
#     if model_name not in SYSTEM_PROMPTS:
#         logger.warning(f"Model '{model_name}' not found in SYSTEM_PROMPTS, using gpt-3.5-turbo as fallback")
#         model_name = 'gpt-3.5-turbo'
    
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['analyze'],
#         'user': f"""Analyze this CV against the requirements.

# REQUIREMENTS:
# {requirements}

# CV CONTENT:
# {cv_text}

# Return a single, valid JSON object using this exact format:
# {{
#     "overall_score": number,           # 0-100 overall match score
#     "requirements_score": number,      # 0-100 score for mandatory requirements
#     "wishes_score": number,           # 0-100 score for optional requirements
#     "requirements": [                  # Array of requirement matches
#         {{
#             "id": string,             # Unique identifier
#             "type": "require",        # Type is always "require" for requirements
#             "title": string,          # Short requirement description
#             "description": string,    # Full requirement text
#             "match": boolean,        # Whether requirement is met
#             "percentage": number,    # 0-100 match percentage
#             "explanation": string    # Evidence-based explanation
#         }}
#     ],
#     "wishes": [                      # Array of optional requirement matches
#         {{
#             "id": string,           # Unique identifier
#             "type": "wish",         # Type is always "wish" for optional items
#             "title": string,        # Short requirement description
#             "description": string,  # Full requirement text
#             "match": boolean,      # Whether requirement is met
#             "percentage": number,  # 0-100 match percentage
#             "explanation": string  # Evidence-based explanation
#         }}
#     ]
# }}"""
#     }

# def get_skills_analysis_prompt(skills_text: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for detailed skills analysis."""
#     if model_name not in SYSTEM_PROMPTS:
#         model_name = 'gpt-3.5-turbo'
        
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['skills'],
#         'user': f"""Analyze these technical skills against the requirements.

# REQUIRED SKILLS:
# {requirements}

# CANDIDATE SKILLS:
# {skills_text}

# Provide analysis in this JSON format:
# {{
#     "technical_skills": {{
#         "match_score": float,        # 0-1 score
#         "matching_skills": [str],    # Skills that match
#         "missing_skills": [str],     # Required skills not found
#         "additional_skills": [str]    # Extra relevant skills
#     }},
#     "recommendations": [str]         # Specific improvement suggestions
# }}"""
#     }

# def get_experience_analysis_prompt(experience: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for experience analysis."""
#     if model_name not in SYSTEM_PROMPTS:
#         model_name = 'gpt-3.5-turbo'
        
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['experience'],
#         'user': f"""Analyze this work experience against the job requirements.

# ROLE REQUIREMENTS:
# {requirements}

# WORK EXPERIENCE:
# {experience}

# Provide analysis in this JSON format:
# {{
#     "experience_match": {{
#         "score": float,              # 0-1 score
#         "years_relevant": float,     # Years of relevant experience
#         "key_achievements": [str],   # Relevant achievements
#         "missing_areas": [str]       # Required experience not found
#     }},
#     "recommendations": [str]         # Specific suggestions
# }}"""
#     }

# def get_motivation_prompt(cv_text: str, job_desc: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for motivation letter."""
#     if model_name not in SYSTEM_PROMPTS:
#         model_name = 'gpt-3.5-turbo'
        
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['motivation'],
#         'user': f"""Write a compelling motivation based on the CV content provided. Do not ask for more information.

# CV CONTENT:
# {cv_text}

# JOB DESCRIPTION:
# {job_desc}

# Focus on:
# 1. Strong matches between requirements and experience
# 2. Relevant achievements and expertise from the CV
# 3. Specific examples from the provided CV
# 4. Growth potential and enthusiasm
# 5. Cultural fit and soft skills

# Generate the motivation directly without asking for additional details."""
#     }
    
    
    
# def get_cover_letter_prompt(
#     cv_text: str,
#     job_desc: str,
#     model_name: str = "gpt-3.5-turbo",
#     tone: str = "professional and engaging",
#     word_limit: int = 300
# ) -> dict:
#     """
#     Generate optimized prompts for high-impact cover letters across all domains.
#     """
#     if model_name not in SYSTEM_PROMPTS:
#         model_name = "gpt-3.5-turbo"

#     return {
#         "system": (
#             "You are an expert career coach and recruiter with experience across multiple industries. "
#             f"Create a compelling, {tone} cover letter under {word_limit} words that demonstrates clear value proposition. "
#             "Focus on quantifiable achievements, relevant skills, and specific alignment with role requirements. "
#             "Adapt language and examples based on the industry context from the job description. "
#             "Return only the polished cover letter text without any meta-commentary, explanations, or formatting markers."
#         ),
#         "user": f"""
# Create a targeted cover letter using the provided CV and job description.

# JOB DESCRIPTION:
# {job_desc}

# CV CONTENT:
# {cv_text}

# REQUIREMENTS:
# 1. Hook: Open with a specific connection to the company/role, not generic interest
# 2. Value Proposition: Lead with your strongest, most relevant achievement with concrete results/metrics
# 3. Skills Alignment: Map 2-3 key CV experiences directly to job requirements using industry-appropriate terminology
# 4. Problem-Solving Evidence: Include a brief example of overcoming a relevant challenge or achieving significant results
# 5. Company Research: Reference specific company aspects, values, or recent developments if identifiable from context
# 6. Strong Close: Confident call-to-action that suggests next steps

# OPTIMIZATION GUIDELINES:
# - Use action verbs appropriate to the industry (achieved, increased, managed, developed, negotiated, etc.)
# - Include specific metrics, percentages, dollar amounts, or scale indicators relevant to the field
# - Avoid generic phrases and tailor language to industry norms
# - Demonstrate understanding of role-specific challenges and requirements
# - Show career progression and growth in responsibilities
# - Match the communication style expected in the target industry

# Output the complete cover letter ready for submission.
# """
#     }


# def get_customize_content_prompt(content_type: str, original_content: str, user_prompt: str, context: dict = None, model_name: str = None) -> dict:
#     """
#     Generates system and user prompts for customizing previously generated content.
#     """
#     system_prompt = (
#         "You are an expert editor and writer. Your task is to revise the provided text based on the user's instructions. "
#         "Pay close attention to the user's feedback and modify the text accordingly, maintaining a professional tone. "
#         "Do not ask for more information - work with what is provided."
#     )

#     user_prompt_text = (
#         f"Please revise the following {content_type} based on my instructions.\n\n"
#         f"ORIGINAL {content_type.upper()}:\n"
#         f"'''\n{original_content}\n'''\n\n"
#         f"USER INSTRUCTIONS:\n"
#         f"'''\n{user_prompt}\n'''\n\n"
#         "Generate the revised text directly, without adding any extra commentary or conversational text."
#     )
    
#     if context:
#         user_prompt_text += f"\n\nADDITIONAL CONTEXT:\n{json.dumps(context, indent=2)}"

#     return {"system": system_prompt, "user": user_prompt_text}

# def get_summary_prompt(cv_text: str, model_name: str = 'gpt-3.5-turbo') -> dict:
#     """Generate prompts for professional summary."""
#     if model_name not in SYSTEM_PROMPTS:
#         model_name = 'gpt-3.5-turbo'
        
#     return {
#         'system': SYSTEM_PROMPTS[model_name]['summary'],
#         'user': f"""Create a professional summary based on this CV. Do not ask for more information.

# CV CONTENT:
# {cv_text}

# Create a concise summary that:
# 1. Highlights years of relevant experience
# 2. Emphasizes key technical skills
# 3. Mentions significant achievements
# 4. Shows career progression
# 5. Includes relevant certifications/education

# Keep it under 200 words and focus on unique value proposition. Generate the summary directly using the provided CV content."""
#     }




# A centralized place for all prompts used in the application
# A centralized place for all prompts used in the application
import json
import logging

logger = logging.getLogger(__name__)

# --- Model-specific System Prompts ---
SYSTEM_PROMPTS = {
    'gpt-3.5-turbo': {
        'analyze': """You are a world-class HR analyst with expertise in technical recruitment. 
        CRITICAL: Follow ALL instructions exactly. Analyze CVs objectively and return ONLY structured feedback in the specified JSON format. 
        Double-check JSON validity before responding.""",
        
        'skills': """You are a senior technical skills assessment expert with 15+ years of industry experience.
        MUST: Evaluate skills against job requirements with precision and provide comprehensive matching analysis with specific evidence.""",
        
        'experience': """You are an expert in evaluating professional experience with deep understanding of career trajectories.
        REQUIRED: Assess work history relevance and quantifiable impact, focusing exclusively on concrete, measurable achievements.""",
        
        'motivation': """You are a master at crafting compelling motivations for job applications with proven success records.
        STRICT REQUIREMENT: Create engaging, specific content highlighting candidate strengths. Maximum 3 sentences. NO generic phrases.""",
        
        'cover_letter': """You are an expert career coach and recruiter with experience across multiple industries and proven track record.
        MANDATORY: Create compelling cover letters demonstrating clear value proposition across all domains. Focus on quantifiable achievements and industry-specific language.""",
        
        'introduction_email': """You are an expert at writing professional introduction emails with 95%+ success rate in candidate placements.
        CRITICAL: Create concise, engaging emails that effectively present candidates to potential employers with measurable impact statements.""",
        
        'summary': """You are an expert at creating professional summaries that increase interview callbacks by 300%.
        REQUIRED: Craft concise, impactful overviews focusing on unique value propositions and quantifiable achievements."""
    },
    
    'gpt-4': {
        'analyze': """You are a world-class HR analyst with deep expertise in technical recruitment and talent assessment across Fortune 500 companies.
        CRITICAL: Provide comprehensive CV analysis with detailed, evidence-based insights in the specified JSON format ONLY. Validate JSON structure before output.""",
        
        'skills': """You are a senior technical skills evaluator with extensive industry knowledge spanning 20+ years and multiple technology stacks.
        MANDATORY: Provide in-depth analysis of technical capabilities with specific, concrete examples and measurable proficiency indicators.""",
        
        'experience': """You are an expert in evaluating career trajectories and professional achievements with deep understanding of industry standards.
        REQUIRED: Assess experience depth, progression, and quantifiable impact with detailed context and benchmark comparisons.""",
        
        'motivation': """You are an expert at crafting compelling professional narratives that resonate with hiring managers and increase success rates by 85%.
        STRICT: Create highly personalized motivations with specific job requirement alignment. Maximum 3 sentences. NO asking for information.""",
        
        'cover_letter': """You are an expert career coach specializing in high-impact cover letters across all industries with documented success rates.
        CRITICAL: Create sophisticated, tailored letters demonstrating deep understanding of role requirements and industry context with measurable achievements.""",
        
        'introduction_email': """You are an expert at crafting professional introduction communications with proven effectiveness in executive placements.
        MANDATORY: Create compelling, industry-appropriate emails with specific value propositions and quantifiable candidate achievements.""",
        
        'summary': """You are an expert in professional branding and career narratives with expertise in C-level positioning.
        REQUIRED: Create compelling professional summaries highlighting unique value propositions with specific, measurable accomplishments."""
    },
    
    'gpt-4-turbo': {
        'analyze': """You are a world-class HR analyst with deep expertise in technical recruitment and talent assessment across global organizations.
        CRITICAL: Provide comprehensive CV analysis with detailed, evidence-based insights in the specified JSON format ONLY. Validate JSON structure before output.""",
        
        'skills': """You are a senior technical skills evaluator with extensive industry knowledge and expertise in emerging technologies.
        MANDATORY: Provide in-depth analysis of technical capabilities with specific examples and quantifiable proficiency metrics.""",
        
        'experience': """You are an expert in evaluating career trajectories with deep understanding of professional achievement patterns.
        REQUIRED: Assess experience depth, progression, and measurable impact with detailed context and industry benchmarks.""",
        
        'motivation': """You are an expert at crafting compelling professional narratives with proven success in competitive markets.
        STRICT: Create highly personalized motivations with specific alignment evidence. Maximum 3 sentences. NO generic statements.""",
        
        'cover_letter': """You are an expert career coach specializing in high-impact cover letters with documented placement success across industries.
        CRITICAL: Create sophisticated, tailored letters with deep role understanding and quantifiable achievement focus.""",
        
        'introduction_email': """You are an expert at crafting professional introduction communications with measurable placement success.
        MANDATORY: Create compelling emails with specific value propositions and concrete candidate achievements.""",
        
        'summary': """You are an expert in professional branding with expertise in executive-level positioning and market differentiation.
        REQUIRED: Create compelling summaries with unique value propositions and specific, quantifiable accomplishments."""
    },
    
    'gemini-1.5-flash': {
        'analyze': """As an advanced HR analyst with proven expertise, provide thorough CV evaluation with precision.
        CRITICAL: Return detailed analysis in the specified JSON format with clear, evidence-based insights. Verify JSON validity.""",
        
        'skills': """As a technical skills analyst with comprehensive industry knowledge, evaluate competencies with precision.
        REQUIRED: Focus on technical depth, practical application, and measurable proficiency indicators.""",
        
        'experience': """As an experience evaluation specialist with deep market understanding, analyze career progression systematically.
        MANDATORY: Focus on quantifiable achievements, growth trajectory, and skill development with specific evidence.""",
        
        'motivation': """As a professional content creator with proven success rates, craft engaging motivations with precision.
        STRICT: Focus on specific alignment between candidate strengths and role requirements. Maximum 3 sentences.""",
        
        'cover_letter': """As a cover letter specialist with documented success across industries, create impactful application letters.
        CRITICAL: Focus on clear value proposition and role alignment with industry-appropriate language and metrics.""",
        
        'introduction_email': """As a professional communication expert with measurable placement success, create effective introduction emails.
        REQUIRED: Focus on candidate strengths and role alignment in concise, professional format with specific achievements.""",
        
        'summary': """As a professional profile expert with expertise in personal branding, create effective summaries.
        MANDATORY: Focus on key achievements, unique qualifications, and quantifiable value propositions."""
    },
    
    'gemini-1.5-pro': {
        'analyze': """As an advanced HR analyst with comprehensive expertise, provide thorough CV evaluation with analytical precision.
        CRITICAL: Return detailed analysis in the specified JSON format with clear, evidence-based insights. Validate JSON structure.""",
        
        'skills': """As a technical skills analyst with extensive industry knowledge, evaluate competencies comprehensively.
        REQUIRED: Focus on technical depth, practical application, and specific proficiency measurements.""",
        
        'experience': """As an experience evaluation specialist with market expertise, analyze career progression systematically.
        MANDATORY: Focus on achievements, growth patterns, and skill development with quantifiable evidence.""",
        
        'motivation': """As a professional content creator with proven effectiveness, craft engaging motivations with precision.
        STRICT: Focus on specific alignment between candidate strengths and requirements. Maximum 3 sentences. NO generic content.""",
        
        'cover_letter': """As a cover letter specialist with cross-industry success, create impactful application letters.
        CRITICAL: Focus on clear value proposition and role alignment with appropriate language and measurable achievements.""",
        
        'introduction_email': """As a professional communication expert with documented success, create effective introduction emails.
        REQUIRED: Focus on candidate strengths and role alignment with specific, quantifiable accomplishments.""",
        
        'summary': """As a professional profile expert with branding expertise, create effective summaries.
        MANDATORY: Focus on key achievements, unique qualifications, and specific value propositions."""
    },
    
    'gemma2:9b-instruct-q4_K_M': {
        'analyze': """You are a proficient HR analyst with expertise in technical recruitment and proven assessment accuracy.
        CRITICAL: Analyze CVs objectively and return ONLY structured feedback in the specified JSON format. Verify JSON validity.""",
        
        'skills': """You are a technical skills assessment expert with comprehensive evaluation methodologies.
        REQUIRED: Evaluate skills against job requirements with detailed matching analysis and specific evidence.""",
        
        'experience': """You are an expert in evaluating professional experience with focus on measurable outcomes.
        MANDATORY: Assess work history relevance and quantifiable impact, focusing on concrete achievements with metrics.""",
        
        'motivation': """You are skilled at writing compelling motivations with proven success in job applications.
        STRICT: Create engaging content highlighting specific candidate strengths. Maximum 3 sentences. NO generic phrases.""",
        
        'cover_letter': """You are a professional cover letter writer with cross-industry experience and documented success.
        CRITICAL: Create persuasive letters showcasing candidate qualifications with industry-specific language and achievements.""",
        
        'introduction_email': """You are skilled at writing professional introduction emails with measurable placement success.
        REQUIRED: Create clear, compelling introductions highlighting specific candidate value propositions.""",
        
        'summary': """You are an expert at creating professional summaries that increase interview success rates.
        MANDATORY: Craft concise, impactful overviews with unique value propositions and quantifiable achievements."""
    },
    
    'gemma3:1b': {
        'analyze': """You are a proficient HR analyst with expertise in technical recruitment and systematic evaluation methods.
        CRITICAL: Analyze CVs objectively and return structured feedback in the specified JSON format only. Validate output.""",
        
        'skills': """You are a technical skills assessment expert with comprehensive analytical frameworks.
        REQUIRED: Evaluate skills against requirements with detailed matching analysis and specific supporting evidence.""",
        
        'experience': """You are an expert in evaluating professional experience with focus on measurable impact assessment.
        MANDATORY: Assess work history relevance focusing on concrete, quantifiable achievements with industry context.""",
        
        'motivation': """You are skilled at writing compelling motivations with proven effectiveness in competitive markets.
        STRICT: Create engaging content with specific candidate strength alignment. Maximum 3 sentences. NO generic statements.""",
        
        'cover_letter': """You are a professional cover letter writer with cross-industry expertise and success metrics.
        CRITICAL: Create persuasive letters with effective candidate qualification presentation and measurable achievements.""",
        
        'introduction_email': """You are skilled at writing professional introduction emails with documented effectiveness.
        REQUIRED: Create clear, compelling introductions with specific candidate value propositions and achievements.""",
        
        'summary': """You are an expert at creating professional summaries with proven impact on hiring success.
        MANDATORY: Craft concise, impactful overviews with unique value propositions and specific accomplishments."""
    },
    
    'llama3': {
        'analyze': """You are a proficient HR analyst with expertise in technical recruitment and evidence-based assessment.
        CRITICAL: Analyze CVs objectively and return structured feedback in the specified JSON format only. Verify JSON structure.""",
        
        'skills': """You are a technical skills assessment expert with systematic evaluation approaches.
        REQUIRED: Evaluate skills against job requirements with comprehensive matching analysis and concrete evidence.""",
        
        'experience': """You are an expert in evaluating professional experience with emphasis on quantifiable outcome assessment.
        MANDATORY: Assess work history relevance and measurable impact, focusing on specific, concrete achievements.""",
        
        'motivation': """You are skilled at writing compelling motivations with documented success in application processes.
        STRICT: Create engaging content highlighting candidate strengths with specific alignment. Maximum 3 sentences.""",
        
        'cover_letter': """You are a professional cover letter writer with cross-industry experience and proven results.
        CRITICAL: Create persuasive letters effectively showcasing candidate qualifications with industry-appropriate metrics.""",
        
        'introduction_email': """You are skilled at writing professional introduction emails with measurable success rates.
        REQUIRED: Create clear, compelling introductions highlighting candidate value propositions with specific achievements.""",
        
        'summary': """You are an expert at creating professional summaries with proven effectiveness in hiring processes.
        MANDATORY: Craft concise, impactful overviews with unique value propositions and quantifiable accomplishments."""
    },
}

def get_analyze_cv_prompt(cv_text: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate optimized prompts for CV analysis with enhanced precision."""
    
    if model_name not in SYSTEM_PROMPTS:
        logger.warning(f"Model '{model_name}' not found in SYSTEM_PROMPTS, using gpt-3.5-turbo as fallback")
        model_name = 'gpt-3.5-turbo'
    
    return {
        'system': SYSTEM_PROMPTS[model_name]['analyze'],
        'user': f"""TASK: Analyze this CV against the requirements with precision and evidence-based assessment.

REQUIREMENTS:
{requirements}

CV CONTENT:
{cv_text}

CRITICAL INSTRUCTIONS:
1. Analyze each requirement individually with specific evidence from the CV
2. Provide percentage scores based on concrete skill/experience matches
3. Include specific examples from CV content in explanations
4. Distinguish clearly between mandatory requirements and optional wishes
5. Return ONLY valid JSON - no additional text or formatting

MANDATORY OUTPUT FORMAT (validate before responding):
{{
    "overall_score": number,           # 0-100 weighted average of requirements and wishes
    "requirements_score": number,      # 0-100 score for mandatory requirements only
    "wishes_score": number,           # 0-100 score for optional requirements only
    "requirements": [                  # Array of mandatory requirement matches
        {{
            "id": "req_[sequential_number]",  # e.g., "req_1", "req_2"
            "type": "require",        # Always "require" for mandatory items
            "title": string,          # Concise requirement title (max 50 chars)
            "description": string,    # Full requirement description
            "match": boolean,        # True if requirement is met (>60% match)
            "percentage": number,    # 0-100 precise match percentage
            "explanation": string    # Specific evidence from CV supporting the score
        }}
    ],
    "wishes": [                      # Array of optional requirement matches
        {{
            "id": "wish_[sequential_number]", # e.g., "wish_1", "wish_2"
            "type": "wish",         # Always "wish" for optional items
            "title": string,        # Concise wish title (max 50 chars)
            "description": string,  # Full wish description
            "match": boolean,      # True if wish is met (>40% match)
            "percentage": number,  # 0-100 precise match percentage
            "explanation": string  # Specific evidence from CV supporting the score
        }}
    ]
}}

VALIDATION CHECKLIST:
- JSON is valid and parseable
- All required fields present
- Scores are realistic numbers 0-100
- Explanations contain specific CV evidence
- IDs follow the specified format"""
    }

def get_skills_analysis_prompt(skills_text: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate optimized prompts for detailed skills analysis."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = 'gpt-3.5-turbo'
        
    return {
        'system': SYSTEM_PROMPTS[model_name]['skills'],
        'user': f"""TASK: Analyze technical skills against requirements with precision and quantifiable assessment.

REQUIRED SKILLS:
{requirements}

CANDIDATE SKILLS:
{skills_text}

CRITICAL INSTRUCTIONS:
1. Match skills exactly - consider synonyms and related technologies
2. Provide specific proficiency evidence where available
3. Identify skill gaps with actionable recommendations
4. Include emerging/additional skills that add value

MANDATORY JSON OUTPUT (validate structure):
{{
    "technical_skills": {{
        "match_score": float,        # 0.0-1.0 precise match ratio
        "matching_skills": [str],    # Exact skills that match requirements
        "missing_skills": [str],     # Required skills not found or insufficient
        "additional_skills": [str],  # Extra relevant skills adding value
        "proficiency_indicators": [str] # Evidence of skill depth/experience
    }},
    "recommendations": [str]         # Specific, actionable improvement suggestions
}}

VALIDATION: Ensure JSON is valid and match_score is realistic based on analysis."""
    }

def get_experience_analysis_prompt(experience: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate optimized prompts for experience analysis."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = 'gpt-3.5-turbo'
        
    return {
        'system': SYSTEM_PROMPTS[model_name]['experience'],
        'user': f"""TASK: Analyze work experience against job requirements with quantifiable metrics and evidence.

ROLE REQUIREMENTS:
{requirements}

WORK EXPERIENCE:
{experience}

CRITICAL INSTRUCTIONS:
1. Calculate relevant experience years precisely
2. Identify key achievements with measurable impact
3. Assess experience depth and progression
4. Highlight gaps requiring attention

MANDATORY JSON OUTPUT (validate structure):
{{
    "experience_match": {{
        "score": float,              # 0.0-1.0 precise experience alignment
        "years_relevant": float,     # Exact years of directly relevant experience
        "years_total": float,        # Total professional experience years
        "key_achievements": [str],   # Specific, quantifiable accomplishments
        "missing_areas": [str],      # Required experience not demonstrated
        "progression_indicators": [str] # Evidence of career growth/advancement
    }},
    "recommendations": [str]         # Specific suggestions for experience enhancement
}}

VALIDATION: Verify all numerical values are realistic and supported by evidence."""
    }

def get_motivation_prompt(cv_text: str, requirement_title: str, requirement_details: dict = None, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate optimized prompts for compelling individual requirement motivations."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = 'gpt-3.5-turbo'
        
    return {
        'system': SYSTEM_PROMPTS[model_name]['motivation'],
        'user': f"""TASK: Write a compelling, evidence-based motivation for the specific requirement using CV content.

REQUIREMENT FOCUS: "{requirement_title}"

CV CONTENT:
{cv_text}

REQUIREMENT DETAILS:
- Title: {requirement_title}
- Description: {requirement_details.get('description', requirement_title) if requirement_details else requirement_title}
- Current Match: {requirement_details.get('percentage', 0) if requirement_details else 0}%

CRITICAL REQUIREMENTS:
1. MAXIMUM 3 sentences
2. Include specific examples/achievements from CV
3. Use confident, professional tone
4. Demonstrate clear alignment with requirement
5. Include quantifiable results where possible

FORBIDDEN:
- Generic phrases like "I believe" or "I think"
- Asking for more information
- Vague statements without CV evidence
- Exceeding 3 sentences

EXAMPLE STRUCTURE:
"With [X years/specific experience] in [relevant area from CV], I directly align with your [requirement]. My experience [specific achievement/project from CV] demonstrates [relevant capability/result]. This background positions me to [value proposition for this requirement]."

Generate the motivation now using ONLY the provided CV content."""
    }
    
def get_cover_letter_prompt(
    cv_text: str,
    job_desc: str,
    model_name: str = "gpt-3.5-turbo",
    tone: str = "professional and engaging",
    word_limit: int = 300,
    consultant_name: str = "the candidate"
) -> dict:
    """Generate highly optimized prompts for accurate, credible cover letters across all domains."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = "gpt-3.5-turbo"

    return {
        "system": SYSTEM_PROMPTS[model_name]['cover_letter'] + f" CRITICAL: Create compelling, {tone} cover letter UNDER {word_limit} words using ONLY verified CV information. ABSOLUTE REQUIREMENT: NO fabrication, exaggeration, or inflation of achievements, experience duration, or capabilities.",
        "user": f"""TASK: Write a professional cover letter for {consultant_name} with VERIFIED achievements and ACCURATE experience representation.

CANDIDATE CV CONTENT (USE ONLY THIS DATA):
{cv_text}

JOB DESCRIPTION:
{job_desc}

CRITICAL ACCURACY REQUIREMENTS:
- MAXIMUM {word_limit} words - count precisely and stop at limit
- Use ONLY achievements/metrics that exist in the CV content
- Match experience duration EXACTLY as stated in CV
- NO fabrication of percentages, improvements, or results
- Base ALL claims on verifiable CV information
- Calibrate language to actual experience level

MANDATORY STRUCTURE:
[Your Name]
[Complete Professional Address]  
[Phone] | [Email] | [LinkedIn]

[Current Date]

[Hiring Manager]
[Company Name]
[Company Address]

Dear Hiring Manager,

PARAGRAPH 1 (Authentic Hook): Connect to company/role using ACTUAL experience from CV - no inflated claims
PARAGRAPH 2 (Verified Value): Strongest REAL accomplishment from CV with context of experience level
PARAGRAPH 3 (Factual Skills): 2-3 ACTUAL experiences from CV mapped to job requirements with honest representation
PARAGRAPH 4 (Professional Close): Confident but realistic call-to-action appropriate to experience level

Sincerely,
{consultant_name}

ACCURACY VALIDATION REQUIREMENTS:
✓ All metrics/percentages come directly from CV content
✓ Experience duration matches CV exactly (e.g., 1.5 years, not "extensive experience")
✓ Project descriptions match CV information precisely
✓ Technologies mentioned are listed in CV
✓ Achievement scale matches experience level appropriately
✓ No superlatives unsupported by CV evidence

CALIBRATED LANGUAGE GUIDELINES:
- Junior level (0-2 years): "contributed to," "participated in," "assisted with," "gained experience in"
- Mid level (3-5 years): "led," "developed," "implemented," "managed"
- Senior level (5+ years): "architected," "directed," "established," "transformed"

OPTIMIZATION REQUIREMENTS:
- Action verbs appropriate to actual experience level
- Specific details ONLY from CV content (project names, technologies, actual results)
- Industry language from job description but realistic to candidate level
- Problem-solution examples with CV-supported context
- Honest progression indicators based on actual career timeline

STRICTLY FORBIDDEN:
- Adding metrics not present in CV content
- Inflating experience duration (claiming 5+ years when CV shows 1.5 years)
- Creating achievements not mentioned in CV
- Using "extensive experience" for junior-level candidates  
- Fabricating team leadership roles not documented in CV
- Adding technologies or skills not listed in CV
- Claiming "worldwide impact" without CV evidence
- Exaggerating project scale beyond CV information
- Generic percentage improvements without CV basis

CREDIBILITY PROTECTION:
- If CV lacks specific metrics, focus on responsibilities and technologies used
- Present genuine strengths without overselling
- Use "contributed to improvements" rather than claiming specific percentages
- Highlight potential based on actual demonstrated skills
- Frame experience positively but accurately

REALISTIC ACHIEVEMENT FRAMING:
Instead of: "Enhanced system performance by 30%" 
Use: "Contributed to system optimization through SQL query improvements"

Instead of: "Led cross-functional teams"
Use: "Collaborated effectively with cross-functional teams"

Instead of: "Extensive experience in..."
Use: "1.5 years of focused experience in..."

VALIDATION CHECKLIST:
1. Word count is under {word_limit}
2. All claims can be traced to CV content
3. Experience level language is appropriate
4. No fabricated metrics or achievements
5. Technology stack matches CV exactly
6. Professional tone without overselling
7. Realistic value proposition for experience level

OUTPUT REQUIREMENT: Generate cover letter that hiring managers will find credible and authentic upon verification."""
    }
    
    
    
def get_introduction_email_prompt(
    consultant_info: dict, 
    assignment_info: dict, 
    analysis_result: dict, 
    model_name: str = "gpt-3.5-turbo"
) -> dict:
    """Generate polished, professional introduction emails with a natural flow."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = "gpt-3.5-turbo"
    
    consultant_name = consultant_info.get("name", "the consultant")
    company_name = assignment_info.get("company_name", "[Company Name]")
    position = assignment_info.get("position", "the position")

    return {
        "system": (
            SYSTEM_PROMPTS[model_name]["introduction_email"] +
            " IMPORTANT: Produce only the final email content, under 250 words, "
            "with a natural, polished tone suitable for business correspondence. "
            "Avoid headings like KEY QUALIFICATIONS; integrate details into smooth sentences. "
            "No meta-commentary or extra text beyond the email."
        ),
        "user": f"""
TASK: Draft a professional, ready-to-send introduction email.

CONSULTANT PROFILE:
{consultant_info}

POSITION DETAILS:
Position: {position}
Company: {company_name}
Requirements: {assignment_info.get('description', '')}

MATCH ANALYSIS: {analysis_result.get('overall_score', 0)}% fit

STYLE REQUIREMENTS:
- Concise (<250 words), warm yet professional
- Reference at least one specific skill or achievement relevant to {company_name}
- Flow naturally, not as a résumé list
- Finish with a confident invitation to connect

OUTPUT FORMAT (no extra commentary):

Subject: Introduction: {consultant_name} – {position} Opportunity at {company_name}

Dear Hiring Manager,

[Opening greeting and intro of {consultant_name}, highlighting experience.]

[One paragraph blending skills and key projects relevant to the position/company.]

[Short paragraph on how {consultant_name} can add value and invite discussion.]

Best regards,
[Your Name]
[Your Title]
[Your Contact Information]
"""
    }


def get_customize_content_prompt(content_type: str, original_content: str, user_prompt: str, context: dict = None, model_name: str = None) -> dict:
    """Generate optimized prompts for customizing content based on user feedback."""
    
    system_prompt = (
        "You are an expert editor and professional writer with proven success in content optimization. "
        "CRITICAL: Revise the provided text based on user instructions with precision and professionalism. "
        "MANDATORY: Maintain or enhance professional quality while incorporating ALL user feedback. "
        "FORBIDDEN: Do not ask for additional information - work with provided content only."
    )

    user_prompt_text = (
        f"TASK: Revise the following {content_type} based on specific user instructions.\n\n"
        f"ORIGINAL {content_type.upper()}:\n"
        f"'''\n{original_content}\n'''\n\n"
        f"USER REVISION INSTRUCTIONS:\n"
        f"'''\n{user_prompt}\n'''\n\n"
        f"CRITICAL REQUIREMENTS:\n"
        f"1. Address ALL user instructions precisely\n"
        f"2. Maintain professional tone and quality\n"
        f"3. Preserve effective elements from original\n"
        f"4. Enhance clarity and impact\n"
        f"5. Return ONLY the revised {content_type} - no commentary\n\n"
        f"VALIDATION: ensure all user requests are implemented while maintaining professional standards."
    )
    
    if context:
        user_prompt_text += f"\n\nADDITIONAL CONTEXT FOR OPTIMIZATION:\n{json.dumps(context, indent=2)}"

    return {"system": system_prompt, "user": user_prompt_text}

def get_summary_prompt(cv_text: str, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate optimized prompts for professional summaries."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = 'gpt-3.5-turbo'
        
    return {
        'system': SYSTEM_PROMPTS[model_name]['summary'],
        'user': f"""TASK: Create a compelling professional summary that increases interview callbacks.

CV CONTENT:
{cv_text}

CRITICAL REQUIREMENTS:
- MAXIMUM 200 words - count precisely
- Lead with years of experience and primary expertise
- Include 2-3 quantifiable achievements
- Highlight unique value proposition
- Use industry-relevant keywords
- Professional, confident tone

MANDATORY STRUCTURE:
1. OPENING: [X] years of [specific expertise] with focus on [key areas]
2. ACHIEVEMENTS: [2-3 quantifiable accomplishments with metrics]
3. EXPERTISE: Core technical/professional competencies
4. VALUE: Unique strengths and career differentiators
5. GROWTH: Relevant certifications, education, or development

OPTIMIZATION REQUIREMENTS:
- Start with most impressive credential/experience
- Include specific numbers: years, percentages, scale, results
- Use action-oriented language
- Highlight progression and growth
- Match common industry terminology
- End with forward-looking capability statement

EXAMPLE METRICS TO INCLUDE:
- Years of experience in specific areas
- Team sizes managed or led
- Budget/revenue responsibility
- Project scale or impact
- Performance improvements achieved
- Technologies mastered
- Certifications earned

FORBIDDEN:
- Generic statements without evidence
- Subjective claims without proof
- First-person references ("I am," "I have")
- Exceeding 200-word limit
- Asking for additional information

VALIDATION: Count words, ensure professional impact, verify all claims are supported by CV content."""
    }
