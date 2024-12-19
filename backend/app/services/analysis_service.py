from typing import Dict, List, Tuple
import logging
from difflib import SequenceMatcher
import re

logger = logging.getLogger(__name__)

class AnalysisService:
    def calculate_skills_match(self, resume_skills: List[str], job_skills: List[str]) -> Tuple[float, List[str]]:
        """Calculate skills match percentage and missing skills"""
        # Handle None or empty values
        resume_skills = resume_skills or []
        job_skills = job_skills or []
        
        if not job_skills:
            return 100.0, []
            
        matched_skills = 0
        missing_skills = []
        
        # Normalize skills for comparison
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        
        for job_skill in job_skills:
            job_skill_lower = job_skill.lower()
            best_match = 0
            
            # Find best partial match for each skill
            for resume_skill in resume_skills_lower:
                match_ratio = SequenceMatcher(None, job_skill_lower, resume_skill).ratio()
                best_match = max(best_match, match_ratio)
            
            if best_match >= 0.8:  # Consider it a match if 80% similar
                matched_skills += 1
            else:
                missing_skills.append(job_skill)
                
        match_percentage = (matched_skills / len(job_skills)) * 100 if job_skills else 100.0
        return match_percentage, missing_skills

    def calculate_experience_match(self, resume_data: Dict, job_data: Dict) -> Tuple[float, List[str]]:
        """Calculate experience match percentage and gaps"""
        # Handle None values
        resume_data = resume_data or {}
        job_data = job_data or {}
        
        try:
            job_years_required = self._extract_years_required(job_data)
            candidate_years = self._calculate_total_experience(resume_data)
            
            # Calculate base match percentage
            if job_years_required == 0:
                experience_match = 100.0
            else:
                experience_match = min(100.0, (candidate_years / max(job_years_required, 1)) * 100)
            
            # Check for relevant experience
            relevant_experience = self._check_relevant_experience(
                resume_data.get('work_experience', []),
                job_data.get('responsibilities', [])
            )
            
            # Adjust match based on relevance
            final_match = (experience_match * 0.6) + (relevant_experience * 0.4)
            
            gaps = self._identify_experience_gaps(resume_data, job_data)
            return final_match, gaps
            
        except Exception as e:
            logger.error(f"Error calculating experience match: {str(e)}")
            return 0.0, ["Unable to calculate experience match"]

    def _extract_years_required(self, job_data: Dict) -> float:
        """Extract required years of experience from job description"""
        try:
            requirements = job_data.get('requirements', '')
            if not requirements:
                return 0.0
                
            # Look for patterns like "X years", "X+ years", "X-Y years"
            year_patterns = [
                r'(\d+)(?:\+)?\s*(?:-\s*\d+)?\s*years?',
                r'(\d+)\s*\+\s*years?',
                r'minimum\s*(?:of\s*)?(\d+)\s*years?'
            ]
            
            for pattern in year_patterns:
                matches = re.findall(pattern, requirements.lower())
                if matches:
                    return float(matches[0])
            return 0.0
            
        except Exception as e:
            logger.error(f"Error extracting years required: {str(e)}")
            return 0.0

    def _calculate_total_experience(self, resume_data: Dict) -> float:
        """Calculate total years of experience from resume"""
        try:
            work_experience = resume_data.get('work_experience', [])
            if not work_experience:
                return 0.0
                
            total_years = 0.0
            for exp in work_experience:
                # Assuming each experience has duration_years or we calculate from dates
                if 'duration_years' in exp:
                    total_years += float(exp['duration_years'])
                # Add logic here to calculate from start/end dates if needed
                
            return total_years
            
        except Exception as e:
            logger.error(f"Error calculating total experience: {str(e)}")
            return 0.0

    def _check_relevant_experience(self, work_experience: List[Dict], job_responsibilities: List[str]) -> float:
        """Check how relevant the candidate's experience is to the job"""
        try:
            if not work_experience or not job_responsibilities:
                return 0.0
                
            total_relevance = 0.0
            for resp in job_responsibilities:
                best_match = 0.0
                for exp in work_experience:
                    description = exp.get('description', '')
                    if description:
                        match_ratio = SequenceMatcher(None, resp.lower(), description.lower()).ratio()
                        best_match = max(best_match, match_ratio)
                total_relevance += best_match
                
            return (total_relevance / len(job_responsibilities)) * 100 if job_responsibilities else 100.0
            
        except Exception as e:
            logger.error(f"Error checking relevant experience: {str(e)}")
            return 0.0

    def _identify_experience_gaps(self, resume_data: Dict, job_data: Dict) -> List[str]:
        """Identify gaps in experience compared to job requirements"""
        gaps = []
        try:
            required_years = self._extract_years_required(job_data)
            actual_years = self._calculate_total_experience(resume_data)
            
            if required_years > actual_years:
                gaps.append(f"Need {required_years - actual_years:.1f} more years of experience")
                
            # Add other gap identification logic here
            
        except Exception as e:
            logger.error(f"Error identifying experience gaps: {str(e)}")
            
        return gaps

    def calculate_education_match(self, resume_data: Dict, job_data: Dict) -> Tuple[float, List[str]]:
        """Calculate education match percentage and recommendations"""
        # Handle None values
        resume_data = resume_data or {}
        job_data = job_data or {}
        
        required_education = job_data.get('qualifications', [])
        candidate_education = resume_data.get('education', [])
        
        if not required_education:
            return 100.0, []
            
        education_score = 0
        recommendations = []
        
        # Check degree levels and fields
        for req in required_education:
            req_lower = req.lower()
            matched = False
            
            for edu in candidate_education:
                if (edu.get('degree') and edu.get('major') and 
                    (req_lower in edu['degree'].lower() or 
                     req_lower in edu['major'].lower())):
                    matched = True
                    break
                    
            if matched:
                education_score += 1
            else:
                recommendations.append(f"Consider pursuing {req}")
                
        match_percentage = (education_score / len(required_education)) * 100 if required_education else 100.0
        return match_percentage, recommendations

    def calculate_overall_match(self, 
                              skills_match: float,
                              experience_match: float,
                              education_match: float) -> float:
        """Calculate weighted overall match percentage"""
        # Handle None values
        skills_match = skills_match or 0.0
        experience_match = experience_match or 0.0
        education_match = education_match or 0.0
        
        weights = {
            'skills': 0.4,
            'experience': 0.4,
            'education': 0.2
        }
        
        overall_match = (
            (skills_match * weights['skills']) +
            (experience_match * weights['experience']) +
            (education_match * weights['education'])
        )
        
        return round(overall_match, 1) 