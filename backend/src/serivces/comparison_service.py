import logging
from typing import List, Dict, Any
import asyncio

logger = logging.getLogger(__name__)


class ResumeComparisonService:
    """Service for comparing and ranking multiple resumes."""
    
    def __init__(self, analyzer):
        """Initialize with CV analyzer instance."""
        self.analyzer = analyzer
    
    async def compare_resumes(
        self,
        resumes: List[Dict[str, str]],
        job_description: str,
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Compare multiple resumes against job description."""
        logger.info(f"Comparing {len(resumes)} resumes against job description")
        
        async def analyze_single_resume(resume: Dict) -> Dict:
            try:
                analysis = await self.analyzer.analyze_cv_assignment_match(
                    cv_text=resume['processed_text'],
                    assignment_text=job_description
                )
                
                return {
                    "filename": resume['filename'],
                    "original_language": resume.get('detected_language', 'en'),
                    "was_translated": resume.get('was_translated', False),
                    "analysis": analysis,
                    "overall_score": analysis.get('overall_score', 0),
                    "requirements_score": analysis.get('requirements_score', 0),
                    "wishes_score": analysis.get('wishes_score', 0),
                    "status": "success"
                }
            except Exception as e:
                logger.error(f"Analysis failed for {resume['filename']}: {e}")
                return {
                    "filename": resume['filename'],
                    "status": "error",
                    "error": str(e),
                    "overall_score": 0
                }
        
        tasks = [analyze_single_resume(resume) for resume in resumes]
        results = await asyncio.gather(*tasks)
        
        ranked_resumes = sorted(
            results, 
            key=lambda x: x.get('overall_score', 0), 
            reverse=True
        )
        
        for idx, resume in enumerate(ranked_resumes, 1):
            resume['rank'] = idx
        
        scores = [r['overall_score'] for r in ranked_resumes if r['status'] == 'success']
        
        statistics = {
            "total_resumes": len(resumes),
            "successfully_analyzed": len(scores),
            "failed_analyses": len(resumes) - len(scores),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0,
            "score_range": max(scores) - min(scores) if scores else 0
        }
        
        return {
            "ranked_resumes": ranked_resumes,
            "statistics": statistics,
            "job_info": job_data
        }
    
    def generate_comparison_summary(
        self, 
        comparison_result: Dict[str, Any]
    ) -> str:
        """Generate text summary of comparison results."""
        ranked = comparison_result['ranked_resumes']
        stats = comparison_result['statistics']
        
        summary = f"""
RESUME COMPARISON SUMMARY
========================

Total Resumes: {stats['total_resumes']}
Successfully Analyzed: {stats['successfully_analyzed']}
Failed: {stats['failed_analyses']}

Score Statistics:
- Average: {stats['average_score']:.1f}%
- Highest: {stats['highest_score']:.1f}%
- Lowest: {stats['lowest_score']:.1f}%
- Range: {stats['score_range']:.1f}%

TOP RANKINGS:
-------------
"""
        
        for resume in ranked[:10]:
            if resume['status'] == 'success':
                summary += f"\n{resume['rank']}. {resume['filename']}\n"
                summary += f"   Overall: {resume['overall_score']:.1f}%\n"
                summary += f"   Requirements: {resume['requirements_score']:.1f}%\n"
                summary += f"   Wishes: {resume['wishes_score']:.1f}%\n"
                if resume['was_translated']:
                    summary += f"   (Translated from {resume['original_language']})\n"
        
        return summary
