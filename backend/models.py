"""Pydantic models for candidate profile validation and API schemas."""

from pydantic import BaseModel, field_validator


class Education(BaseModel):
    degree: str
    college: str
    university: str
    graduation_year: int
    cgpa: str


class Skills(BaseModel):
    programming: list[str]
    frontend: list[str]
    backend: list[str]
    database: list[str]
    ai_ml: list[str]


class Project(BaseModel):
    name: str
    description: str
    tech_stack: list[str]


class SocialLinks(BaseModel):
    github: str
    linkedin: str
    portfolio: str


class Candidate(BaseModel):
    name: str
    headline: str
    education: Education
    skills: Skills
    projects: list[Project]
    experience: list[str]
    achievements: list[str]
    certifications: list[str]
    social_links: SocialLinks


class ChatRequest(BaseModel):
    message: str

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message must not be empty or only whitespace.")
        return v.strip()


class ChatResponse(BaseModel):
    response: str
