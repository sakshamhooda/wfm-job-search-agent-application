# Resume-Based Job Search Application

An MVP application that analyzes resumes, extracts key information, and searches for matching job opportunities across multiple job boards. The application uses AI-powered agents to optimize search strategies and rank job matches.

## Features

- Resume parsing (PDF and DOCX support)
- Keyword-based job search
- AI-powered job matching
- Multiple job board integration
- Export results in CSV and Markdown formats
- Interactive web interface using Streamlit

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume-job-search.git
cd resume-job-search
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```
Edit `.env` and add your Anthropic API key.

## Usage

1. Start the Streamlit application:
```bash
streamlit run src/app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically `http://localhost:8501`).

3. Upload your resume (PDF or DOCX format).

4. Enter additional keywords for skills, job titles, and locations (optional).

5. Click "Search Jobs" to start the search process.

6. View results and download them in CSV or Markdown format.

## Project Structure

```
resume-job-search/
├── src/
│   ├── app.py                 # Main Streamlit application
│   ├── agents/
│   │   ├── search_strategy.py # Search query optimization
│   │   ├── web_scraper.py    # Job board scraping
│   │   └── filtering.py      # Result filtering and ranking
│   └── utils/
│       ├── resume_parser.py   # Resume parsing
│       └── data_processor.py  # Data formatting
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # Project documentation
```

## Development

### Adding New Job Boards

To add support for a new job board:

1. Add the new job board URL to `WebScraperAgent.job_boards`
2. Create a new parsing method in `WebScraperAgent` (e.g., `_parse_newboard`)
3. Add appropriate error handling and rate limiting

### Enhancing Resume Parsing

The resume parser can be enhanced by:

1. Adding more sophisticated section detection
2. Implementing better skills extraction
3. Adding support for more file formats
4. Improving education and experience parsing

### Improving Job Matching

To improve job matching:

1. Fine-tune the Claude prompts in `FilteringAgent`
2. Add more matching criteria
3. Implement custom scoring algorithms
4. Add support for industry-specific matching

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Claude API by Anthropic for AI-powered job matching
- Streamlit for the web interface
- Beautiful Soup for web scraping