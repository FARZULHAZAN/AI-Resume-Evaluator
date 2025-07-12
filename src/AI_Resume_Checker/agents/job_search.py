
from typing import List, Dict, Any,Optional
import os
import requests
import logging
import json
import re
from pydantic import BaseModel
from src.AI_Resume_Checker.config.settings import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)




    

class JobSearchAgent:
    """Class for searching and extracting job requirements using Tavily Search API and LLMFoundry."""

    def __init__(self, job_role: str, experiance: int, jd: Optional[str] = None):
    
        self.search_results = []
        self.job_role = job_role
        self.experiance = experiance
        self.jd = jd
        try:
            
            self.llm_url = "https://llmfoundry.straive.com/gemini/v1beta/openai/chat/completions"
            self.llm_headers = {"Authorization": f"Bearer {settings.gemini_api_key}:my-test-project",
                "Content-Type": "application/json"
            }
            logger.info("Initialized JobSearchAgent with SERPAPI and LLMFoundry API.")
        except Exception as e:
            logger.error(f"Failed to initialize JobSearchAgent: {str(e)}")
            raise
            

    def search_job_description(self) -> Dict[str, Any]:
            """Search for job descriptions using JSearch API via RapidAPI."""
              # Assuming this is a number (e.g., 3)

            try:
                url = "https://jsearch.p.rapidapi.com/search"
                headers = {
                    "x-rapidapi-key": settings.x_rapidapi_key,
                    "x-rapidapi-host": "jsearch.p.rapidapi.com"
                }
                query = f"{self.job_role} with {self.experiance} years experience"
                params = {
                    "query": query,
                    "num_pages": "1"
                }

                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()  # Raises HTTPError if the request fails
                data = response.json()

                # Extract top 3 job descriptions
                job_descriptions = []
                for job in data.get("data", [])[:3]:
                    description = job.get("job_description", "")
                    if description:
                        job_descriptions.append(description)

                # Combine descriptions into one string
                self.search_result = "\n\n".join(job_descriptions)

                # Call your existing LLM-based extractor
                return self._call_llm_and_extract(self.search_result, self.job_role, self.experiance)

            except Exception as e:
                print(f"Error occurred in JSearch API: {e}")
                return {}

                
    
   

    def extract_from_uploaded_jd(self):
        """Extract job requirements directly from user-uploaded JD."""
        job_role=self.job_role
        experiance=self.experiance
        jd_text=self.jd
        logger.info("Extracting job requirements from uploaded JD")
        text = jd_text.strip()
        if len(text) > 15000:
            text = text[:15000] + "..."
        return self._call_llm_and_extract(text, job_role, experiance)

    def _call_llm_and_extract(self, input_text: str, job_role: str, experiance: int):
            job_role=self.job_role
            experiance=self.experiance
            """
            Internal helper to send job description text to the LLM and extract a list of required skills.

            Args:
                input_text (str): The job description or search results text.
                job_role (str): The role/title of the job.
                experiance (int): Years of experience for the role.

            Returns:
                List[JobRequirement]: A list of JobRequirement instances, each containing a skill name.
            """
            try:
                # Define system and user prompts
                system_prompt = (
                    "You are an AI assistant that specializes in accurately extracting only the required skills "
                    "from job descriptions and related text. Ignore unrelated information like company details, "
                    "job perks, responsibilities, or general statements. Extract all relevant skills explicitly or "
                    "implicitly mentioned as required for the role. Do not hallucinate or invent skills."
                )

                user_prompt = {
                    "instruction": (
                        f"Extract all required skills for the role of {job_role} with {experiance} years of experience. "
                        "Focus only on skills (technical, soft, or domain-specific) explicitly or strongly implied as required. "
                        "Ignore unrelated text such as company information, benefits, responsibilities, or qualifications that are not skills. "
                        "Output only a JSON list of skill names as strings, with no additional text or formatting."
                    ),
                    "search_results": input_text,
                    "output_format": ['skill1','skill2']
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
                    
                    return [s for s in skills_list]

                except Exception as e:
                    #logger.error(f"Unexpected error while processing LLM output: {e}")

                    return []

            except Exception as e:
                #logger.exception(f"Error during LLM skill extraction: {e}")
                return []
            
