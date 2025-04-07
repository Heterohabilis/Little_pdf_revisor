import os
from coagent.agents import ChatAgent, ModelClient
from coagent.core import AgentSpec, new
from dotenv import load_dotenv

load_dotenv()

SCORE = "score"

with open("prompts/score_prompt.txt", "r", encoding="utf-8") as f:
    score_prompt = f.read()

score_agent = AgentSpec(
    SCORE,
    new(
        ChatAgent,
        system=score_prompt,
        client=ModelClient(
            model="openai/gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
        ),
    ),
)
