import logging
import re
from typing import Dict, List, Any
from difflib import SequenceMatcher
import asyncio

logger = logging.getLogger(__name__)


class MatchCalculator:
    """Service for calculating dynamic match percentages between content and requirements."""
    
    @staticmethod
    def calculate_text_similarity(text1: str, text2: str) -> float:
        """Calculate similarity between two texts using sequence matching."""
        if not text1 or not text2:
            return 0.0
        
        # Normalize texts
        text1_normalized = text1.lower().strip()
        text2_normalized = text2.lower().strip()
        
        # Use SequenceMatcher for similarity
        matcher = SequenceMatcher(None, text1_normalized, text2_normalized)
        return matcher.ratio() * 100
    
    @staticmethod
    def extract_keywords(text: str) -> set:
        """Extract keywords from text."""
        # Remove special characters and split
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        # Common stop words to exclude
        stop_words = {'the', 'and', 'for', 'are', 'with', 'this', 'that', 'from', 'have', 'been', 'will', 'your', 'can', 'our', 'their'}
        return set(word for word in words if word not in stop_words)
    
    @staticmethod
    def calculate_keyword_match(content: str, requirement: str) -> float:
        """Calculate match percentage based on keyword overlap."""
        content_keywords = MatchCalculator.extract_keywords(content)
        requirement_keywords = MatchCalculator.extract_keywords(requirement)
        
        if not requirement_keywords:
            return 0.0
        
        # Calculate overlap
        overlap = content_keywords.intersection(requirement_keywords)
        match_percentage = (len(overlap) / len(requirement_keywords)) * 100
        
        return min(match_percentage, 100.0)
    
    @staticmethod
    def calculate_content_match(content: str, requirement_title: str, requirement_description: str = "") -> float:
        """
        Calculate comprehensive match percentage between content and requirement.
        Combines multiple matching strategies.
        """
        if not content:
            return 0.0
        
        # Strategy 1: Keyword matching with title
        title_keyword_match = MatchCalculator.calculate_keyword_match(content, requirement_title)
        
        # Strategy 2: Keyword matching with description (if available)
        desc_keyword_match = 0.0
        if requirement_description:
            desc_keyword_match = MatchCalculator.calculate_keyword_match(content, requirement_description)
        
        # Strategy 3: Sequence similarity with title
        title_similarity = MatchCalculator.calculate_text_similarity(content, requirement_title)
        
        # Strategy 4: Check for direct mentions
        content_lower = content.lower()
        title_lower = requirement_title.lower()
        direct_mention_bonus = 20.0 if title_lower in content_lower else 0.0
        
        # Combine strategies with weights
        if requirement_description:
            combined_match = (
                title_keyword_match * 0.3 +
                desc_keyword_match * 0.3 +
                title_similarity * 0.2 +
                direct_mention_bonus * 0.2
            )
        else:
            combined_match = (
                title_keyword_match * 0.4 +
                title_similarity * 0.3 +
                direct_mention_bonus * 0.3
            )
        
        return min(combined_match, 100.0)
    
    @staticmethod
    async def recalculate_motivation_match(
        motivation_text: str, 
        requirement: Dict[str, Any],
        cv_text: str = ""
    ) -> float:
        """
        Recalculate match percentage for a motivation against its requirement.
        """
        requirement_title = requirement.get('title', '')
        requirement_description = requirement.get('description', requirement_title)
        
        # Calculate match based on motivation content
        match_percentage = MatchCalculator.calculate_content_match(
            motivation_text,
            requirement_title,
            requirement_description
        )
        
        # Bonus if CV content is referenced
        if cv_text:
            cv_keywords = MatchCalculator.extract_keywords(cv_text)
            motivation_keywords = MatchCalculator.extract_keywords(motivation_text)
            cv_reference_bonus = min(len(cv_keywords.intersection(motivation_keywords)) * 2, 15)
            match_percentage = min(match_percentage + cv_reference_bonus, 100.0)
        
        logger.info(f"Recalculated motivation match for '{requirement_title}': {match_percentage:.1f}%")
        return match_percentage
    
    @staticmethod
    async def recalculate_cover_letter_match(
        cover_letter_text: str,
        requirements: List[Dict[str, Any]],
        assignment_description: str = ""
    ) -> float:
        """
        Recalculate overall match percentage for a cover letter.
        """
        if not cover_letter_text or not requirements:
            return 0.0
        
        # Calculate how well cover letter addresses each requirement
        requirement_matches = []
        for req in requirements:
            req_title = req.get('title', '')
            req_description = req.get('description', req_title)
            
            match = MatchCalculator.calculate_content_match(
                cover_letter_text,
                req_title,
                req_description
            )
            requirement_matches.append(match)
        
        # Average match across all requirements
        avg_match = sum(requirement_matches) / len(requirement_matches) if requirement_matches else 0.0
        
        # Bonus for professional formatting
        formatting_indicators = [
            'dear', 'sincerely', 'regards', 'application', 
            'position', 'experience', 'skills', 'qualified'
        ]
        cover_letter_lower = cover_letter_text.lower()
        formatting_score = sum(5 for indicator in formatting_indicators if indicator in cover_letter_lower)
        
        final_match = min(avg_match + formatting_score, 100.0)
        
        logger.info(f"Recalculated cover letter match: {final_match:.1f}%")
        return final_match
    
    @staticmethod
    async def recalculate_email_match(
        email_text: str,
        requirements: List[Dict[str, Any]],
        consultant_name: str = ""
    ) -> float:
        """
        Recalculate overall match percentage for an introduction email.
        """
        if not email_text or not requirements:
            return 0.0
        
        # Calculate requirement coverage
        requirement_matches = []
        for req in requirements:
            req_title = req.get('title', '')
            match = MatchCalculator.calculate_keyword_match(email_text, req_title)
            requirement_matches.append(match)
        
        avg_match = sum(requirement_matches) / len(requirement_matches) if requirement_matches else 0.0
        
        # Bonus for professional email elements
        email_indicators = [
            'subject:', 'dear', 'hello', 'introduce', 'candidate',
            'experience', 'skills', 'opportunity', 'attached', 'resume'
        ]
        email_lower = email_text.lower()
        email_formatting_score = sum(4 for indicator in email_indicators if indicator in email_lower)
        
        # Check for consultant name
        name_bonus = 10.0 if consultant_name and consultant_name.lower() in email_lower else 0.0
        
        final_match = min(avg_match + email_formatting_score + name_bonus, 100.0)
        
        logger.info(f"Recalculated email match: {final_match:.1f}%")
        return final_match
    
    @staticmethod
    async def batch_recalculate_motivations(
        motivations: Dict[str, str],
        requirements: List[Dict[str, Any]],
        cv_text: str = ""
    ) -> Dict[str, float]:
        """
        Recalculate match percentages for multiple motivations concurrently.
        """
        tasks = []
        requirement_map = {req['id']: req for req in requirements}
        
        for req_id, motivation_text in motivations.items():
            if req_id in requirement_map:
                task = MatchCalculator.recalculate_motivation_match(
                    motivation_text,
                    requirement_map[req_id],
                    cv_text
                )
                tasks.append((req_id, task))
        
        results = await asyncio.gather(*[task for _, task in tasks])
        
        return {req_id: match_pct for (req_id, _), match_pct in zip(tasks, results)}


def get_match_calculator() -> MatchCalculator:
    """Get match calculator instance."""
    return MatchCalculator()
