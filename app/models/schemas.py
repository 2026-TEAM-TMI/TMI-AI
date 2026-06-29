from pydantic import BaseModel
from typing import List, Optional

# 입력
class GithubAnalyzeRequest(BaseModel):
    github_url: str          # https://github.com/user/repo
    github_token: Optional[str] = None  # private repo 대응

# 출력 (Spring Boot ↔ FastAPI 계약)
class ProjectSummary(BaseModel):
    project_name: str
    description: str
    my_role: str             # LLM이 추출한 본인 기여 역할
    tech_stack: List[str]
    contributions: List[str] # 기여 내역 bullet
    troubleshooting: List[str]
    period: str              # "2024.03 ~ 2024.06"

class PortfolioAnalyzeResponse(BaseModel):
    projects: List[ProjectSummary]
    total_skills: List[str]
    career_keywords: List[str]  # 강점 키워드 (추천에도 활용)

# 기업 추천
class JobRecommendRequest(BaseModel):
    career_keywords: List[str]
    skills: List[str]

class JobRecommendResponse(BaseModel):
    companies: List[dict]    # {name, match_score, reason, apply_url}


class CommitInfo:
    pass


class GitHubRepositoryContext:
    pass


class PullRequestInfo:
    pass


class RepositoryInfo:
    pass