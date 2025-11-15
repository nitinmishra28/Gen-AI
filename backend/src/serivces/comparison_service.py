import logging
from typing import List, Dict, Any, Optional
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
        job_data: Dict[str, Any],
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Compare multiple resumes against job description with ranking.
        
        Args:
            resumes: List of processed resume dictionaries
            job_description: Job requirements text
            job_data: Additional job information
            model_name: LLM model to use for analysis
            
        Returns:
            Dictionary with ranked resumes and statistics
        """
        logger.info(f"Comparing {len(resumes)} resumes using model: {model_name}")
        
        async def analyze_single_resume(resume: Dict) -> Dict:
            """Analyze a single resume and return results with scores."""
            try:
                analysis = await self.analyzer.analyze_cv_assignment_match(
                    cv_text=resume['processed_text'],
                    assignment_text=job_description,
                    model_name=model_name
                )
                
                overall_score = analysis.get('overall_score', 0)
                
                return {
                    "filename": resume['filename'],
                    "original_language": resume.get('detected_language', 'en'),
                    "was_translated": resume.get('was_translated', False),
                    "analysis": analysis,
                    "overall_score": overall_score,
                    "requirements_score": analysis.get('requirements_score', 0),
                    "wishes_score": analysis.get('wishes_score', 0),
                    "initial_score": overall_score,
                    "current_score": overall_score,
                    "customization_count": 0,
                    "score_improvement": 0,
                    "status": "success"
                }
            except Exception as e:
                logger.error(f"Analysis failed for {resume['filename']}: {e}")
                return {
                    "filename": resume['filename'],
                    "status": "error",
                    "error": str(e),
                    "overall_score": 0,
                    "initial_score": 0,
                    "current_score": 0
                }
        
        tasks = [analyze_single_resume(resume) for resume in resumes]
        results = await asyncio.gather(*tasks)
        
        ranked_resumes = sorted(
            results, 
            key=lambda x: x.get('overall_score', 0), 
            reverse=True
        )
        
        # Assign ranks (1-10)
        for idx, resume in enumerate(ranked_resumes, 1):
            resume['rank'] = idx
        
        # Calculate statistics
        scores = [r['overall_score'] for r in ranked_resumes if r['status'] == 'success']
        
        statistics = {
            "total_resumes": len(resumes),
            "successfully_analyzed": len(scores),
            "failed_analyses": len(resumes) - len(scores),
            "average_score": sum(scores) / len(scores) if scores else 0,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0,
            "score_range": max(scores) - min(scores) if scores else 0,
            "model_used": model_name
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
        """
        Generate text summary of comparison results.
        
        Args:
            comparison_result: Result dictionary from compare_resumes
            
        Returns:
            Formatted text summary
        """
        ranked = comparison_result['ranked_resumes']
        stats = comparison_result['statistics']
        
        summary = f"""
RESUME COMPARISON SUMMARY
========================

Total Resumes: {stats['total_resumes']}
Successfully Analyzed: {stats['successfully_analyzed']}
Failed: {stats['failed_analyses']}
Model Used: {stats.get('model_used', 'N/A')}

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
                medal = ""
                if resume['rank'] == 1:
                    medal = " 🥇"
                elif resume['rank'] == 2:
                    medal = " 🥈"
                elif resume['rank'] == 3:
                    medal = " 🥉"
                
                summary += f"\n{resume['rank']}.{medal} {resume['filename']}\n"
                summary += f"   Overall: {resume['overall_score']:.1f}%\n"
                summary += f"   Requirements: {resume['requirements_score']:.1f}%\n"
                summary += f"   Wishes: {resume['wishes_score']:.1f}%\n"
                
                if resume['was_translated']:
                    summary += f"   (Translated from {resume['original_language']})\n"
                
                if resume.get('customization_count', 0) > 0:
                    improvement = resume['current_score'] - resume['initial_score']
                    summary += f"   Improvement: +{improvement:.1f}% ({resume['customization_count']} customizations)\n"
        
        return summary
    
    def update_resume_score(
        self,
        comparison_result: Dict[str, Any],
        filename: str,
        new_score: float
    ) -> Dict[str, Any]:
        """
        Update a resume's score after customization and re-rank.
        
        Args:
            comparison_result: Current comparison result
            filename: Name of the resume to update
            new_score: New overall score after customization
            
        Returns:
            Updated comparison result with new rankings
        """
        ranked_resumes = comparison_result['ranked_resumes']
        
        # Find and update the resume
        for resume in ranked_resumes:
            if resume['filename'] == filename:
                resume['current_score'] = new_score
                resume['overall_score'] = new_score
                resume['customization_count'] = resume.get('customization_count', 0) + 1
                resume['score_improvement'] = new_score - resume['initial_score']
                break
        
        # Re-rank all resumes
        ranked_resumes.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
        
        for idx, resume in enumerate(ranked_resumes, 1):
            resume['rank'] = idx
        
        # Recalculate statistics
        scores = [r['overall_score'] for r in ranked_resumes if r['status'] == 'success']
        
        comparison_result['statistics'].update({
            "average_score": sum(scores) / len(scores) if scores else 0,
            "highest_score": max(scores) if scores else 0,
            "lowest_score": min(scores) if scores else 0,
            "score_range": max(scores) - min(scores) if scores else 0
        })
        
        comparison_result['ranked_resumes'] = ranked_resumes
        
        logger.info(f"Updated score for {filename}: {new_score:.1f}% (Rank: {[r for r in ranked_resumes if r['filename'] == filename][0]['rank']})")
        
        return comparison_result
