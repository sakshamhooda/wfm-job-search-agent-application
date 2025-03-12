from anthropic import Anthropic
import os
from dotenv import load_dotenv
from typing import List, Dict

class FilteringAgent:
    def __init__(self):
        load_dotenv()
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def filter_jobs(self, job_listings: List[Dict], resume_data: Dict) -> List[Dict]:
        """
        Filter and rank job listings based on resume match
        
        Args:
            job_listings (list): List of job listings
            resume_data (dict): Parsed resume data
            
        Returns:
            list: Filtered and ranked job listings
        """
        filtered_jobs = []
        
        for job in job_listings:
            # Calculate match score using Claude
            match_score = self._calculate_match_score(job, resume_data)
            
            # Add match score to job listing
            job['match_score'] = match_score
            
            # Only include jobs with match score above threshold
            if match_score >= 50:  # 50% match threshold
                filtered_jobs.append(job)
        
        # Sort by match score
        filtered_jobs.sort(key=lambda x: x['match_score'], reverse=True)
        
        return filtered_jobs
    
    def _calculate_match_score(self, job: Dict, resume_data: Dict) -> float:
        """
        Calculate match score between job listing and resume using Claude
        
        Args:
            job (dict): Job listing
            resume_data (dict): Parsed resume data
            
        Returns:
            float: Match score percentage
        """
        try:
            # Prepare prompt for Claude
            prompt = f"""Analyze the match between this job listing and candidate's resume.
            
            Job Listing:
            Title: {job.get('title', '')}
            Description: {job.get('description', '')}
            Requirements: {job.get('requirements', '')}
            
            Resume:
            Skills: {resume_data.get('skills', [])}
            Experience: {resume_data.get('experience', [])}
            Education: {resume_data.get('education', [])}
            
            Calculate a percentage match score based on:
            1. Skills match
            2. Experience relevance
            3. Education requirements
            4. Overall role fit
            
            Return only a number between 0 and 100."""

            # Get score from Claude
            response = self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=50,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract score from response
            score = float(response.content[0].text.strip())
            return min(max(score, 0), 100)  # Ensure score is between 0 and 100
            
        except Exception as e:
            print(f"Error calculating match score: {str(e)}")
            return 50.0  # Default middle score on error
    
    def _generate_match_explanation(self, job: Dict, resume_data: Dict) -> str:
        """
        Generate explanation for why a job matches the resume
        
        Args:
            job (dict): Job listing
            resume_data (dict): Parsed resume data
            
        Returns:
            str: Explanation of the match
        """
        try:
            # Prepare prompt for Claude
            prompt = f"""Explain why this job matches the candidate's resume.
            
            Job Listing:
            Title: {job.get('title', '')}
            Description: {job.get('description', '')}
            Requirements: {job.get('requirements', '')}
            
            Resume:
            Skills: {resume_data.get('skills', [])}
            Experience: {resume_data.get('experience', [])}
            Education: {resume_data.get('education', [])}
            
            Provide a brief explanation highlighting the key matching points."""

            # Get explanation from Claude
            response = self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=200,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"Error generating match explanation: {str(e)}")
            return "Match based on general qualifications and requirements."