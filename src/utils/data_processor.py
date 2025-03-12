class DataProcessor:
    @staticmethod
    def generate_markdown(job_listings):
        """
        Generate markdown format of job listings
        
        Args:
            job_listings (list): List of job listing dictionaries
            
        Returns:
            str: Markdown formatted text
        """
        markdown = "# Job Matches\n\n"
        
        for job in job_listings:
            markdown += f"## {job.get('title', 'Unknown Position')}\n\n"
            markdown += f"**Company:** {job.get('company', 'Unknown')}\n\n"
            markdown += f"**Location:** {job.get('location', 'Unknown')}\n\n"
            
            if job.get('match_score'):
                markdown += f"**Match Score:** {job['match_score']}%\n\n"
            
            if job.get('description'):
                markdown += "### Description\n\n"
                markdown += f"{job['description']}\n\n"
            
            if job.get('requirements'):
                markdown += "### Requirements\n\n"
                markdown += f"{job['requirements']}\n\n"
            
            if job.get('url'):
                markdown += f"[Apply Here]({job['url']})\n\n"
            
            markdown += "---\n\n"
        
        return markdown
    
    @staticmethod
    def format_csv_data(job_listings):
        """
        Format job listings for CSV export
        
        Args:
            job_listings (list): List of job listing dictionaries
            
        Returns:
            list: Formatted data ready for CSV export
        """
        formatted_data = []
        
        for job in job_listings:
            formatted_job = {
                'Title': job.get('title', ''),
                'Company': job.get('company', ''),
                'Location': job.get('location', ''),
                'Match Score': job.get('match_score', ''),
                'Description': job.get('description', ''),
                'Requirements': job.get('requirements', ''),
                'URL': job.get('url', '')
            }
            formatted_data.append(formatted_job)
        
        return formatted_data