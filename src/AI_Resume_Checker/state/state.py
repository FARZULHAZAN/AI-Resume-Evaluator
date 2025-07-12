
from typing import TypedDict, Optional, List

class ResumeState(TypedDict):
    path: str
    job_role: str
    experience: int
    job_description: Optional[str]
    recommendations: List[str]
    match_percent: float
    resume_skills: List[str]
    job_skills: List[str]
