from openai import AsyncOpenAI
from pathlib import Path
import json


class LLMService:
    def __init__(self, api_key: str, model: str = "claud"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.prompt_dir = Path(__file__).parent.parent / "prompts"

    def _load_prompt(self, name: str) -> str:
        return (self.prompt_dir / f"{name}.txt").read_text(encoding="utf-8")

    async def analyze_github(self, repo_context: dict) -> dict:
        prompt = self._load_prompt("analyze_commits")

        # 커밋 로그 청킹 (토큰 초과 방지)
        commits_text = "\n".join(
            f"[{c['date'][:10]}] {c['message']}"
            for c in repo_context["commits"]
        )

        user_content = f"""
        ## README
        {repo_context['readme'][:3000]}

        ## 커밋 로그 (최근 100개)
        {commits_text[:4000]}

        ## 사용 언어
        {repo_context['languages']}
        """

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"},  # JSON 모드
            temperature=0.3
        )

        return json.loads(response.choices[0].message.content)