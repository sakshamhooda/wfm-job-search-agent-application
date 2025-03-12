from anthropic import Anthropic
import os
from dotenv import load_dotenv

class SearchStrategyAgent:
    def __init__(self):
        load_dotenv()
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def generate_queries(self, resume_data, skills, job_titles, locations):
        """
        Generate optimized search queries based on resume data and user inputs
        
        Args:
            resume_data (dict): Parsed resume information
            skills (list): User-provided skills
            job_titles (list): User-provided job titles
            locations (list): User-provided locations
            
        Returns:
            list: List of search queries optimized for different job platforms
        """
        # Combine resume skills with user-provided skills
        all_skills = set(resume_data.get('skills', []) + skills)
        
        # Generate base queries
        queries = []
        
        # If job titles are provided, use them; otherwise, extract from resume
        search_titles = job_titles if job_titles else self._extract_job_titles(resume_data)
        
        # If locations are provided, use them; otherwise, use a broader search
        search_locations = locations if locations else ['remote']
        
        # Generate combinations of search queries
        for title in search_titles:
            for location in search_locations:
                # Basic query
                query = f"{title} {location}"
                queries.append(query)
                
                # Add skills to create more specific queries
                if all_skills:
                    skills_str = " ".join(list(all_skills)[:3])  # Use top 3 skills
                    specific_query = f"{title} {skills_str} {location}"
                    queries.append(specific_query)
        
        return queries
    
    def _extract_job_titles(self, resume_data):
        """Extract relevant job titles from resume data using Claude"""
        try:
            # Prepare prompt for Claude
            prompt = f"""Based on the following resume information, suggest relevant job titles to search for:

            Experience:
            {resume_data.get('experience', [])}

            Skills:
            {resume_data.get('skills', [])}

            Please provide 3-5 relevant job titles that match this candidate's experience and skills.
            Return only the job titles, one per line."""

            # Get suggestions from Claude
            response = self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=150,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Process response
            suggested_titles = response.content[0].text.strip().split('\n')
            return [title.strip() for title in suggested_titles if title.strip()]
            
        except Exception as e:
            print(f"Error extracting job titles: {str(e)}")
            return ["software engineer", "developer"]  # Default fallback titles