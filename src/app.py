import streamlit as st
import pandas as pd
from utils.resume_parser import ResumeParser
from utils.data_processor import DataProcessor
from agents.search_strategy import SearchStrategyAgent
from agents.web_scraper import WebScraperAgent
from agents.filtering import FilteringAgent

def main():
    st.title("Resume-Based Job Search")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Resume Input")
        input_method = st.radio(
            "Choose input method",
            ["Upload Resume", "Manual Entry"]
        )
        
        if input_method == "Upload Resume":
            resume_file = st.file_uploader("Choose your resume", type=["pdf", "docx", "txt"])
        else:
            st.write("Enter your resume details below:")
            resume_text = st.text_area(
                "Resume Text",
                height=300,
                placeholder="Paste or type your resume content here..."
            )
        
        st.header("Keywords")
        skills = st.text_input("Skills (comma-separated)")
        job_titles = st.text_input("Desired Job Titles (comma-separated)")
        locations = st.text_input("Preferred Locations (comma-separated)")
    
    # Main content area
    try:
        # Process resume based on input method
        resume_parser = ResumeParser()
        if input_method == "Upload Resume" and resume_file is not None:
            resume_data = resume_parser.parse(resume_file)
        elif input_method == "Manual Entry" and 'resume_text' in locals() and resume_text.strip():
            resume_data = resume_parser.parse_text(resume_text)
        else:
            st.info("Please provide your resume to start the job search.")
            return
            
        # Display parsed resume data
        st.header("Parsed Resume Information")
        st.write(resume_data)
        
        # Initialize agents
        search_agent = SearchStrategyAgent()
        scraper_agent = WebScraperAgent()
        filter_agent = FilteringAgent()
        
        # Process job search
        if st.button("Search Jobs"):
            with st.spinner("Searching for matching jobs..."):
                # Get search queries
                search_queries = search_agent.generate_queries(
                    resume_data,
                    skills.split(",") if skills else [],
                    job_titles.split(",") if job_titles else [],
                    locations.split(",") if locations else []
                )
                
                # Scrape job listings
                job_listings = scraper_agent.scrape_jobs(search_queries)
                
                # Filter and rank jobs
                filtered_jobs = filter_agent.filter_jobs(job_listings, resume_data)
                
                # Convert to DataFrame
                df = pd.DataFrame(filtered_jobs)
                
                # Display results
                st.header("Job Matches")
                st.dataframe(df)
                
                # Download buttons
                st.download_button(
                    label="Download as CSV",
                    data=df.to_csv(index=False),
                    file_name="job_matches.csv",
                    mime="text/csv"
                )
                
                # Generate markdown
                markdown_content = DataProcessor.generate_markdown(filtered_jobs)
                st.download_button(
                    label="Download as Markdown",
                    data=markdown_content,
                    file_name="job_matches.md",
                    mime="text/markdown"
                )
                    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()