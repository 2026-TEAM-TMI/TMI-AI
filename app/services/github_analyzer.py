import httpx
from typing import List, Dict

class GitHubAnalyzer:
    BASE = "https://api.github.com"

    def __init__(self, token: str | None = None):
        headers = {"Accept": "application/vnd.github+json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        self.client = httpx.AsyncClient(headers=headers)

    async def get_repo_context(self, owner: str, repo: str) -> Dict:
        """커밋 로그, README, 언어 통계, PR 목록 수집"""
        commits   = await self._get_commits(owner, repo)
        readme    = await self._get_readme(owner, repo)
        languages = await self._get_languages(owner, repo)
        prs       = await self._get_merged_prs(owner, repo)

        return {
            "commits": commits[:100],   # 최근 100개
            "readme": readme,
            "languages": languages,
            "pull_requests": prs[:30],
        }

    async def _get_commits(self, owner, repo) -> List[Dict]:
        r = await self.client.get(
            f"{self.BASE}/repos/{owner}/{repo}/commits",
            params={"per_page": 100}
        )
        return [
            {"sha": c["sha"][:7], "message": c["commit"]["message"],
             "author": c["commit"]["author"]["name"],
             "date": c["commit"]["author"]["date"]}
            for c in r.json()
        ]

    async def _get_readme(self, owner, repo) -> str:
        r = await self.client.get(f"{self.BASE}/repos/{owner}/{repo}/readme")
        if r.status_code != 200:
            return ""
        import base64
        return base64.b64decode(r.json()["content"]).decode("utf-8", errors="ignore")