# 📝 LinkedIn AI Resume Generator

An AI-powered web application that automatically scrapes your LinkedIn profile, generates tailored resume content using AI, and exports a professional PDF resume – all through a simple web interface!

---

## 🚀 Features

- 🔗 **LinkedIn Profile Scraping**  
  Extracts key details like experience, education, skills, and certifications.

- 🤖 **AI-Powered Resume Content Generation**  
  Uses AI (OpenAI / Gemini API) to rewrite and enhance your LinkedIn data.

- 📄 **PDF Resume Export**  
  Converts the generated resume into a well-formatted PDF.

- 🌐 **Flask-based Web App**  
  A simple user interface to input LinkedIn URLs and download resumes.

- 🕒 **Session-wise Progress Tracking**  
  Tracks each user's resume generation process.

---

## 📥 How to Get the Project

👉 **[Download the Full Project as a ZIP]](https://github.com/yashMsingh/AI-resume-maker-from-linkedin-public-profile/blob/main/linkedin-20250628T063449Z-1-001.zip))**  

Unzip the folder to view the complete project structure and files.

---

## 📂 Project Structure

```
linkedin-ai-resume-generator/
├── app.py                  # Flask backend
├── ai_resume_generator.py  # AI-based resume content logic
├── linkedin_scraper.py     # LinkedIn scraping logic
├── pdf_generator.py        # PDF conversion
├── templates/              # HTML templates for Flask
├── generated_resumes/      # Output folder for generated PDFs
├── output/                 # Temporary outputs
├── .env                    # API keys and configs
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## ⚙️ Setup Instructions

1. **Unzip the downloaded folder.**

2. **Go to the project directory:**

```bash
cd linkedin-ai-resume-generator
```

3. **Install all Python dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create a `.env` file** (for your API keys):

```
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
```

5. **Run the Flask app:**

```bash
python app.py
```

Visit:  
`http://localhost:5000`

---

## ✅ How It Works:

1. Open the web app.
2. Paste your LinkedIn profile URL.
3. Enter a job title (optional).
4. Click **Generate Resume**.
5. Download your professionally generated PDF.

---

## 📌 Current Limitations

- LinkedIn scraping may break if LinkedIn updates their site structure.
- AI-generated content may not always match human tone (manual tweaks may be needed).
- The UI is still basic and needs improvement.

---

## 🛠️ What Needs Improvement (And Where I Need Help 👇)

- **Improve the frontend UI/UX**
- **Add error handling for failed LinkedIn scraping**
- **Make the AI-generated content more customizable**
- **Deploy on a free cloud service (like Render or Heroku)**
- **Implement asynchronous processing for long jobs**
- **Add more resume design templates**

If you’re a developer, designer, or just someone interested in resume tech, **I would love your feedback, suggestions, or contributions!** 😊

---

## 🤝 Contributions Welcome!

Pull requests, bug reports, suggestions for improvement — all are appreciated!  
Feel free to fork, improve, and raise issues.

---


