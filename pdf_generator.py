from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import black, darkblue
import os
from datetime import datetime
import re

class PDFResumeGenerator:
    def __init__(self):
        """Initialize the PDF generator with custom styles"""
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Create custom styles for the resume"""
        # Header style (for name)
        self.styles.add(ParagraphStyle(
            name='ResumeHeader',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=6,
            alignment=TA_CENTER,
            textColor=darkblue,
            fontName='Helvetica-Bold'
        ))
        
        # Subheader style (for contact info)
        self.styles.add(ParagraphStyle(
            name='ContactInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=black
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=6,
            spaceBefore=12,
            textColor=darkblue,
            fontName='Helvetica-Bold'
        ))
        
        # Job title style
        self.styles.add(ParagraphStyle(
            name='JobTitle',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=2,
            fontName='Helvetica-Bold'
        ))
        
        # Company style
        self.styles.add(ParagraphStyle(
            name='Company',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            fontName='Helvetica-Oblique'
        ))
        
        # Regular content style
        self.styles.add(ParagraphStyle(
            name='ResumeContent',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
            leftIndent=20
        ))
        
        # Bullet point style
        self.styles.add(ParagraphStyle(
            name='BulletPoint',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=4,
            leftIndent=20,
            bulletIndent=10
        ))

    def create_resume_pdf(self, resume_data, profile_data=None):
        """
        Create a PDF resume from structured data
        
        Args:
            resume_data (dict): Contains 'formatted_content' and 'sections'
            profile_data (dict): LinkedIn profile data for header
            
        Returns:
            str: Path to the generated PDF file
        """
        try:
            # Create output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = profile_data.get('name', 'Resume').replace(' ', '_') if profile_data else 'Resume'
            filename = f"resume_{name}_{timestamp}.pdf"
            
            # Ensure output directory exists
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)
            
            filepath = os.path.join(output_dir, filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Build PDF content
            story = []
            
            # Add header section
            story.extend(self.create_header_section(profile_data))
            
            # Add main content sections
            if 'sections' in resume_data and resume_data['sections']:
                # Use structured sections if available
                for section_title, content in resume_data['sections'].items():
                    story.extend(self.create_section(section_title, content))
            else:
                # Fallback to parsing raw text
                story.extend(self.parse_resume_text(resume_data.get('formatted_content', '')))
            
            # Build PDF
            doc.build(story)
            
            return filepath
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            raise

    def create_header_section(self, profile_data):
        """Create header section with name and contact info"""
        elements = []
        
        if profile_data:
            # Name
            elements.append(Paragraph(profile_data.get('name', 'Professional Resume'), self.styles['ResumeHeader']))
            
            # Contact info
            contact_info = []
            if profile_data.get('location'):
                contact_info.append(profile_data['location'])
            if profile_data.get('email'):
                contact_info.append(profile_data['email'])
            if profile_data.get('phone'):
                contact_info.append(profile_data['phone'])
            if profile_data.get('url'):
                contact_info.append(profile_data['url'])
            
            if contact_info:
                elements.append(Paragraph(" | ".join(contact_info), self.styles['ContactInfo']))
        
        elements.append(Spacer(1, 12))
        return elements

    def create_section(self, section_title, content):
        """Create a formatted section"""
        elements = []
        
        # Standardize section title
        section_title = section_title.upper()
        
        # Add section header
        elements.append(Paragraph(section_title, self.styles['SectionHeader']))
        
        # Process content based on section type
        if section_title in ['PROFESSIONAL EXPERIENCE', 'WORK EXPERIENCE', 'EXPERIENCE']:
            elements.extend(self.create_experience_section(content))
        elif section_title in ['EDUCATION', 'ACADEMIC BACKGROUND']:
            elements.extend(self.create_education_section(content))
        elif section_title in ['SKILLS', 'TECHNICAL SKILLS']:
            elements.extend(self.create_skills_section(content))
        else:
            # Generic section
            elements.append(Paragraph(content, self.styles['ResumeContent']))
        
        return elements

    def parse_resume_text(self, resume_text):
        """Parse raw resume text into structured elements"""
        story = []
        sections = self.split_into_sections(resume_text)
        
        for section_title, content in sections:
            story.extend(self.create_section(section_title, content))
        
        return story

    def split_into_sections(self, text):
        """Split text into sections based on headers"""
        sections = []
        current_section = ""
        current_content = []
        
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check if line is a section header
            if (line.isupper() and len(line) > 3) or \
               any(line.upper().startswith(header) for header in 
                   ['CONTACT', 'PROFESSIONAL', 'EXPERIENCE', 'EDUCATION', 'SKILLS', 'SUMMARY']):
                
                # Save previous section
                if current_section:
                    sections.append((current_section, '\n'.join(current_content)))
                
                # Start new section
                current_section = line
                current_content = []
            else:
                current_content.append(line)
        
        # Add last section
        if current_section:
            sections.append((current_section, '\n'.join(current_content)))
        
        return sections

    def create_experience_section(self, content):
        """Format experience section"""
        elements = []
        
        if isinstance(content, str):
            # Handle raw text
            entries = content.split('\n\n')
            for entry in entries:
                if entry.strip():
                    elements.append(Paragraph(entry, self.styles['ResumeContent']))
                    elements.append(Spacer(1, 8))
        else:
            # Handle structured data
            for exp in content:
                if 'title' in exp:
                    title = exp['title']
                    if 'company' in exp and exp['company']:
                        title += f" - {exp['company']}"
                    elements.append(Paragraph(title, self.styles['JobTitle']))
                
                if 'description' in exp and exp['description']:
                    # Format bullet points
                    desc = exp['description'].replace('•', '• ')
                    elements.append(Paragraph(desc, self.styles['ResumeContent']))
                
                elements.append(Spacer(1, 8))
        
        return elements

    def create_education_section(self, content):
        """Format education section"""
        elements = []
        
        if isinstance(content, str):
            # Handle raw text
            elements.append(Paragraph(content, self.styles['ResumeContent']))
        else:
            # Handle structured data
            for edu in content:
                if 'degree' in edu and 'school' in edu:
                    text = f"{edu['degree']} - {edu['school']}"
                    if 'dates' in edu:
                        text += f" ({edu['dates']})"
                    elements.append(Paragraph(text, self.styles['ResumeContent']))
                    elements.append(Spacer(1, 6))
        
        return elements

    def create_skills_section(self, content):
        """Format skills section"""
        elements = []
        
        if isinstance(content, list):
            # Handle list of skills
            content = ", ".join(content)
        
        elements.append(Paragraph(content, self.styles['ResumeContent']))
        return elements

# Example usage
if __name__ == "__main__":
    # Test data
    test_resume = {
        'formatted_content': """
JOHN DOE
San Francisco, CA | john.doe@email.com | (123) 456-7890

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years in full-stack development.

EXPERIENCE
Senior Software Engineer - TechCorp (2020-Present)
• Developed scalable web applications
• Improved performance by 40%

EDUCATION
B.S. Computer Science - Stanford University
""",
        'sections': {}
    }

    test_profile = {
        'name': 'John Doe',
        'location': 'San Francisco, CA',
        'email': 'john.doe@email.com',
        'phone': '(123) 456-7890'
    }

    generator = PDFResumeGenerator()
    pdf_path = generator.create_resume_pdf(test_resume, test_profile)
    print(f"PDF generated at: {pdf_path}")