import os
from coagent.agents import ChatAgent, ModelClient
from coagent.core import AgentSpec, new
from dotenv import load_dotenv

load_dotenv()

with open("prompts/match_prompt.txt", "r", encoding="utf-8") as f:
    match_prompt = f.read()

match_agent = AgentSpec(
    "match",
    new(
        ChatAgent,
        system=match_prompt,
        client=ModelClient(
            model="openai/gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
        ),
    ),
)
