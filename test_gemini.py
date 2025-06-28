import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    print("❌ API key not found in .env file")
    print("Make sure your .env file contains: GOOGLE_API_KEY=your_actual_key")
else:
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # First, list available models
        print("📋 Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  ✅ {model.name}")
        
        # Try different model names
        model_names = [
            'gemini-1.5-flash',
            'gemini-1.5-pro', 
            'gemini-pro',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro'
        ]
        
        for model_name in model_names:
            try:
                print(f"\n🧪 Testing model: {model_name}")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say hello world")
                
                print("✅ Gemini API is working!")
                print(f"✅ Working model: {model_name}")
                print(f"Response: {response.text}")
                break
                
            except Exception as model_error:
                print(f"❌ {model_name} failed: {str(model_error)}")
                continue
        else:
            print("❌ No working models found")
        
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        print("Check if your API key is correct")