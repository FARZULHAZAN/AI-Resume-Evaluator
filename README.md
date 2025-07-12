# AI Resume Evaluator

![AI Resume Checker](https://img.shields.io/badge/AI-Resume%20Checker-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32.0+-red)
![LangGraph](https://img.shields.io/badge/LangGraph-0.0.25+-orange)

A powerful AI-driven application that analyzes your resume against job requirements, providing a skill match score and personalized recommendations to improve your job application success rate.

## 📋 Overview

AI Resume Checker helps job seekers optimize their resumes for specific job roles by:

1. Extracting skills from your resume
2. Finding relevant job descriptions based on your target role
3. Comparing your skills against job requirements
4. Calculating a match percentage
5. Providing actionable recommendations for skills to add or improve

The system uses advanced AI models to understand the conceptual meaning of skills, ensuring accurate matching beyond simple keyword comparison.

## ✨ Features

- **Resume Parsing**: Supports PDF, DOCX, and TXT formats
- **Skill Extraction**: Automatically identifies technical and soft skills from your resume
- **Job Description Analysis**: Either searches for relevant job descriptions or uses a provided one
- **Intelligent Skill Comparison**: Matches skills based on conceptual equivalence, not just exact text
- **Match Score**: Provides a percentage match between your resume and job requirements
- **Personalized Recommendations**: Suggests specific skills to learn or highlight
- **User-Friendly Interface**: Simple Streamlit UI for easy interaction

## 🏗️ Architecture

The application is built using a modular architecture with LangGraph for workflow orchestration:

```
AI Resume Checker
├── Frontend (Streamlit)
├── Workflow (LangGraph)
│   ├── ExtractResumeSkills Node
│   ├── ExtractJobSkills Node
│   └── CompareAndRecommend Node
└── Agents
    ├── SkillExtractor
    ├── JobSearchAgent
    └── SkillsComparisonEngine
```

### Components

- **Frontend**: Streamlit-based user interface for file upload and displaying results
- **Workflow**: LangGraph-powered workflow that orchestrates the analysis process
- **Agents**:
  - **SkillExtractor**: Extracts skills from resume documents
  - **JobSearchAgent**: Searches for job descriptions or processes provided ones
  - **SkillsComparisonEngine**: Compares resume skills with job requirements

## 🚀 Installation

### Prerequisites

- Python 3.8+
- API keys for:
  - Gemini API (for LLM capabilities)
  - RapidAPI (for job search functionality)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-resume-checker.git
   cd ai-resume-checker
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your API keys:
   ```
   GEMINI_API_KEY=your_gemini_api_key
   x_rapidapi_key=your_rapidapi_key
   LANGSMITH_API_KEY=your_langsmith_api_key
   LANGSMITH_PROJECT=your_langsmith_project
   LANGSMITH_TRACING=true
   ```

## 💻 Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the provided URL (typically http://localhost:8501)

3. Upload your resume (PDF, DOCX, or TXT format)

4. Enter your target job role and years of experience

5. Optionally, paste a specific job description if you have one

6. Click "Analyze Resume" to start the analysis

7. View your match score and skill recommendations

## ⚙️ Configuration

The application can be configured through the `settings.py` file or environment variables:

- **API Keys**: Set your API keys in the `.env` file
- **File Types**: Supported file types can be modified in settings
- **Max File Size**: Default is 10MB, can be adjusted in settings
- **UI Settings**: Page title, icon, and layout can be customized

## 🔧 Technologies Used

- **Streamlit**: For the web interface
- **LangGraph**: For workflow orchestration
- **LangChain**: For document processing
- **Gemini API**: For AI-powered skill extraction and comparison
- **RapidAPI/JSearch**: For job description search
- **PyPDF2/python-docx**: For document parsing
- **Pandas**: For data manipulation
- **Pydantic**: For data validation and settings management

## 🧪 Monitoring & Debugging

For in-memory testing of the LangGraph workflow:

```bash
langgraph-cli run --inmem
```
## Demo 
[Demo](https://drive.google.com/drive/folders/1A_RV3_C5frozmTwyV-67nmiF1PvcUyiF?usp=sharing)

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you have any questions or need help, please open an issue in the repository.
