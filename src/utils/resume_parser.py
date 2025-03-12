import PyPDF2
from docx import Document
import io
import re
from datetime import datetime

class ResumeParser:
    def parse(self, file):
        """
        Parse resume file (PDF, DOCX, or TXT) and extract relevant information
        
        Args:
            file: Streamlit UploadedFile object
        
        Returns:
            dict: Parsed resume data
        """
        # Read file content
        content = self._read_file(file)
        return self._process_content(content)
    
    def parse_text(self, text):
        """
        Parse manually entered resume text
        
        Args:
            text (str): Raw resume text
        
        Returns:
            dict: Parsed resume data
        """
        return self._process_content(text)
    
    def _read_file(self, file):
        """Read content from PDF, DOCX, or TXT file"""
        file_type = file.name.split('.')[-1].lower()
        content = ""
        
        try:
            if file_type == 'pdf':
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                for page in pdf_reader.pages:
                    content += page.extract_text() + "\n"
            
            elif file_type == 'docx':
                doc = Document(io.BytesIO(file.read()))
                for para in doc.paragraphs:
                    content += para.text + "\n"
            
            elif file_type == 'txt':
                content = file.read().decode('utf-8')
            
            return content.strip()
            
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
    
    def _process_content(self, content):
        """Process resume content and extract information"""
        sections = self._extract_sections(content)
        skills = self._extract_skills(content, sections)
        experience = self._extract_experience(content, sections)
        education = self._extract_education(content, sections)
        
        return {
            'raw_text': content,
            'sections': sections,
            'skills': skills,
            'experience': experience,
            'education': education
        }
    
    def _extract_sections(self, content):
        """Extract different sections from resume content"""
        sections = {
            'header': '',
            'summary': '',
            'skills': '',
            'experience': '',
            'education': '',
            'other': ''
        }
        
        # Common section headers
        section_patterns = {
            'summary': r'(?i)(summary|objective|profile)',
            'skills': r'(?i)(skills|technologies|technical expertise)',
            'experience': r'(?i)(experience|employment|work history)',
            'education': r'(?i)(education|academic|qualifications)'
        }
        
        # Split content into lines
        lines = content.split('\n')
        current_section = 'header'
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line is a section header
            matched_section = None
            for section, pattern in section_patterns.items():
                if re.match(pattern, line, re.IGNORECASE):
                    matched_section = section
                    break
            
            if matched_section:
                current_section = matched_section
                sections[current_section] = ''
            else:
                sections[current_section] += line + '\n'
        
        return sections
    
    def _extract_skills(self, content, sections):
        """Extract skills from resume content"""
        skills = set()
        
        # Look for skills in the skills section if it exists
        skills_text = sections.get('skills', '')
        if skills_text:
            # Split by common delimiters
            skill_candidates = re.split(r'[,•|/]', skills_text)
            skills.update([s.strip() for s in skill_candidates if s.strip()])
        
        # Common technical skills to look for throughout the resume
        common_skills = [
            # Programming Languages
            'python', 'java', 'javascript', 'c++', 'ruby', 'php',
            # Web Technologies
            'html', 'css', 'react', 'angular', 'vue', 'node.js',
            # Frameworks
            'django', 'flask', 'spring', 'express',
            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis',
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            # Other
            'git', 'agile', 'scrum', 'jira', 'machine learning'
        ]
        
        # Look for common skills throughout the resume
        content_lower = content.lower()
        for skill in common_skills:
            if skill in content_lower:
                skills.add(skill)
        
        return sorted(list(skills))
    
    def _extract_experience(self, content, sections):
        """Extract work experience from resume content"""
        experience = []
        
        # Get experience section
        exp_text = sections.get('experience', '')
        if not exp_text:
            return experience
        
        # Try to split into different positions
        positions = re.split(r'\n(?=[A-Z])', exp_text)
        
        for position in positions:
            position = position.strip()
            if not position:
                continue
                
            exp_entry = {
                'title': '',
                'company': '',
                'duration': '',
                'description': ''
            }
            
            lines = position.split('\n')
            if not lines:
                continue
                
            # First line usually contains title and company
            first_line = lines[0]
            title_company = first_line.split(' at ')
            if len(title_company) >= 2:
                exp_entry['title'] = title_company[0].strip()
                exp_entry['company'] = title_company[1].strip()
            else:
                exp_entry['title'] = first_line
            
            # Look for dates
            date_pattern = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s*\d{4}'
            dates = re.findall(date_pattern, position)
            if len(dates) >= 2:
                exp_entry['duration'] = f"{dates[0]} - {dates[1]}"
            elif len(dates) == 1:
                exp_entry['duration'] = f"{dates[0]} - Present"
            
            # Rest is description
            exp_entry['description'] = '\n'.join(lines[1:]).strip()
            
            experience.append(exp_entry)
        
        return experience
    
    def _extract_education(self, content, sections):
        """Extract education information from resume content"""
        education = []
        
        # Get education section
        edu_text = sections.get('education', '')
        if not edu_text:
            return education
        
        # Split into different educational entries
        entries = re.split(r'\n(?=[A-Z])', edu_text)
        
        for entry in entries:
            entry = entry.strip()
            if not entry:
                continue
            
            edu_entry = {
                'degree': '',
                'institution': '',
                'year': '',
                'details': ''
            }
            
            lines = entry.split('\n')
            if not lines:
                continue
            
            # First line usually contains degree and institution
            first_line = lines[0]
            parts = first_line.split(',')
            if len(parts) >= 2:
                edu_entry['degree'] = parts[0].strip()
                edu_entry['institution'] = parts[1].strip()
            else:
                edu_entry['institution'] = first_line
            
            # Look for years
            year_pattern = r'\b20\d{2}\b'
            years = re.findall(year_pattern, entry)
            if years:
                edu_entry['year'] = years[0]
            
            # Rest is details
            edu_entry['details'] = '\n'.join(lines[1:]).strip()
            
            education.append(edu_entry)
        
        return education