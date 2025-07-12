import os
import requests
import json
import logging
import re
from typing import Any,Optional
from src.AI_Resume_Checker.state.state import ResumeState
from src.AI_Resume_Checker.config.settings import settings
from src.AI_Resume_Checker.agents.skill_extraction import SkillExtractor
from src.AI_Resume_Checker.agents.job_search import JobSearchAgent
import pandas as pd
# Logging setup


# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



# ✅ Main class
class SkillsComparisonEngine:
    def __init__(self, state: ResumeState):
        self.path = state["path"]
        self.df = pd.DataFrame()
        self.job_role = state["job_role"]
        self.experiance = state["experience"]
        self.job_skills = []

        # ✅ Extract resume skills
        self.skill = SkillExtractor(self.path)
        self.skills = self.skill.extract_skills()

        # ✅ Handle job description
        if state.get("job_description"):
            self.jd = state["job_description"]
            self.jobs = JobSearchAgent(self.job_role, self.experiance, self.jd)
            self.job_skills = self.jobs.extract_from_uploaded_jd()
        else:
            self.jobs = JobSearchAgent(self.job_role, self.experiance)
            self.job_skills = self.jobs.search_job_description()


        # ✅ Setup LLM call
        try:
            self.llm_url = "https://llmfoundry.straive.com/gemini/v1beta/openai/chat/completions"
            self.llm_headers = {
                "Authorization": f"Bearer {os.getenv('GEMINI_API_KEY')}:my-test-project",
                "Content-Type": "application/json"
            }
            logger.info("Initialized SkillsComparisonEngine.")
        except Exception as e:
            logger.error(f"Failed to initialize SkillsComparisonEngine: {e}")
            raise

    def _call_llm(self, system_prompt: str, user_prompt: Any, temperature: float = 0.2) -> Any:
        payload = {
            "model": "gemini-2.5-pro",
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt)}
            ]
        }

        try:
            response = requests.post(self.llm_url, headers=self.llm_headers, json=payload)
            if response.status_code != 200:
                logger.error(f"LLM API Error {response.status_code}: {response.text[:300]}")
                return None

            reply_text = response.json()["choices"][0]["message"]["content"].strip()
            cleaned = re.sub(r"```(?:json)?|```", "", reply_text).strip()
            return json.loads(cleaned) if cleaned.startswith("[") or cleaned.startswith("{") else cleaned
        except Exception as e:
            logger.error(f"LLM call error: {e}")
            return None

    def compare_skills(self) -> pd.DataFrame:
        system_prompt = (
            """You are a Conceptually-Aware Skill Matching AI. Your task is to perform a sophisticated comparison between candidate skills and job requirements by understanding the underlying meaning of each skill.

Your primary goal is to determine if a candidate's skill is a **conceptual equivalent** of a job requirement, resulting in a definitive 'exact' or 'missing' status.

A skill is considered an 'exact' match if it meets one of the following criteria of conceptual equivalence:
1.  **Identical Match:** The strings are the same (e.g., 'Python' and 'Python').
2.  **Abbreviations and Full Forms:** One skill is a common industry abbreviation of the other (e.g., 'LLM' and 'Large Language Models'; 'NLP' and 'Natural Language Processing').
3.  **Well-known Synonyms:** The skills are different words for the same concept (e.g., 'Teamwork' and 'Collaboration'; 'Data Mining' and 'Knowledge Discovery').
4.  **Core Skill Equivalence:** One skill is a minor variation or superset that fully encompasses the other (e.g., a candidate's 'Python' skill is a match for a 'Python Scripting' requirement).

**Crucially, what is NOT a match:**
- Do NOT classify a specific tool as a match for a general skill category (e.g., 'Excel' is not a conceptual match for 'Data Analysis').
- Do NOT match related but distinct skills (e.g., 'React' is not a match for 'Vue.js').

For each job requirement, you must check all candidate skills to find a conceptual equivalent. If one is found, it's 'exact'. If, after checking all skills, no conceptual equivalent is found, it is 'missing'. There is no middle ground."""
        )

        user_prompt = {
            "instruction": "Analyze the candidate's skills against job requirements based on their conceptual meaning. For each job skill, determine if a conceptually equivalent skill exists in the candidate's list and classify it as 'exact' or 'missing'.",
            "candidate_skills": self.skills,
            "job_requirements": self.job_skills,
            "output_format": [
                {
                    "job_requirement": "The skill name from the job_requirements list.",
                    "match_status": "exact | missing",
                    "matching_candidate_skill": "The skill name from candidate_skills",
                    "recommendation": "Actionable advice for the candidate to acquire the skill. Provide only when 'match_status' is 'missing'."
                }
            ]
        }

        result = self._call_llm(system_prompt, user_prompt)

        if not result:
            logger.error("Skill comparison returned no result.")
            return pd.DataFrame(columns=["skill_resume", "skill_job_requirement", "alignment", "recommendation"])

        data = []
        for item in result:
            data.append({
                "skill_resume": item.get("matching_candidate_skill"),
                "skill_job_requirement": item.get("job_requirement"),
                "alignment": item.get("match_status"),
                "recommendation": item.get("recommendation") if item.get("match_status") == "missing" else None
            })

        self.df = pd.DataFrame(data)
        return self.df

    def analyze_gaps(self, state: ResumeState) -> ResumeState:
        self.compare_skills()

        if "job_role" in state and state["job_role"]:
            total_rows = self.df.shape[0]
            exact_matches = self.df[self.df['alignment'] == 'exact'].shape[0]
            match_percent = (exact_matches / total_rows) * 100 if total_rows > 0 else 0.0

            not_matched = self.df[self.df['alignment'] != 'exact']
            recommandations = not_matched['recommendation'].dropna().tolist()

            

        return {"match_percent":match_percent,"recommandations":recommandations}
