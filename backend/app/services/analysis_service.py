from typing import Dict
import logging
from openai import AsyncOpenAI
from app.core.config import get_settings
from app.utils.prompting_instructions import FIT_SCORE_SYSTEM_PROMPT
import json

logger = logging.getLogger(__name__)
settings = get_settings()

class AnalysisService:
    def __init__(self):
        openai_api_key = settings.OPENAI_API_KEY.strip()
        if not openai_api_key:
            raise ValueError("OpenAI API key not found in settings")
            
        self.client = AsyncOpenAI(
            api_key=openai_api_key,
            base_url="https://api.openai.com/v1",
            max_retries=3,
            timeout=30.0
        )
        self.model = settings.OPENAI_MODEL

    async def analyze_resume_fit(self, resume_data: Dict, job_data: Dict) -> Dict:
        """
        Analyze resume fit using OpenAI's LLM
        Returns: Full analysis result from OpenAI
        """
        try:
            # Adapt the input format for the new summary structure
            input_content = {
                "job_description": job_data,
                "resume_summary": resume_data  # Now contains the summarized format
            }

            logger.info("Sending analysis request to OpenAI")
            # Call OpenAI API using the FIT_SCORE_SYSTEM_PROMPT
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": FIT_SCORE_SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(input_content)}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )

            # Parse the response
            analysis_result = json.loads(completion.choices[0].message.content)
            logger.info(f"\n\n\033[94mAnalysis result:\033[0m {analysis_result}\n\n")
            logger.info("Successfully generated analysis using OpenAI")

            # Transform the analysis result to match the expected frontend format
            transformed_result = {
                "overallFit": int(analysis_result.get("fit_analysis", {}).get("fit_score", 0)),
                "skillsMatch": int(analysis_result.get("score_breakdown", {}).get("skills_match", {}).get("score", 0)),
                "experienceMatch": int(analysis_result.get("score_breakdown", {}).get("experience_match", {}).get("score", 0)),
                "recommendations": [],  # Initialize empty array
                "detailed_analysis": {
                    "executive_summary": analysis_result.get("executive_summary"),
                    "fit_analysis": {
                        "overall_assessment": analysis_result.get("fit_analysis", {}).get("overall_assessment"),
                        "fit_score": int(analysis_result.get("fit_analysis", {}).get("fit_score", 0))
                    },
                    "key_strengths": {
                        "skills": analysis_result.get("key_strengths", {}).get("skills", []),
                        "experience": analysis_result.get("key_strengths", {}).get("experience", []),
                        "notable_achievements": analysis_result.get("key_strengths", {}).get("notable_achievements", [])
                    },
                    "areas_for_development": {
                        "skills_gaps": analysis_result.get("areas_for_development", {}).get("skills_gaps", []),
                        "experience_gaps": analysis_result.get("areas_for_development", {}).get("experience_gaps", []),
                        "recommendations": analysis_result.get("areas_for_development", {}).get("recommendations", [])
                    },
                    "score_breakdown": {
                        "skills_match": str(analysis_result.get("score_breakdown", {}).get("skills_match", {}).get("score", 0)) + "% - " + 
                                      analysis_result.get("score_breakdown", {}).get("skills_match", {}).get("explanation", ""),
                        "experience_match": str(analysis_result.get("score_breakdown", {}).get("experience_match", {}).get("score", 0)) + "% - " + 
                                          analysis_result.get("score_breakdown", {}).get("experience_match", {}).get("explanation", "")
                    },
                    "interesting_fact": analysis_result.get("interesting_fact")
                }
            }

            # Add recommendations
            if analysis_result.get("executive_summary"):
                transformed_result["recommendations"].append(analysis_result["executive_summary"])
            
            if analysis_result.get("fit_analysis", {}).get("overall_assessment"):
                transformed_result["recommendations"].append(
                    f"Overall Assessment: {analysis_result['fit_analysis']['overall_assessment']}"
                )

            # Add key strengths to recommendations
            if analysis_result.get("key_strengths"):
                strengths = analysis_result["key_strengths"]
                if strengths.get("skills"):
                    transformed_result["recommendations"].append(
                        f"Key Skills: {', '.join(strengths['skills'])}"
                    )
                if strengths.get("experience"):
                    transformed_result["recommendations"].append(
                        f"Relevant Experience: {', '.join(strengths['experience'])}"
                    )

            # Add development areas to recommendations
            if analysis_result.get("areas_for_development"):
                dev = analysis_result["areas_for_development"]
                if dev.get("skills_gaps"):
                    transformed_result["recommendations"].append(
                        f"Skills to Develop: {', '.join(dev['skills_gaps'])}"
                    )
                if dev.get("recommendations"):
                    transformed_result["recommendations"].extend(dev["recommendations"])

            # Add interesting fact if available
            if analysis_result.get("interesting_fact"):
                transformed_result["recommendations"].append(
                    f"Notable: {analysis_result['interesting_fact']}"
                )

            return transformed_result

        except Exception as e:
            logger.error(f"Error in analyze_resume_fit: {str(e)}")
            return {
                "overallFit": 0,
                "skillsMatch": 0,
                "experienceMatch": 0,
                "recommendations": ["Error analyzing resume. Please try again."],
                "detailed_analysis": {
                    "error": str(e),
                    "executive_summary": "Error analyzing resume",
                    "fit_analysis": {
                        "overall_assessment": "Analysis failed",
                        "fit_score": 0
                    }
                }
            }