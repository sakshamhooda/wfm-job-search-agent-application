import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict
from fake_useragent import UserAgent
import logging

class WebScraperAgent:
    def __init__(self):
        self.ua = UserAgent()
        # Initialize logger
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Longer delay between requests to avoid rate limiting
        self.min_delay = 5
        self.max_delay = 10
        
        # Add more realistic browser headers
        self.base_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        
        # Job search endpoints
        self.search_endpoints = {
            'linkedin': 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search',
            'indeed': 'https://api.indeed.com/ads/apisearch',  # Would require API key
            'glassdoor': 'https://www.glassdoor.com/Job/jobs.htm'
        }
    
    def get_headers(self):
        """Generate headers with random user agent"""
        headers = self.base_headers.copy()
        headers['User-Agent'] = self.ua.random
        return headers
    
    def scrape_jobs(self, search_queries: List[str]) -> List[Dict]:
        """
        Scrape job listings from multiple job boards based on search queries
        
        Args:
            search_queries (list): List of search queries to use
            
        Returns:
            list: List of job listings
        """
        all_jobs = []
        
        for query in search_queries:
            # Add delay between queries
            delay = random.uniform(self.min_delay, self.max_delay)
            time.sleep(delay)
            
            try:
                # Start with LinkedIn as it's more scraping-friendly
                jobs = self._scrape_linkedin(query)
                all_jobs.extend(jobs)
                
                self.logger.info(f"Successfully scraped {len(jobs)} jobs for query: {query}")
                
            except Exception as e:
                self.logger.error(f"Error scraping jobs for query '{query}': {str(e)}")
                continue
        
        # Remove duplicates
        return self._remove_duplicates(all_jobs)
    
    def _scrape_linkedin(self, query: str) -> List[Dict]:
        """Scrape job listings from LinkedIn"""
        jobs = []
        start = 0
        limit = 10  # Number of jobs per request
        
        try:
            # Format query for URL
            formatted_query = query.replace(' ', '%20')
            base_url = f"{self.search_endpoints['linkedin']}?keywords={formatted_query}&location=&start={start}"
            
            headers = self.get_headers()
            response = requests.get(base_url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract job cards
                job_cards = soup.find_all('div', {'class': 'job-search-card'})
                
                for card in job_cards:
                    try:
                        job = {
                            'title': card.find('h3', {'class': 'base-search-card__title'}).text.strip(),
                            'company': card.find('h4', {'class': 'base-search-card__subtitle'}).text.strip(),
                            'location': card.find('span', {'class': 'job-search-card__location'}).text.strip(),
                            'link': card.find('a', {'class': 'base-card__full-link'})['href'],
                            'source': 'LinkedIn'
                        }
                        
                        jobs.append(job)
                    except Exception as e:
                        self.logger.warning(f"Error parsing job card: {str(e)}")
                        continue
            
        except Exception as e:
            self.logger.error(f"Error scraping LinkedIn: {str(e)}")
        
        return jobs
    
    def _remove_duplicates(self, jobs: List[Dict]) -> List[Dict]:
        """Remove duplicate job listings"""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = f"{job.get('title', '')}-{job.get('company', '')}-{job.get('location', '')}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs