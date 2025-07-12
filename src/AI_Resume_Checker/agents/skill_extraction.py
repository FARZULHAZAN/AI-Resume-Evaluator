from typing import List, Dict, Any
import os
import requests
import logging
import json
import re
from pydantic import BaseModel
from src.AI_Resume_Checker.config.settings import settings
from langchain.document_loaders import PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


    


class SkillExtractor:
    """Class for extracting skills from resume text using LLMFoundry REST API."""

    def __init__(self,file_path):
        """
        Initialize the SkillExtractor.
        """
        self.skills=[]
        self.content=""
        try:
            self.file_path=file_path
            #token = os.environ['LLMFOUNDRY_TOKEN']
            self.llm_url = "https://llmfoundry.straive.com/gemini/v1beta/openai/chat/completions"
            self.llm_headers = {"Authorization": f"Bearer {settings.gemini_api_key}:my-test-project",
                "Content-Type": "application/json"
            }
            logger.info("Initialized SkillExtractor with LLMFoundry REST API.")
        except KeyError as e:
            logger.error(f"Environment variable {e} not set.")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize SkillExtractor: {str(e)}")
            raise
    def convert_to_txt(self) -> str:
            """
            Convert PDF, TXT, or DOCX file to plain text using LangChain loaders.

            Args:
                file_path (str): Path to the input file.

            Returns:
                str: Extracted plain text content.
            """
            ext = os.path.splitext(self.file_path)[1].lower()

            if ext == ".pdf":
                loader = PyPDFLoader(self.file_path)
            elif ext == ".txt":
                loader = TextLoader(self.file_path)
            elif ext == ".docx":
                loader = UnstructuredWordDocumentLoader(self.file_path)
            else:
                raise ValueError("Unsupported file format. Only PDF, TXT, and DOCX are supported.")

            documents = loader.load()
            self.content = "\n".join(doc.page_content for doc in documents)
            return self.content

    def extract_skills(self):
        """
        Extract skills from resume text using LLMFoundry.
        """
        
        try:
            system_prompt = (
        "You are an AI assistant that specializes in accurately extracting individual skills from resumes. "
        "Your sole purpose is to identify and list every distinct skill a candidate has mentioned. "
        "Do not group or summarize skills into categories. Each skill must be listed individually. "
        "Ignore all non-skill information such as personal details, company names, job titles, dates of employment, "
        "and general descriptions of past roles or projects. Focus solely on the abilities and competencies mentioned. "
        "Extract all skills the candidate has listed or demonstrated in their experience, education, or a dedicated skills section. "
        "Do not hallucinate or invent skills not present in the text."
    )

            user_prompt = {
        "instruction": (
            f"From the following resume text, extract all individual skills. Do not generalize.\n\n{self.content}\n\n"
            "Focus on specific, individual skills (e.g., technical, software, soft, or domain-specific). Extract every distinct skill mentioned. "
            "Do not group skills into categories like 'Programming Languages' or 'Soft Skills'. For example, if you see Python, Java, and C++, extract them as 'python', 'java', and 'c++' individually. "
            "Ignore all non-skill text, including the candidate's name, contact information, company names, job titles (like 'Software Engineer'), employment dates, university names, and descriptions of responsibilities that don't name a specific skill. "
            "List each skill separately. For example: 'python', 'react', 'project management', 'agile methodologies', 'data analysis', 'public speaking'. "
            "Output only a flat JSON list of skill names as lowercase strings. Do not include any other text, explanations, or formatting."
        ),
        "search_results": self.content, # The resume text goes here
        "sample_output_format": ["skill1", "skill2", "skill3"]
    }


            payload = {
                    "model": "gemini-2.5-pro",
                    "temperature": 0.2,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": json.dumps(user_prompt)}
                    ]
                }


            response = requests.post(self.llm_url, 
            headers=self.llm_headers,
            json=payload, timeout=30)
                
            
            if response.status_code != 200:
                #logger.error(f"LLM API call failed with status code {response.status_code}: {response.text}")
                return []

            reply_text = response.json()["choices"][0]["message"]["content"].strip()

            # Remove markdown formatting if present
            cleaned_reply = re.sub(r"```(?:json)?|```", "", reply_text).strip()
        
            try:
                skills_list = json.loads(cleaned_reply)

                if not isinstance(skills_list, list) or not all(isinstance(s, str) for s in skills_list):
                    raise ValueError("LLM output is not a list of strings")
                self.skills=[s for s in skills_list]
                return self.skills

            except Exception as e:
                #logger.error(f"Unexpected error while processing LLM output: {e}")

                return []

        except Exception as e:
            #logger.exception(f"Error during LLM skill extraction: {e}")
            return []
        

# Example usage
