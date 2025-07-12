
from src.AI_Resume_Checker.state.state import ResumeState
from src.AI_Resume_Checker.agents.skill_extraction import SkillExtractor
from src.AI_Resume_Checker.agents.job_search import JobSearchAgent
from src.AI_Resume_Checker.agents.skill_extraction import SkillExtractor
from src.AI_Resume_Checker.agents.comparison_engine import SkillsComparisonEngine# You already have this
from typing import Dict

def load_resume_and_extract_skills(state: ResumeState) -> ResumeState:
    extractor = SkillExtractor(state["path"])
    extractor.convert_to_txt()
    state["resume_skills"] = extractor.extract_skills()
    return state

def load_job_description_and_extract_skills(state: ResumeState) -> ResumeState:
    
    
    if state.get("job_description"):
        agent = JobSearchAgent(state["job_role"], state["experience"], jd=state.get("job_description"))
        skills = agent.extract_from_uploaded_jd()
    else:
        agent = JobSearchAgent(state["job_role"], state["experience"])
        skills = agent.search_job_description()
        
    # Normalize to list of strings
    if isinstance(skills[0], dict) and "skill" in skills[0]:
        state["job_skills"] = [s["skill"] for s in skills]
    else:
        state["job_skills"] = skills

    return state

def compare_skills_and_generate_recommendations(state: ResumeState) -> ResumeState:
    engine = SkillsComparisonEngine(state)
    match_results = engine.analyze_gaps(state)
    state["match_percent"] = match_results.get("match_percent")
    state["recommendations"] = match_results.get("recommandations")
    return state
