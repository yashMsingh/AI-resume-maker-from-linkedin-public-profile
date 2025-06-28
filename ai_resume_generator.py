import os
from dotenv import load_dotenv
import google.generativeai as genai
import json

# Load environment variables
load_dotenv()

class ResumeGenerator:
    def __init__(self):
        """Initialize the AI resume generator with Gemini API"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # Try different model names (most likely working ones first)
        self.model = None
        model_names = [
            'gemini-1.5-flash',
            'gemini-1.5-pro',
            'models/gemini-1.5-flash', 
            'models/gemini-1.5-pro'
        ]
        
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                # Test the model with a simple request
                test_response = self.model.generate_content("Hello")
                print(f"✅ Using model: {model_name}")
                break
            except Exception as e:
                print(f"❌ Model {model_name} failed: {str(e)}")
                continue
        
        if not self.model:
            raise ValueError("No working Gemini model found")
    
    def generate_resume_content(self, profile_data, job_title=None):
        """Generate professional resume content using AI"""
        try:
            # Create detailed prompt for resume generation
            prompt = self.create_resume_prompt(profile_data, job_title)
            
            print("🤖 Generating resume content with AI...")
            response = self.model.generate_content(prompt)
            
            if response.text:
                return self.parse_resume_response(response.text)
            else:
                return self.create_fallback_resume(profile_data)
                
        except Exception as e:
            print(f"AI generation error: {str(e)}")
            return self.create_fallback_resume(profile_data)
    
    def create_resume_prompt(self, profile_data, job_title):
        """Create a detailed prompt for AI resume generation"""
        job_focus = f" for a {job_title} position" if job_title else ""
        
        prompt = f"""
        Create a professional resume{job_focus} based on the following LinkedIn profile data:

        Name: {profile_data.get('name', 'Not provided')}
        Current Role: {profile_data.get('headline', 'Not provided')}
        Location: {profile_data.get('location', 'Not provided')}
        About: {profile_data.get('about', 'Not provided')}

        Experience:
        {self.format_experience_for_prompt(profile_data.get('experience', []))}

        Education:
        {self.format_education_for_prompt(profile_data.get('education', []))}

        Skills: {', '.join(profile_data.get('skills', []))}

        Please create a professional resume with the following sections:
        1. PROFESSIONAL SUMMARY (2-3 sentences highlighting key strengths)
        2. CORE COMPETENCIES (bullet points of key skills)
        3. PROFESSIONAL EXPERIENCE (detailed bullet points with achievements)
        4. EDUCATION
        5. TECHNICAL SKILLS

        Guidelines:
        - Use action verbs and quantifiable achievements where possible
        - Keep bullet points concise but impactful
        - Tailor content to be ATS-friendly
        - Make it professional and modern
        - Focus on results and impact

        Format the response as structured text with clear section headers.
        """
        
        return prompt
    
    def format_experience_for_prompt(self, experiences):
        """Format experience data for the AI prompt"""
        if not experiences:
            return "No experience data provided"
        
        formatted = []
        for exp in experiences:
            exp_text = f"- {exp.get('title', 'Unknown')}"
            if exp.get('company'):
                exp_text += f" at {exp['company']}"
            if exp.get('description'):
                exp_text += f": {exp['description']}"
            formatted.append(exp_text)
        
        return '\n'.join(formatted)
    
    def format_education_for_prompt(self, education):
        """Format education data for the AI prompt"""
        if not education:
            return "No education data provided"
        
        formatted = []
        for edu in education:
            edu_text = f"- {edu.get('degree', 'Unknown degree')}"
            if edu.get('school'):
                edu_text += f" from {edu['school']}"
            formatted.append(edu_text)
        
        return '\n'.join(formatted)
    
    def parse_resume_response(self, ai_response):
        """Parse AI response into structured resume data"""
        try:
            # Split response into sections
            sections = {}
            current_section = None
            current_content = []
            
            lines = ai_response.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if line is a section header
                if any(header in line.upper() for header in [
                    'PROFESSIONAL SUMMARY', 'SUMMARY', 'OBJECTIVE',
                    'CORE COMPETENCIES', 'SKILLS', 'TECHNICAL SKILLS',
                    'PROFESSIONAL EXPERIENCE', 'EXPERIENCE', 'WORK EXPERIENCE',
                    'EDUCATION', 'ACADEMIC BACKGROUND'
                ]):
                    if current_section:
                        sections[current_section] = '\n'.join(current_content)
                    current_section = line
                    current_content = []
                else:
                    current_content.append(line)
            
            # Add last section
            if current_section:
                sections[current_section] = '\n'.join(current_content)
            
            return {
                'formatted_content': ai_response,
                'sections': sections
            }
            
        except Exception as e:
            print(f"Error parsing AI response: {str(e)}")
            return {
                'formatted_content': ai_response,
                'sections': {}
            }
    
    def create_fallback_resume(self, profile_data):
        """Create a basic resume if AI generation fails"""
        print("🔄 Creating fallback resume...")
        
        resume_content = f"""
{profile_data.get('name', 'Your Name')}
{profile_data.get('location', 'Location')}

PROFESSIONAL SUMMARY
{profile_data.get('about', 'Professional with experience in various roles and responsibilities.')}

PROFESSIONAL EXPERIENCE
"""
        
        # Add experiences
        for exp in profile_data.get('experience', []):
            resume_content += f"\n{exp.get('title', 'Position')}"
            if exp.get('company'):
                resume_content += f" | {exp['company']}"
            if exp.get('description'):
                resume_content += f"\n• {exp['description']}"
            resume_content += "\n"
        
        # Add education
        if profile_data.get('education'):
            resume_content += "\nEDUCATION\n"
            for edu in profile_data['education']:
                resume_content += f"{edu.get('degree', 'Degree')} | {edu.get('school', 'Institution')}\n"
        
        # Add skills
        if profile_data.get('skills'):
            resume_content += f"\nSKILLS\n{', '.join(profile_data['skills'])}\n"
        
        return {
            'formatted_content': resume_content.strip(),
            'sections': {}
        }

# Test function
if __name__ == "__main__":
    try:
        generator = ResumeGenerator()
        
        # Test data
        test_profile = {
            'name': 'Test User',
            'headline': 'Software Developer',
            'about': 'Experienced developer with passion for creating innovative solutions',
            'experience': [
                {
                    'title': 'Senior Developer',
                    'company': 'Tech Corp',
                    'description': 'Led development of web applications'
                }
            ],
            'education': [
                {
                    'degree': 'Computer Science',
                    'school': 'University'
                }
            ],
            'skills': ['Python', 'JavaScript', 'React']
        }
        
        result = generator.generate_resume_content(test_profile, "Full Stack Developer")
        print("✅ Resume generated successfully!")
        print("\n" + "="*50)
        print(result['formatted_content'])
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")