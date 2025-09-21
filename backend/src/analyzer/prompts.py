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

















# A centralized place for all prompts used in the application
import json

# --- Model-specific System Prompts ---
SYSTEM_PROMPTS = {
    'gpt-3.5-turbo': {
        'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
        Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
        'skills': """You are a technical skills assessment expert.
        Evaluate skills against job requirements and provide detailed matching analysis.""",
        
        'experience': """You are an expert in evaluating professional experience.
        Assess work history relevance and impact, focusing on concrete achievements.""",
        
        'motivation': """You are skilled at writing compelling motivations for job applications.
        Create engaging content that highlights candidate strengths. Do not ask for more information.""",
        
        'cover_letter': """You are a professional cover letter writer.
        Create persuasive letters that effectively showcase candidate qualifications.""",
        
        'summary': """You are an expert at creating professional summaries.
        Craft concise, impactful overviews of candidate profiles."""
    },
    
    'gpt-4': {
        'analyze': """You are a world-class HR analyst with deep expertise in technical recruitment and talent assessment.
        Provide comprehensive CV analysis with detailed insights in the specified JSON format only.""",
        
        'skills': """You are a senior technical skills evaluator with extensive industry knowledge.
        Provide in-depth analysis of technical capabilities with specific examples.""",
        
        'experience': """You are an expert in evaluating career trajectories and professional achievements.
        Assess experience depth, progression, and impact with detailed context.""",
        
        'motivation': """You are an expert at crafting compelling professional narratives.
        Create highly personalized motivations that resonate with specific job requirements. Do not ask for more information.""",
        
        'cover_letter': """You are an expert career coach specializing in high-impact cover letters.
        Create sophisticated, tailored letters that demonstrate deep understanding of the role.""",
        
        'summary': """You are an expert in professional branding and career narratives.
        Create compelling professional summaries that highlight unique value propositions."""
    },
    
    'gpt-4-turbo': {
        'analyze': """You are a world-class HR analyst with deep expertise in technical recruitment and talent assessment.
        Provide comprehensive CV analysis with detailed insights in the specified JSON format only.""",
        
        'skills': """You are a senior technical skills evaluator with extensive industry knowledge.
        Provide in-depth analysis of technical capabilities with specific examples.""",
        
        'experience': """You are an expert in evaluating career trajectories and professional achievements.
        Assess experience depth, progression, and impact with detailed context.""",
        
        'motivation': """You are an expert at crafting compelling professional narratives.
        Create highly personalized motivations that resonate with specific job requirements. Do not ask for more information.""",
        
        'cover_letter': """You are an expert career coach specializing in high-impact cover letters.
        Create sophisticated, tailored letters that demonstrate deep understanding of the role.""",
        
        'summary': """You are an expert in professional branding and career narratives.
        Create compelling professional summaries that highlight unique value propositions."""
    },
    
    'gemini-1.5-flash': {
        'analyze': """As an advanced HR analyst, provide thorough CV evaluation.
        Return detailed analysis in the specified JSON format with clear insights.""",
        
        'skills': """As a technical skills analyst, evaluate competencies comprehensively.
        Focus on both technical depth and practical application.""",
        
        'experience': """As an experience evaluation specialist, analyze career progression.
        Focus on achievements, growth, and skill development.""",
        
        'motivation': """As a professional content creator, craft engaging motivations.
        Focus on alignment between candidate strengths and role requirements. Do not ask for more information.""",
        
        'cover_letter': """As a cover letter specialist, create impactful application letters.
        Focus on clear value proposition and role alignment.""",
        
        'summary': """As a professional profile expert, create effective summaries.
        Focus on key achievements and unique qualifications."""
    },
    
    'gemini-1.5-pro': {
        'analyze': """As an advanced HR analyst, provide thorough CV evaluation.
        Return detailed analysis in the specified JSON format with clear insights.""",
        
        'skills': """As a technical skills analyst, evaluate competencies comprehensively.
        Focus on both technical depth and practical application.""",
        
        'experience': """As an experience evaluation specialist, analyze career progression.
        Focus on achievements, growth, and skill development.""",
        
        'motivation': """As a professional content creator, craft engaging motivations.
        Focus on alignment between candidate strengths and role requirements. Do not ask for more information.""",
        
        'cover_letter': """As a cover letter specialist, create impactful application letters.
        Focus on clear value proposition and role alignment.""",
        
        'summary': """As a professional profile expert, create effective summaries.
        Focus on key achievements and unique qualifications."""
    },
    
    'gemma2:9b-instruct-q4_K_M': {
        'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
        Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
        'skills': """You are a technical skills assessment expert.
        Evaluate skills against job requirements and provide detailed matching analysis.""",
        
        'experience': """You are an expert in evaluating professional experience.
        Assess work history relevance and impact, focusing on concrete achievements.""",
        
        'motivation': """You are skilled at writing compelling motivations for job applications.
        Create engaging content that highlights candidate strengths. Do not ask for more information.""",
        
        'cover_letter': """You are a professional cover letter writer.
        Create persuasive letters that effectively showcase candidate qualifications.""",
        
        'summary': """You are an expert at creating professional summaries.
        Craft concise, impactful overviews of candidate profiles."""
    },
    
    'gemma3:1b': {
        'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
        Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
        'skills': """You are a technical skills assessment expert.
        Evaluate skills against job requirements and provide detailed matching analysis.""",
        
        'experience': """You are an expert in evaluating professional experience.
        Assess work history relevance and impact, focusing on concrete achievements.""",
        
        'motivation': """You are skilled at writing compelling motivations for job applications.
        Create engaging content that highlights candidate strengths. Do not ask for more information.""",
        
        'cover_letter': """You are a professional cover letter writer.
        Create persuasive letters that effectively showcase candidate qualifications.""",
        
        'summary': """You are an expert at creating professional summaries.
        Craft concise, impactful overviews of candidate profiles."""
    },
    
    'llama3': {
        'analyze': """You are a proficient HR analyst with expertise in technical recruitment. 
        Analyze CVs objectively and return structured feedback in the specified JSON format only.""",
        
        'skills': """You are a technical skills assessment expert.
        Evaluate skills against job requirements and provide detailed matching analysis.""",
        
        'experience': """You are an expert in evaluating professional experience.
        Assess work history relevance and impact, focusing on concrete achievements.""",
        
        'motivation': """You are skilled at writing compelling motivations for job applications.
        Create engaging content that highlights candidate strengths. Do not ask for more information.""",
        
        'cover_letter': """You are a professional cover letter writer.
        Create persuasive letters that effectively showcase candidate qualifications.""",
        
        'summary': """You are an expert at creating professional summaries.
        Craft concise, impactful overviews of candidate profiles."""
    },
}

def get_analyze_cv_prompt(cv_text: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate prompts for CV analysis."""
    
    # Add fallback for unknown models
    if model_name not in SYSTEM_PROMPTS:
        logger.warning(f"Model '{model_name}' not found in SYSTEM_PROMPTS, using gpt-3.5-turbo as fallback")
        model_name = 'gpt-3.5-turbo'
    
    return {
        'system': SYSTEM_PROMPTS[model_name]['analyze'],
        'user': f"""Analyze this CV against the requirements.

REQUIREMENTS:
{requirements}

CV CONTENT:
{cv_text}

Return a single, valid JSON object using this exact format:
{{
    "overall_score": number,           # 0-100 overall match score
    "requirements_score": number,      # 0-100 score for mandatory requirements
    "wishes_score": number,           # 0-100 score for optional requirements
    "requirements": [                  # Array of requirement matches
        {{
            "id": string,             # Unique identifier
            "type": "require",        # Type is always "require" for requirements
            "title": string,          # Short requirement description
            "description": string,    # Full requirement text
            "match": boolean,        # Whether requirement is met
            "percentage": number,    # 0-100 match percentage
            "explanation": string    # Evidence-based explanation
        }}
    ],
    "wishes": [                      # Array of optional requirement matches
        {{
            "id": string,           # Unique identifier
            "type": "wish",         # Type is always "wish" for optional items
            "title": string,        # Short requirement description
            "description": string,  # Full requirement text
            "match": boolean,      # Whether requirement is met
            "percentage": number,  # 0-100 match percentage
            "explanation": string  # Evidence-based explanation
        }}
    ]
}}"""
    }

def get_skills_analysis_prompt(skills_text: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate prompts for detailed skills analysis."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = 'gpt-3.5-turbo'
        
    return {
        'system': SYSTEM_PROMPTS[model_name]['skills'],
        'user': f"""Analyze these technical skills against the requirements.

REQUIRED SKILLS:
{requirements}

CANDIDATE SKILLS:
{skills_text}

Provide analysis in this JSON format:
{{
    "technical_skills": {{
        "match_score": float,        # 0-1 score
        "matching_skills": [str],    # Skills that match
        "missing_skills": [str],     # Required skills not found
        "additional_skills": [str]    # Extra relevant skills
    }},
    "recommendations": [str]         # Specific improvement suggestions
}}"""
    }

def get_experience_analysis_prompt(experience: str, requirements: str, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate prompts for experience analysis."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = 'gpt-3.5-turbo'
        
    return {
        'system': SYSTEM_PROMPTS[model_name]['experience'],
        'user': f"""Analyze this work experience against the job requirements.

ROLE REQUIREMENTS:
{requirements}

WORK EXPERIENCE:
{experience}

Provide analysis in this JSON format:
{{
    "experience_match": {{
        "score": float,              # 0-1 score
        "years_relevant": float,     # Years of relevant experience
        "key_achievements": [str],   # Relevant achievements
        "missing_areas": [str]       # Required experience not found
    }},
    "recommendations": [str]         # Specific suggestions
}}"""
    }

def get_motivation_prompt(cv_text: str, job_desc: str, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate prompts for motivation letter."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = 'gpt-3.5-turbo'
        
    return {
        'system': SYSTEM_PROMPTS[model_name]['motivation'],
        'user': f"""Write a compelling motivation based on the CV content provided. Do not ask for more information.

CV CONTENT:
{cv_text}

JOB DESCRIPTION:
{job_desc}

Focus on:
1. Strong matches between requirements and experience
2. Relevant achievements and expertise from the CV
3. Specific examples from the provided CV
4. Growth potential and enthusiasm
5. Cultural fit and soft skills

Generate the motivation directly without asking for additional details."""
    }

def get_cover_letter_prompt(cv_text: str, job_desc: str, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate prompts for cover letter."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = 'gpt-3.5-turbo'
        
    return {
        'system': SYSTEM_PROMPTS[model_name]['cover_letter'],
        'user': f"""Create a professional cover letter based on the CV and job description provided. Do not ask for more information.

JOB DESCRIPTION:
{job_desc}

CV CONTENT:
{cv_text}

Include:
1. Strong opening that grabs attention
2. Specific examples of relevant experience from the CV
3. Clear connection to job requirements
4. Demonstration of company knowledge
5. Professional closing with call to action

Generate the cover letter directly using the provided information."""
    }

def get_customize_content_prompt(content_type: str, original_content: str, user_prompt: str, context: dict = None, model_name: str = None) -> dict:
    """
    Generates system and user prompts for customizing previously generated content.
    """
    system_prompt = (
        "You are an expert editor and writer. Your task is to revise the provided text based on the user's instructions. "
        "Pay close attention to the user's feedback and modify the text accordingly, maintaining a professional tone. "
        "Do not ask for more information - work with what is provided."
    )

    user_prompt_text = (
        f"Please revise the following {content_type} based on my instructions.\n\n"
        f"ORIGINAL {content_type.upper()}:\n"
        f"'''\n{original_content}\n'''\n\n"
        f"USER INSTRUCTIONS:\n"
        f"'''\n{user_prompt}\n'''\n\n"
        "Generate the revised text directly, without adding any extra commentary or conversational text."
    )
    
    if context:
        user_prompt_text += f"\n\nADDITIONAL CONTEXT:\n{json.dumps(context, indent=2)}"

    return {"system": system_prompt, "user": user_prompt_text}

def get_summary_prompt(cv_text: str, model_name: str = 'gpt-3.5-turbo') -> dict:
    """Generate prompts for professional summary."""
    if model_name not in SYSTEM_PROMPTS:
        model_name = 'gpt-3.5-turbo'
        
    return {
        'system': SYSTEM_PROMPTS[model_name]['summary'],
        'user': f"""Create a professional summary based on this CV. Do not ask for more information.

CV CONTENT:
{cv_text}

Create a concise summary that:
1. Highlights years of relevant experience
2. Emphasizes key technical skills
3. Mentions significant achievements
4. Shows career progression
5. Includes relevant certifications/education

Keep it under 200 words and focus on unique value proposition. Generate the summary directly using the provided CV content."""
    }
