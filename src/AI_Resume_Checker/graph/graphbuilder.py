# graph/workflow.py
from langgraph.graph import StateGraph, END
from src.AI_Resume_Checker.state.state import ResumeState
from src.AI_Resume_Checker.nodes.nodes import (
    load_resume_and_extract_skills,
    load_job_description_and_extract_skills,
    compare_skills_and_generate_recommendations,
)

def run_workflow() -> StateGraph:
    workflow = StateGraph(ResumeState)

    workflow.add_node("ExtractResumeSkills", load_resume_and_extract_skills)
    workflow.add_node("ExtractJobSkills", load_job_description_and_extract_skills)
    workflow.add_node("CompareAndRecommend", compare_skills_and_generate_recommendations)

    workflow.set_entry_point("ExtractResumeSkills")
    workflow.add_edge("ExtractResumeSkills", "ExtractJobSkills")
    workflow.add_edge("ExtractJobSkills", "CompareAndRecommend")
    workflow.add_edge("CompareAndRecommend", END)

    return workflow.compile()
agent=run_workflow()

