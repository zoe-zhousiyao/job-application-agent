from __future__ import annotations

from pydantic import BaseModel, Field


class JobAnalysis(BaseModel):
    extracted_skills: list[str] = Field(default_factory=list)
    extracted_keywords: list[str] = Field(default_factory=list)
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    match_score: int = 0
    summary: str = ""


class AgentOutput(BaseModel):
    analysis_report: str
    tailored_bullets: str
    cover_letter: str
